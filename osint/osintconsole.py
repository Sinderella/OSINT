from Queue import Queue
import cmd
import re
from threading import Thread
import time

from bs4 import BeautifulSoup
from requests import ConnectionError
from stevedore import dispatch

from osint.models.person import Person, Email, Phone, Name, Relationship, Organisation, Location
from osint import THREAD_NO
from osint.utils.ners import url_ner
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
        self.queue = Queue()
        self.result = Person()
        self.params = dict()

        for i in range(THREAD_NO):
            thread = Thread(target=self.worker)
            thread.daemon = True
            thread.start()

    def worker(self):
        while True:
            url = self.queue.get()
            self.extract_info(url)
            self.queue.task_done()

    def extract_info(self, url):
        req = Requester()
        try:
            res = req.get(url)
        except ConnectionError:
            return
        soup = BeautifulSoup(res.content, 'html.parser')
        raw_text = soup.get_text(strip=True)

        extracted_emails = self._extract_email(raw_text)
        for email in extracted_emails:
            email_obj = Email()
            email_obj.address = email
            self.result.add_email(email_obj)

        extracted_phone_nos = self._extract_phone_no(raw_text)
        for phone_no in extracted_phone_nos:
            phone_no_obj = Phone()
            phone_no_obj.number = phone_no
            phone_no_obj.display = phone_no
            self.result.add_phone(phone_no_obj)

        # extract using NLP
        entities = url_ner(res.content)
        for tag, data in entities:
            if tag == 'PERSON':
                if data.lower() == (self.params['FIRST_NAME'] + ' ' + self.params['LAST_NAME']).lower():
                    continue
                relator = Relationship()

                relator_name = Name()
                relator_first_name = data.split(' ')[0]
                relator_last_name = data.split(' ')[-1]
                relator_name.first_name = relator_first_name
                relator_name.last_name = relator_last_name
                relator_name.display = data

                relator_person = Person()
                relator_person.add_name(relator_name)

                relator.person = relator_person
                relator.relationship_type = 'Unknown'

                self.result.add_relationship(relator)
            elif tag == 'ORGANIZATION':
                organisation = Organisation()
                organisation.name = data

                self.result.add_organisation(organisation)
            elif tag == 'LOCATION':
                location = Location()
                location.name = data

                self.result.add_location(location)

                # for key in self.result:
                #     if isinstance(self.result[key], list):
                #         counts = collections.Counter(self.result[key])
                #         self.result[key] = sorted(self.result[key], key=counts.get, reverse=True)
                #         self.result[key] = list(collections.OrderedDict.fromkeys(self.result[key]))

    def _extract_email(self, text):
        results = re.findall(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.(?!PNG|JPG|JS|GIF)[A-Z]{2,}', text, flags=re.IGNORECASE)
        return set(results)

    def _extract_phone_no(self, text):
        results = re.findall(r'(\+[0-9]{1,4}\(0\)[0-9\ ]{,8}|0[0-9\ ]{8,12})', text)
        return set(results)

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

        start_time = time.time()

        if 'EMAIL' in self.params:
            if ',' in self.params['EMAIL']:
                emails = self.params['EMAIL'].split[',']
            else:
                emails = [self.params['EMAIL']]
            for email in emails:
                results = self.mgr.map(filter_func, query_source, 'google', "\"" + email + "\"")
                for result in results:
                    [self.queue.put(url) for url in result.result['urls']]
                    # results = self.mgr.map(filter_func, query_source, 'bing', "\"" + email + "\"")
                    # for result in results:
                    #     [self.queue.put(url) for url in result.result['urls']]

                persons = self.mgr.map(filter_func, query_source, 'pipl', "email={}".format(self.params['EMAIL']))

                for person in persons:
                    self.result.add_person(person)

        if 'FIRST_NAME' in self.params and 'LAST_NAME' in self.params:
            full_name = self.params['FIRST_NAME'] + ' ' + self.params['LAST_NAME']
            results = self.mgr.map(filter_func, query_source, 'google', "\"" + full_name + "\"")
            for result in results:
                [self.queue.put(url) for url in result.result['urls']]
            # results = self.mgr.map(filter_func, query_source, 'bing', "\"" + full_name + "\"")
            # for result in results:
            #     [self.queue.put(url) for url in result.result['urls']]
            persons = self.mgr.map(filter_func, query_source, 'pipl',
                                   "first_name={}&last_name={}".format(self.params['FIRST_NAME'],
                                                                       self.params['LAST_NAME']))
            for person in persons:
                self.result.add_person(person)

        self.queue.join()
        print(self.result)
        # for key in self.result:
        #     print(Fore.YELLOW + '{}: '.format(key) + Fore.RESET)
        #     if isinstance(self.result[key], set) or isinstance(self.result[key], list):
        #         for url in self.result[key]:
        #             print('\t{}'.format(url))
        #     else:
        #         print('{}'.format(self.result[key]))
        # print(Fore.CYAN + '=' * 100 + Fore.RESET)

        end_time = time.time()
        hours, rem = divmod(end_time - start_time, 3600)
        minutes, seconds = divmod(rem, 60)
        print("Elapsed time: {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))

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
