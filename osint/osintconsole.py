# encoding: utf-8
from __future__ import print_function

import cmd
import codecs
import datetime
import errno
import operator
import os
import sqlite3
from threading import Lock, Semaphore

from stevedore import dispatch

from osint.models.person import Person
from osint.utils.analyser import Analyser
from osint.utils.queues import WorkerQueue
from osint.utils.threads import Scraper, Extractor
from utils.parsers import param_parser


class Console(cmd.Cmd):
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.mgr = dispatch.DispatchExtensionManager(
                'osint.plugins.source',
                lambda *args, **kwds: True,
                invoke_on_load=True,
        )
        self.intro = "Loaded " + str(len(self.mgr.extensions)) + " modules"
        self.prompt = "osint$ "

        self.INPUT_PARAMS = ['FIRST_NAME', 'LAST_NAME', 'EMAIL', 'USERNAME', 'FACEBOOK', 'LINKEDIN']
        self.SHOW_PARAMS = ['params', 'options', 'info']

        self.queries = []

        self.url_queue = WorkerQueue()
        self.extract_queue = WorkerQueue()
        self.result = Person()
        self.params = dict()

        self.cur_db_cursor = None
        self.cur_db_name = None
        self.cur_db = None

        self.lock = Lock()
        self.sema = Semaphore(1)
        self.running = False
        self.url_timer_running = False
        self.extract_timer_running = False

        self.start_time = 0

    def extract_info(self):
        print("[*] Connecting to the database...")
        try:
            cur_db = sqlite3.connect(self.cur_db_name + '/documents.db')
        except sqlite3.Error as e:
            print("[!] An error occurred: {}".format(e.args[0]))
            return
        cur_db_cursor = cur_db.cursor()

        results = cur_db_cursor.execute("SELECT did, path FROM documents").fetchall()
        extractor = Extractor(self.cur_db_name, self.lock)
        extractor.start()
        print("[*] Started entities extraction...")
        for result in results:
            document_id = result[0]
            path_to_html = result[1]
            extractor.put((document_id, path_to_html))

    def analyse(self):
        analyser = Analyser(self.cur_db_name, self.queries)
        analyser.analyse()
        # # TODO: analyse the extracted entities
        # try:
        #     cur_db = sqlite3.connect(self.cur_db_name + '/documents.db')
        # except sqlite3.Error as e:
        #     print("[!] An error occurred: {}".format(e.args[0]))
        #     return
        # cur_db_cursor = cur_db.cursor()
        # entities = {}
        # results = cur_db_cursor.execute('SELECT type FROM entity_types')
        # for result in results:
        #     entities[result[0]] = {}
        #
        # results = cur_db_cursor.execute('SELECT type, entity FROM entities')
        # for result in results:
        #     entity_type = result[0]
        #     entity = result[1]
        #     if entity in entities.get(entity_type):
        #         entities[entity_type][entity] = entities.get(entity_type).get(entity) + 1
        #     elif entities.get(entity_type) is not None:
        #         entities[entity_type][entity] = 1
        #
        # # rank by frequency
        # for entity_type in entities:
        #     entities[entity_type] = sorted(entities.get(entity_type).items(), key=operator.itemgetter(1), reverse=True)
        # # print out the entities
        # for entity_type in entities:
        #     print("{}:".format(entity_type))
        #     for entity in entities[entity_type]:
        #         print("[{0}] {1}".format(entity[1], entity[0].encode('utf-8')))

    def do_analyse(self, params):
        self.analyse()

    def do_extract(self, params):
        self.extract_info()

    def do_reload(self, params):
        del self.mgr
        self.mgr = dispatch.DispatchExtensionManager(
                'osint.plugins.source',
                lambda *args, **kwds: True,
                invoke_on_load=True,
        )
        print(self.intro)

    def do_run(self, params):
        """run
        Gather information from different sources using supplied information.
        """

        def filter_func(ext, extension_name, *args, **kwargs):
            return ext.name == extension_name

        def query_source(ext, extension_name, data, *args, **kwargs):
            ext.obj.query = data
            return ext.obj.get_result()

        try:
            os.mkdir('./db')
        except OSError as e:
            if e.errno != errno.EEXIST:
                pass

        self.cur_db_name = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        os.mkdir('./db/' + self.cur_db_name)
        self.cur_db_name = './db/' + self.cur_db_name
        self.cur_db = sqlite3.connect(self.cur_db_name + '/documents.db')
        self.cur_db_cursor = self.cur_db.cursor()

        with codecs.open('./schema.sql', 'rt') as f:
            schema = f.read()
        self.cur_db.executescript(schema)
        with codecs.open('./types.sql', 'rt') as f:
            types = f.read()
        self.cur_db.executescript(types)
        self.cur_db.commit()

        print("[*] Started scraping websites...")
        scraper = Scraper(self.cur_db_name, self.lock, self.queries)
        scraper.start()

        # TODO: build queries based on input, permute through all inputs with full name
        # TODO: insert inputs as entities
        if 'EMAIL' in self.params:
            if ',' in self.params['EMAIL']:
                emails = self.params['EMAIL'].split[',']
            else:
                emails = [self.params['EMAIL']]
            for email in emails:
                results = self.mgr.map(filter_func, query_source, 'google', "\"" + email + "\"")
                self.queries.append(email)
                for result in results:
                    [scraper.put(url) for url in result.result['urls']]
                    # [self.url_queue.put(url) for url in result.result['urls']]
                    # results = self.mgr.map(filter_func, query_source, 'bing', "\"" + email + "\"")
                    # for result in results:
                    #     [self.queue.put(url) for url in result.result['urls']]

                    # persons = self.mgr.map(filter_func, query_source, 'pipl', "email={}".format(self.params['EMAIL']))
                    #
                    # for person in persons:
                    #     self.result.add_person(person)

        if 'FIRST_NAME' in self.params and 'LAST_NAME' in self.params:
            full_name = self.params['FIRST_NAME'] + ' ' + self.params['LAST_NAME']
            # insert_entity(self.cur_db_cursor, None, full_name, 'Name')
            results = self.mgr.map(filter_func, query_source, 'google', "\"" + full_name + "\"")
            self.queries.append(full_name)
            for result in results:
                [scraper.put(url) for url in result.result['urls']]
                # [self.url_queue.put(url) for url in result.result['urls']]
                # results = self.mgr.map(filter_func, query_source, 'bing', "\"" + full_name + "\"")
                # for result in results:
                #     [self.queue.put(url) for url in result.result['urls']]
                # persons = self.mgr.map(filter_func, query_source, 'pipl',
                #                        "first_name={}&last_name={}".format(self.params['FIRST_NAME'],
                #                                                            self.params['LAST_NAME']))
                # for person in persons:
                #     self.result.add_person(person)

                # self.queue.join()
                # print(self.result)
                # for key in self.result:
                #     print(Fore.YELLOW + '{}: '.format(key) + Fore.RESET)
                #     if isinstance(self.result[key], set) or isinstance(self.result[key], list):
                #         for url in self.result[key]:
                #             print('\t{}'.format(url))
                #     else:
                #         print('{}'.format(self.result[key]))
                # print(Fore.CYAN + '=' * 100 + Fore.RESET)

    def do_pause(self, params):
        """pause
        Pause the running task in background
        """
        self.lock.acquire()

    def do_resume(self, params):
        """resume
        Resume the paused task running in background
        """
        self.lock.release()

    def do_set(self, params):
        """set [param] [value]
        Set the searching parameter with the input value.
        ---
        FIRST_NAME - First name of the profile
        LAST_NAME - Last name of the profile
        EMAIL - Emails of the profile (e.g. name@domain.com, or ['name@domain.com', 'name2@domain.com']
        FACEBOOK - Facebook username or profile id (e.g. /zuck, or id=111111)
        """
        argc, argv = param_parser(params)
        #
        key = argv[0]
        if argc > 1:
            value = ''.join(argv[1:])
        else:
            value = ""
        if key and key in self.INPUT_PARAMS:
            print(key + '=> ' + value)
            self.params[key] = value
        else:
            self.do_help('set')

    def complete_set(self, text, *args):
        if not text:
            completions = self.INPUT_PARAMS[:]
        else:
            completions = [f
                           for f in self.INPUT_PARAMS
                           if f.startswith(text.upper())]
        return completions

    def do_show(self, params):
        """show [<params|options|info>]
        Display information of the parameter
        ---
        params - parameters
        options - option
        info - complete information of the profile
        """
        argc, argv = param_parser(params)
        if argc != 1:
            self.do_help('show')
            return
        return {
            'params': self.__show_params,
            'options': self.__show_options,
            'info': self.__show_info,
        }.get(argv[0])()

    def complete_show(self, text, *args):
        if not text:
            completions = self.SHOW_PARAMS
        else:
            completions = [f
                           for f in self.SHOW_PARAMS
                           if f.startswith(text.lower())]
        return completions

    def do_load(self, params):
        """load [db_name]
        Load the saved state of gathered documents
        ---
        db_name - name of the db
        """
        argc, argv = param_parser(params)
        if argc != 1:
            self.do_list()
            return
        self.cur_db_name = './db/' + argv[0]
        self.cur_db = sqlite3.connect(self.cur_db_name + '/documents.db')
        self.cur_db_cursor = self.cur_db.cursor()
        self.cur_db_cursor.execute('SELECT count(*) FROM documents')
        loaded_row = self.cur_db_cursor.fetchall()[0][0]
        print("{} documents are loaded".format(loaded_row))

    def do_list(self, params=None):
        """list
        List the saved states of gathered documents
        """
        try:
            os.mkdir('./db')
        except OSError:
            pass
        dir_list = [filename for filename in os.listdir('./db') if os.path.isdir('./db/' + filename)]
        print("Saved states:")
        for dir_name in dir_list:
            print("\t{}".format(dir_name))

    def do_listdoc(self, params):
        """listdoc
        List all the saved documents
        """
        self.cur_db_cursor.execute('SELECT url, path FROM documents')
        result = self.cur_db_cursor.fetchall()
        for row in result:
            print('\t{}\t{}'.format(row[1], row[0]))

    def __show_params(self):
        print('Name: {} {}'.format(self.params.get('FIRST_NAME', ''), self.params.get('LAST_NAME', '')))
        print('Email: {}'.format(self.params.get('EMAIL', '')))
        print('Facebook: {}'.format(self.params.get('FACEBOOK', '')))
        print('Linkedin: {}'.format(self.params.get('LINKEDIN', '')))
        print('')

    def __show_options(self):
        pass

    def __show_info(self):
        print(self.result)
        # for key in self.result:
        #     print('{}:'.format(key))
        #     if isinstance(self.result[key], set):
        #         for item in list(self.result[key]):
        #             print('\t{}'.format(item))
        #     else:
        #         print('\t{}'.format(self.result[key]))

    def do_EOF(self, line):
        return True

    def postloop(self):
        print()
