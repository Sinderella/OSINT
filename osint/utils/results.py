class Result(object):
    def __init__(self, source_name=None):
        self.source_name = source_name
        self.result = dict()
        self.result['source_name'] = self.source_name

    def set_source_name(self, source_name):
        self.source_name = source_name
        self.result['source_name'] = self.source_name

    def add_url(self, url):
        if self.result in 'urls':
            self.result['urls'].append(url)
        else:
            self.result['urls'] = [url, ]

    def add_urls(self, urls):
        if self.result in urls:
            self.result['urls'] += urls
        else:
            self.result['urls'] = urls

    def print_result(self):
        if self.source_name is None:
            return
        for key in self.result.keys():
            if isinstance(self.result[key], str):
                print(key.capitalize() + ': ' + self.result[key])
            elif isinstance(self.result[key], list):
                print(key.capitalize() + ': ')
                for item in self.result[key]:
                    print("\t" + str(item))
            else:
                return
