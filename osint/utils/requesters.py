from requests import Session, adapters


class Requester(object):
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0'
        }
        self.session = Session()
        self.session.headers.update(self.headers)

        max_retries_adapter = adapters.HTTPAdapter(max_retries=5)
        self.session.mount('http://', max_retries_adapter)
        self.session.mount('https://', max_retries_adapter)

    def get(self, url):
        return self.session.get(url)

    def post(self, url, data):
        return self.session.post(url, data)

    def post_json(self, url, data):
        return self.session.post(url, json=data)

    def post_file(self, url, file_name):
        files = {
            'file': open(file_name, 'rb'),
        }
        return self.session.post(url, files=files)
