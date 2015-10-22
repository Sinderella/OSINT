from Queue import Queue
import cmd
import re
from threading import Thread

from bs4 import BeautifulSoup
from colorama import Fore
from requests import ConnectionError
from stevedore import dispatch

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
        self.results = dict()
        self.params = dict()

        for i in range(3):
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
        if 'email' in self.results:
            self.results['email'] = self.results['email'].union(self._extract_email(raw_text))
        else:
            self.results['email'] = self._extract_email(raw_text)

        if 'phone_no' in self.results:
            self.results['phone_no'] = self.results['phone_no'].union(self._extract_phone_no(raw_text))
        else:
            self.results['phone_no'] = self._extract_phone_no(raw_text)

        # extract using NLP

        for key in self.results:
            if isinstance(self.results[key], list):
                self.results[key].sort()

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

        self.results.clear()

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

        if 'FIRST_NAME' in self.params and 'LAST_NAME' in self.params:
            full_name = self.params['FIRST_NAME'] + ' ' + self.params['LAST_NAME']
            results = self.mgr.map(filter_func, query_source, 'google', "\"" + full_name + "\"")
            for result in results:
                [self.queue.put(url) for url in result.result['urls']]
            # results = self.mgr.map(filter_func, query_source, 'bing', "\"" + full_name + "\"")
            # for result in results:
            #     [self.queue.put(url) for url in result.result['urls']]
            results = self.mgr.map(filter_func, query_source, 'pipl',
                                   "first_name={}&last_name={}".format(self.params['FIRST_NAME'],
                                                                       self.params['LAST_NAME']))
        self.queue.join()
        for key in self.results:
            print(Fore.YELLOW + '{}: '.format(key) + Fore.RESET)
            if isinstance(self.results[key], set):
                for url in self.results[key]:
                    print('\t{}'.format(url))
            else:
                print('{}'.format(self.results[key]))
        print(Fore.CYAN + '=' * 100 + Fore.RESET)

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
        for key in self.results:
            print('{}:'.format(key))
            if isinstance(self.results[key], set):
                for item in list(self.results[key]):
                    print('\t{}'.format(item))
            else:
                print('\t{}'.format(self.results[key]))

    def do_EOF(self, line):
        return True

    def postloop(self):
        print()
