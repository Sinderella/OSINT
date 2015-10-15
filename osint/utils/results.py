class Result(object):
    def __init__(self, source_name=None):
        self._source_name = source_name
        self._result = dict()
        self._result['source_name'] = self._source_name

    @property
    def source_name(self):
        return self._source_name

    @source_name.setter
    def source_name(self, source_name):
        self._source_name = source_name

    @property
    def result(self):
        return self._result

    def set_source_name(self, source_name):
        self.source_name = source_name
        self.result['source_name'] = self.source_name

    def add_url(self, url):
        if 'urls' not in self.result:
            self.result['urls'] = [url, ]
            return
        self.result['urls'].append(url)

    def add_urls(self, urls):
        if 'urls' in self.result:
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
