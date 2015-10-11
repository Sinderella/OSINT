from bs4 import BeautifulSoup

import base
from osint.utils.requesters import Requester
from osint.utils.results import Result


class Google(base.SourceBase):
    """Google
    """

    def __init__(self):
        base.SourceBase.__init__(self)
        self.web_requester = Requester()
        self.url = 'https://www.google.com/search?q={}'
        self.query = None

    def set_query(self, query):
        self.query = query

    def get_result(self):
        result = Result('Google')
        response = self.web_requester.get(self.url.format(self.query))
        soup = BeautifulSoup(response.content, "html.parser")
        tmp = soup.select('[style="margin-bottom:23px"]')
        if len(tmp) > 0 and tmp.text.startswith('No results found'):
            return result
        links = [x['href'] for x in soup.select('.srg .rc .r a[onmousedown]')]
        result.add_urls(links)
        return result


if __name__ == '__main__':
    g = Google()
    g.set_query('"halloween@windowslive.com"')
    print g.get_result()
