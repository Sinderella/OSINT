from bs4 import BeautifulSoup

import base
from osint.utils.requesters import Requester
from osint.utils.results import Result


class Google(base.SourceBase):
    """Google
    """

    def __init__(self):
        super(Google, self).__init__()
        self.web_requester = Requester()
        self.url = 'https://www.google.com/search?q={}&start={}'
        self._query = None

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = query

    def get_result(self):
        result = Result('Google')
        for n in range(0, 20, 10):
            response = self.web_requester.get(self.url.format(self.query, n))
            soup = BeautifulSoup(response.content, "html.parser")
            tmp = soup.select('#res')
            if len(tmp) == 0:
                break
            links = [x['href'] for x in soup.select('.srg .rc .r a[onmousedown]')]
            result.add_urls(links)
        return result
