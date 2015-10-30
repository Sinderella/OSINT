from osint.models.person import Person
from osint.plugins import base
from osint.utils.requesters import Requester


class Pipl(base.SourceBase):
    def __init__(self):
        super(Pipl, self).__init__()
        self.web_requester = Requester()
        self.url = 'https://api.pipl.com/search/v4/?key=sample_key&no_sponsored=true&{}'
        self._query = None

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, query):
        if isinstance(query, str):
            self._query = query
        elif isinstance(query, dict):
            self._query = list()
            if 'FIRST_NAME' in query and 'LAST_NAME' in query:
                self._query.append("first_name={}&last_name={}".format(query['FIRST_NAME'], query['LAST_NAME']))
            if 'EMAIL' in query:
                self._query.append("email={}".format(query['EMAIL']))
            if 'USERNAME' in query:
                self._query.append("username={}".format(query['USERNAME']))

    def get_result(self):
        if isinstance(self.query, str):
            responses = [self.web_requester.get(self.url.format(self.query)), ]
        elif isinstance(self.query, list):
            responses = [self.web_requester.get(self.url.format(query)) for query in self.query]
        else:
            raise TypeError("A query is required")

        person = Person()

        for response in responses:
            data = response.json()

            if data['@http_status_code'] == 403:
                raise RuntimeError('API calls limitation exceeds')
            elif data['@http_status_code'] != 200:
                continue
            if 'person' in data:
                person.parse_json(data['person'])
            if 'possible_persons' in data:
                for possible_person in data['possible_persons']:
                    person.parse_json(possible_person)

                    # try:
                    #     result.add_images([url['url'] for url in data['person']['images']])
                    # except KeyError:
                    #     pass
                    # try:
                    #     result.add_origins([origin['country'] for origin in data['person']['origin_countries']])
                    # except KeyError:
                    #     pass
                    # try:
                    #     result.add_urls([url['url'] for url in data['person']['urls']])
                    # except KeyError:
                    #     pass
                    # try:
                    #     result.add_usernames([username['content'] for username in data['person']['usernames']])
                    # except KeyError:
                    #     pass

        return person


if __name__ == '__main__':
    p = Pipl()
    query = dict()
    query['FIRST_NAME'] = "Thanat"
    query['LAST_NAME'] = "Sirithawornsant"
    # query['EMAIL'] = "halloween@windowslive.com"
    # query['USERNAME'] = "sinderella"
    # p.query = 'first_name=thanat&last_name=sirithawornsant'
    p.query = query
    result = p.get_result()
    print(result)
