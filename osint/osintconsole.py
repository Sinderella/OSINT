# encoding=utf8
from __future__ import print_function

import cmd
import codecs
import datetime
import hashlib
import operator
import os
import re
import sqlite3
import time
from threading import Thread, Lock, Timer

from bs4 import BeautifulSoup
from requests import ConnectionError
from stevedore import dispatch

from osint.models.person import Person
from osint.utils.db_helpers import insert_entity
from osint.utils.ners import html_ner
from osint.utils.queues import WorkerQueue
from osint.utils.requesters import Requester
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
        self.url_queue = WorkerQueue()
        self.extract_queue = WorkerQueue()
        self.result = Person()
        self.params = dict()

        self.cur_db_cursor = None
        self.cur_db_name = None
        self.cur_db = None

        self.lock = Lock()
        self.running = False
        self.url_timer_running = False
        self.extract_timer_running = False

        self.start_time = 0

        # for i in range(THREAD_NO): # TODO: make it multithreading
        thread_targets = [self.url_worker, self.extract_worker]
        for target in thread_targets:
            thread = Thread(target=target)
            thread.daemon = True
            thread.start()

    def url_worker(self):
        while True:
            self.lock.acquire()
            url = self.url_queue.get()
            if not self.url_timer_running:
                self.url_timer_running = True
                self.url_timer()
            # TODO: separate extraction to different thread
            # TODO: optimise db connection overhead
            self.save_html(url)
            self.url_queue.task_done()
            self.lock.release()
            if self.url_queue.empty():
                self.url_queue.reset_count()
                self.prompt = "osint$ "
                self.running = False
                self.url_timer_running = False

                end_time = time.time()
                hours, rem = divmod(end_time - self.start_time, 3600)
                minutes, seconds = divmod(rem, 60)
                print("\n[*] Elapsed time: {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
                print(self.prompt, end='')

    def extract_worker(self):
        while True:
            self.lock.acquire()
            url = self.extract_queue.get()
            if not self.extract_timer_running:
                self.extract_timer_running = True
                self.extract_timer()
            self.extract_queue.task_done()
            self.lock.release()
            if self.extract_queue.empty():
                self.extract_queue.reset_count()
                self.prompt = "osint$ "
                self.running = False
                self.extract_timer_running = False

                end_time = time.time()
                hours, rem = divmod(end_time - self.start_time, 3600)
                minutes, seconds = divmod(rem, 60)
                print("\n[*] Elapsed time: {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
                print(self.prompt, end='')

    def url_timer(self):
        if self.running and self.url_timer_running:
            self._update_progress(self.url_queue.get_done(), self.url_queue.get_total(), "URL")
            Timer(300, self.url_timer).start()
        else:
            self.url_timer_running = False

    def save_html(self, url):
        req = Requester()
        try:
            res = req.get(url)
        except ConnectionError:
            return
        soup = BeautifulSoup(res.content, 'html.parser')
        raw_text = soup.get_text(strip=True)

        hash_filename = hashlib.sha1(self.cur_db_name + '//' + url).hexdigest()
        with codecs.open(self.cur_db_name + '/' + hash_filename + '.html', 'w', encoding='utf8') as fp:
            fp.write(raw_text)
        cur_db = sqlite3.connect(self.cur_db_name + '/documents.db')
        cur_db_cursor = cur_db.cursor()
        cur_db_cursor.execute("""
        insert into documents (url, path)
        values ('{}', '{}')
        """.format(url, self.cur_db_name + '/' + hash_filename + '.html'))
        cur_db.commit()
        cur_db.close()

    def extract_timer(self):
        if self.running and self.url_timer_running:
            self._update_progress(self.url_queue.get_done(), self.url_queue.get_total(), "document")
            Timer(300, self.extract_timer).start()
        else:
            self.url_timer_running = False

    def extract_info(self):
        # TODO: implement timer for extracting
        if self.running:
            print("[!] The program is running in the background, only one instance is allowed to be running")
            return
        self.prompt = "[extracting] osint$ "
        self.running = True
        self.start_time = time.time()
        print("[*] Connecting to the database...")
        try:
            cur_db = sqlite3.connect(self.cur_db_name + '/documents.db')
        except sqlite3.Error as e:
            print("[!] An error occurred: {}".format(e.args[0]))
            return
        cur_db_cursor = cur_db.cursor()

        results = cur_db_cursor.execute("SELECT did, path FROM documents").fetchall()
        print("[*] Started extracting entities...")
        for result in results:
            document_id = result[0]
            path_to_html = result[1]
            with codecs.open(path_to_html, 'rt', encoding='utf8') as fp:
                raw_text = fp.read()
            extracted_emails = self._extract_email(raw_text)
            for email in extracted_emails:
                insert_entity(cur_db_cursor, document_id, email, 'Email')
                # email_obj = Email()
                # email_obj.address = email
                # self.result.add_email(email_obj)

            extracted_phone_nos = self._extract_phone_no(raw_text)
            for phone_no in extracted_phone_nos:
                insert_entity(cur_db_cursor, document_id, phone_no, 'Phone')
                # phone_no_obj = Phone()
                # phone_no_obj.number = phone_no
                # phone_no_obj.display = phone_no
                # self.result.add_phone(phone_no_obj)

            # extract using NLP
            entities = html_ner(raw_text)
            for tag, data in entities:
                if tag == 'PERSON':
                    insert_entity(cur_db_cursor, document_id, data, 'Name')
                    # relator = Relationship()
                    #
                    # relator_name = Name()
                    # relator_first_name = data.split(' ')[0]
                    # relator_last_name = data.split(' ')[-1]
                    # relator_name.first_name = relator_first_name
                    # relator_name.last_name = relator_last_name
                    # relator_name.display = data
                    #
                    # relator_person = Person()
                    # relator_person.add_name(relator_name)
                    #
                    # relator.person = relator_person
                    # relator.relationship_type = 'Unknown'
                    #
                    # self.result.add_relationship(relator)
                elif tag == 'ORGANIZATION':
                    insert_entity(cur_db_cursor, document_id, data, 'Organisation')
                    # organisation = Organisation()
                    # organisation.name = data
                    #
                    # self.result.add_organisation(organisation)
                elif tag == 'LOCATION':
                    insert_entity(cur_db_cursor, document_id, data, 'Location')
                    # location = Location()
                    # location.name = data
                    #
                    # self.result.add_location(location)
        cur_db.commit()
        print("[*] Entities extraction is completed")

        # for key in self.result:
        #     if isinstance(self.result[key], list):
        #         counts = collections.Counter(self.result[key])
        #         self.result[key] = sorted(self.result[key], key=counts.get, reverse=True)
        #         self.result[key] = list(collections.OrderedDict.fromkeys(self.result[key]))

    def _extract_email(self, text):
        # results = re.findall(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.(?!PNG|JPG|JS|GIF)[A-Z]{2,}', text, flags=re.IGNORECASE)
        # results = re.findall(r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$', text, flags=re.IGNORECASE)
        # TODO: find a better regex
        results = re.findall(r'[a-z0-9\.]+@[a-z0-9\.]+\.[a-z]{2,}', text, flags=re.IGNORECASE)
        return set(results)

    def _extract_phone_no(self, text):
        # results = re.findall(r'(\+[0-9]{1,4}\(0\)[0-9\ ]{,8}|0[0-9\ ]{8,12})', text)
        results = re.findall(r'\+(?:[0-9]?){6,14}[0-9]', text)
        return set(results)

    def _update_progress(self, done_url, total_url, type):
        total_percentage = done_url * 100.0 / total_url
        print("\n[{0:5.2f}%] {1} remaining {2}s ({3} total {2}s)".format(total_percentage, total_url - done_url, type,
                                                                         total_url))

    def analyse(self):
        # TODO: analyse the extracted entities
        try:
            cur_db = sqlite3.connect(self.cur_db_name + '/documents.db')
        except sqlite3.Error as e:
            print("[!] An error occurred: {}".format(e.args[0]))
            return
        cur_db_cursor = cur_db.cursor()
        entities = {}
        results = cur_db_cursor.execute('SELECT type FROM entity_types')
        for result in results:
            entities[result[0]] = {}

        results = cur_db_cursor.execute('SELECT type, entity FROM entities')
        for result in results:
            entity_type = result[0]
            entity = result[1]
            if entity in entities.get(entity_type):
                entities[entity_type][entity] = entities.get(entity_type).get(entity) + 1
            elif entities.get(entity_type) is not None:
                entities[entity_type][entity] = 1

        # rank by frequency
        for entity_type in entities:
            entities[entity_type] = sorted(entities.get(entity_type).items(), key=operator.itemgetter(1), reverse=True)
        # print out the entities
        for entity_type in entities:
            print("{}:".format(entity_type))
            for entity in entities[entity_type]:
                print("[{0}] {1}".format(entity[1], entity[0].encode('utf-8')))

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

        if self.running:
            print("[!] The program is running in the background, only one instance is allowed to be running")
            return
        self.prompt = "[running] osint$ "
        self.running = True
        self.start_time = time.time()

        try:
            os.mkdir('./db')
        except OSError:
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

        # TODO: build queries based on input, permute through all inputs with full name
        # TODO: insert inputs as entities
        if 'EMAIL' in self.params:
            if ',' in self.params['EMAIL']:
                emails = self.params['EMAIL'].split[',']
            else:
                emails = [self.params['EMAIL']]
            for email in emails:
                results = self.mgr.map(filter_func, query_source, 'google', "\"" + email + "\"")
                for result in results:
                    [self.url_queue.put(url) for url in result.result['urls']]
                    # results = self.mgr.map(filter_func, query_source, 'bing', "\"" + email + "\"")
                    # for result in results:
                    #     [self.queue.put(url) for url in result.result['urls']]

                persons = self.mgr.map(filter_func, query_source, 'pipl', "email={}".format(self.params['EMAIL']))

                for person in persons:
                    self.result.add_person(person)

        if 'FIRST_NAME' in self.params and 'LAST_NAME' in self.params:
            full_name = self.params['FIRST_NAME'] + ' ' + self.params['LAST_NAME']
            # insert_entity(self.cur_db_cursor, None, full_name, 'Name')
            results = self.mgr.map(filter_func, query_source, 'google', "\"" + full_name + "\"")
            for result in results:
                [self.url_queue.put(url) for url in result.result['urls']]
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
        self.prompt = "[paused] osint$ "
        self.url_timer_running = False
        self.lock.acquire()

    def do_resume(self, params):
        """resume
        Resume the paused task running in background
        """
        self.prompt = "[running] osint$ "
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

    def do_list(self, params):
        """list
        List the saved states of gathered documents
        """
        try:
            os.mkdir('./db')
        except OSError:
            pass
        dir_list = [filename for filename in os.listdir('./db') if os.path.isdir('./db/' + filename)]
        print("Saved states:")
        for dir in dir_list:
            print("\t{}".format(dir))

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
