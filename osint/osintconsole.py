# encoding: utf-8
from __future__ import print_function

import cmd
import codecs
import datetime
import errno
import os
import sqlite3
from urllib import unquote
from threading import Lock

from stevedore import dispatch

from osint.utils.analyser import Analyser
from osint.utils.db_helpers import insert_keyword
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
        self.intro_msg = "Loaded " + str(len(self.mgr.extensions)) + " modules"
        print(self.intro_msg)
        self.prompt = "osint$ "

        self.INPUT_PARAMS = ['Name', 'Email', 'Phone',
                             'Location']  # 'Image', 'URL', 'Education', 'Job', 'User ID', 'Organisation', 'Location']
        self.SHOW_PARAMS = ['params']

        self.queries = []

        self.params = dict()

        self.cur_db_cursor = None
        self.cur_db_name = None
        self.cur_db = None

        self.lock = Lock()

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

        return extractor

    def analyse(self, expected_types=None):
        analyser = Analyser(self.cur_db_name, self.queries, expected_types)
        analyser.start()

        return analyser

    def do_analyse(self, params):
        """analyse
        Analyse the retrieved entities
        """
        argc, argv = param_parser(params)
        if argc == 0:
            print("Please provide what you're looking for (e.g. name, location, ...)")
            return
        expected_types = [expected_type.strip() for expected_type in argv[0].split(',')]
        return self.analyse(expected_types)

    def do_extract(self, params):
        """extract
        Extract information from the retrieved documents
        """
        return self.extract_info()

    def do_reload(self, params):
        """reload
        Reload new modules as plugins
        """
        del self.mgr
        self.mgr = dispatch.DispatchExtensionManager(
            'osint.plugins.source',
            lambda *args, **kwds: True,
            invoke_on_load=True,
        )
        print(self.intro_msg)

    def precmd(self, line):
        if self.cur_db_name:
            return line

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

        return line

    def do_url(self, params):
        """url [entity]
        Get the source(s) of the retrieved entity
        ---
        entity - The entity that will be traced back to the URL
        """
        argc, argv = param_parser(params)

        if argc == 1:
            entity = argv[0]
        elif argc > 1:
            entity = ' '.join(argv[0:])
        else:
            self.do_help('url')
            return

        if self.cur_db_name is None:
            print("[!] Database is not loaded")
            return

        self.cur_db = sqlite3.connect(self.cur_db_name + '/documents.db')
        self.cur_db_cursor = self.cur_db.cursor()

        query = 'SELECT documents.url FROM documents WHERE documents.did IN ' \
                '(SELECT DISTINCT entities.did FROM entities WHERE entities.entity LIKE \'%{0}%\')'
        self.cur_db_cursor.execute(query.format(entity))

        loaded_rows = self.cur_db_cursor.fetchall()
        if len(loaded_rows):
            print("Entity: {} is not found in the database".format(entity))
            return

        urls = [row[0] for row in loaded_rows]
        print("Entity: {} is retrieved from:".format(entity))
        for url in urls:
            if '%3A' in url:
                url = unquote(url).decode('utf8')
            print("\t{}".format(url))

    def do_run(self, params):
        """run
        Gather information from different sources using supplied information.
        """

        def filter_func(ext, extension_name, *args, **kwargs):
            return ext.name == extension_name

        def query_source(ext, extension_name, data, *args, **kwargs):
            ext.obj.query = data
            return ext.obj.get_result()

        print("[*] Started scraping websites...")
        scraper = Scraper(self.cur_db_name, self.lock)

        # TODO: build queries based on input, permute through all inputs with full name
        cur_db_cursor = self.cur_db.cursor()
        for row in cur_db_cursor.execute('SELECT type, keyword FROM keywords'):
            keyword_type = row[0]
            keyword = row[1]
            for plugin in ['google', 'bing']:
                results = self.mgr.map(filter_func, query_source, plugin, "\"" + keyword + "\"")
                self.queries.append(keyword)
                for result in results:
                    [scraper.put(url) for url in result.result['urls']]

        scraper.start()

        return scraper

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
        Name - First name of the profile
        Email - Emails of the profile (e.g. name@domain.com, or ['name@domain.com', 'name2@domain.com']
        Phone - Phone number
        Location - Name of the location
        """
        argc, argv = param_parser(params)
        #
        key = argv[0]
        if argc > 1:
            value = ' '.join(argv[1:])
        else:
            value = ""
        value = value.lower()
        if key and key in self.INPUT_PARAMS:
            print(key + ' => ' + value)
            self.params[key] = value
            insert_keyword(self.cur_db_cursor, key, value)
            self.cur_db.commit()
        else:
            self.do_help('set')

    def complete_set(self, text, *args):
        if not text:
            completions = self.INPUT_PARAMS[:]
        else:
            completions = [f
                           for f in self.INPUT_PARAMS
                           if f.startswith(text.title())]
        return completions

    def do_show(self, params):
        """show [params]
        Display information of the parameter
        ---
        params - parameters
        """
        argc, argv = param_parser(params)
        if argc == 1 and argv[0] in self.SHOW_PARAMS:
            return {
                'params': self.__show_params,
            }.get(argv[0])()
        else:
            self.do_help('show')

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
        print('Current DB: {0}'.format(self.cur_db_name))
        for key in self.params:
            print('{0}: {1}'.format(key.title(), self.params[key]))
        print('')

    def do_EOF(self, line):
        """EOF
        """
        return True

    def postloop(self):
        print()
