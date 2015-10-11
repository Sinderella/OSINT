import cmd

from stevedore import dispatch

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

        self.INPUT_PARAMS = ['FIRST_NAME', 'LAST_NAME', 'EMAIL', 'FACEBOOK']
        self.SHOW_PARAMS = ['params', 'options', 'info']
        self.params = dict()
        self.params['EMAIL'] = 'halloween@windowslive.com'

    def __set_check_func(self, plugin_name):
        self.dispatch_extension = plugin_name

    def do_reload(self, params):
        del self.mgr
        self.mgr = dispatch.DispatchExtensionManager(
            'osint.plugins.source',
            lambda *args, **kwds: True,
            invoke_on_load=True,
        )
        print(self.intro)

    def do_run(self, params):
        def filter_func(ext, extension_name, *args, **kwargs):
            return ext.name == extension_name

        def query_source(ext, extension_name, data, *args, **kwargs):
            ext.obj.set_query(data)
            return ext.obj.get_result()

        results = list()
        result = self.mgr.map(filter_func, query_source, 'google', "\"" + self.params['EMAIL'] + "\"")
        results.append(result)
        result = self.mgr.map(filter_func, query_source, 'bing', "\"" + self.params['EMAIL'] + "\"")
        results.append(result)

        for result in results:
            result[0].print_result()

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
            value = argv[1]
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
        print('')

    def __show_options(self):
        pass

    def __show_info(self):
        pass

    def do_quit(self, line):
        return True

    def postloop(self):
        print()
