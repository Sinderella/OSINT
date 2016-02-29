from bs4 import BeautifulSoup

import base
from osint.utils.requesters import Requester
from osint.utils.results import Result


class Bing(base.SourceBase):
    """Bing
    """

    def __init__(self):
        super(Bing, self).__init__()
        self.web_requester = Requester()
        self.url = 'https://www.bing.com/search?q={}&first={}'
        self._query = None

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        self._query = query

    def get_result(self):
        result = Result('Bing')
        for n in range(1, 21, 10):
            response = self.web_requester.get(self.url.format(self.query, n))
            soup = BeautifulSoup(response.content, "html.parser")
            links = [x['href'] for x in soup.select('li.b_algo h2 a')]
            result.add_urls(links)
        return result
