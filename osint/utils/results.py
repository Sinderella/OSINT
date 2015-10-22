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

    def add_image(self, image):
        if 'images' not in self.result:
            self.result['images'] = [image, ]
        else:
            self.result['images'].append(image)

    def add_images(self, images):
        if 'images' in self.result:
            self.result['images'] += images
        else:
            self.result['images'] = images

    def add_origin(self, origin):
        if 'origins' not in self.result:
            self.result['origins'] = [origin, ]
        else:
            self.result['origins'].append(origin)

    def add_origins(self, origins):
        if 'origins' in self.result:
            self.result['origins'] += origins
        else:
            self.result['origins'] = origins

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

    def add_username(self, username):
        if 'usernames' not in self.result:
            self.result['usernames'] = [username, ]
            return
        self.result['usernames'].append(username)

    def add_usernames(self, usernames):
        if 'usernames' in self.result:
            self.result['usernames'] += usernames
        else:
            self.result['usernames'] = usernames

    def print_result(self):
        if self.source_name is None:
            return
        print('Source: {}'.format(self.source_name))
        for key in self.result.keys():
            if key == 'source_name':
                continue
            if isinstance(self.result[key], str):
                print(key.capitalize() + ': ' + self.result[key])
            elif isinstance(self.result[key], list):
                print(key.capitalize() + ': ')
                for item in self.result[key]:
                    print("\t" + str(item))
            else:
                return
