import json

from colorama import Fore


class Name(object):
    def __init__(self):
        self._first_name = None
        self._middle_name = None
        self._last_name = None
        self._display = None

    def __str__(self):
        return self.display

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        self._first_name = first_name

    @property
    def middle_name(self):
        return self._middle_name

    @middle_name.setter
    def middle_name(self, middle_name):
        self._middle_name = middle_name

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, last_name):
        self._last_name = last_name

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, display):
        self._display = display


class Address(object):
    def __init__(self):
        self._country = None
        self._state = None
        self._city = None
        self._street = None
        self._house_no = None
        self._apartment_no = None
        self._zip_code = None

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, country):
        self._country = country

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self._state = state

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, city):
        self._city = city

    @property
    def street(self):
        return self._street

    @street.setter
    def street(self, street):
        self._street = street

    @property
    def house_no(self):
        return self._house_no

    @house_no.setter
    def house_no(self, house_no):
        self._house_no = house_no

    @property
    def apartment_no(self):
        return self._apartment_no

    @apartment_no.setter
    def apartment_no(self, apartment_no):
        self._apartment_no = apartment_no

    @property
    def zip_code(self):
        return self._zip_code

    @zip_code.setter
    def zip_code(self, zip_code):
        self._zip_code = zip_code


class Email(object):
    def __init__(self):
        self._email_type = None
        self._address = None
        self._email_provider = None

    @property
    def email_type(self):
        return self._email_type

    @email_type.setter
    def email_type(self, email_type):
        self._email_type = email_type

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address):
        self._address = address

    @property
    def email_provider(self):
        return self._email_provider

    @email_provider.setter
    def email_provider(self, email_provider):
        self._email_provider = email_provider


class Username(object):
    def __init__(self):
        self._name = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


class DateofBirth(object):
    def __init__(self):
        self._date_range = None
        self._display = None

    @property
    def date_range(self):
        return self._date_range

    @date_range.setter
    def date_range(self, date_range):
        self._date_range = date_range

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, display):
        self._display = display


class Image(object):
    def __init__(self):
        self._url = None

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url


class Job(object):
    def __init__(self):
        self._title = None
        self._organisation = None
        self._industry = None
        self._date_range = None
        self._display = None

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def organisation(self):
        return self._organisation

    @organisation.setter
    def organisation(self, organisation):
        self._organisation = organisation

    @property
    def industry(self):
        return self._industry

    @industry.setter
    def industry(self, industry):
        self._industry = industry

    @property
    def date_range(self):
        return self._date_range

    @date_range.setter
    def date_range(self, date_range):
        self._date_range = date_range

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, display):
        self._display = display


class Education(object):
    def __init__(self):
        self._degree = None
        self._school = None
        self._date_range = None
        self._display = None

    @property
    def degree(self):
        return self._degree

    @degree.setter
    def degree(self, degree):
        self._degree = degree

    @property
    def school(self):
        return self._school

    @school.setter
    def school(self, school):
        self._school = school

    @property
    def date_range(self):
        return self._date_range

    @date_range.setter
    def date_range(self, date_range):
        self._date_range = date_range

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, display):
        self._display = display


class Gender(object):
    def __init__(self):
        self._gender = None
        self._ethnicity = None

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        self._gender = gender

    @property
    def ethnicity(self):
        return self._ethnicity

    @ethnicity.setter
    def ethnicity(self, ethnicity):
        self._ethnicity = ethnicity


class Language(object):
    def __init__(self):
        self._language = None
        self._region = None
        self._display = None

    @property
    def language(self):
        return self._language

    @language.setter
    def language(self, language):
        self._language = language

    @property
    def region(self):
        return self._region

    @region.setter
    def region(self, region):
        self._region = region

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, display):
        self._display = display


class OriginCountry(object):
    def __init__(self):
        self._country = None

    @property
    def country(self):
        return self._country

    @country.setter
    def country(self, country):
        self._country = country


class Relationship(object):
    def __init__(self):
        self._relationship_type = None
        self._subtype = None
        self._person = None

    @property
    def relationship_type(self):
        return self._relationship_type

    @relationship_type.setter
    def relationship_type(self, relationship_type):
        self._relationship_type = relationship_type

    @property
    def subtype(self):
        return self._subtype

    @subtype.setter
    def subtype(self, subtype):
        self._subtype = subtype

    @property
    def person(self):
        return self._person

    @person.setter
    def person(self, person):
        self._person = person


class Url(object):
    def __init__(self):
        self._domain = None
        self._name = None
        self._category = None
        self._url = None

    @property
    def domain(self):
        return self._domain

    @domain.setter
    def domain(self, domain):
        self._domain = domain

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, category):
        self._category = category

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        self._url = url


class DateRange(object):
    def __init__(self):
        self._start = None
        self._end = None

    @property
    def start(self):
        return self._start

    @start.setter
    def start(self, start):
        self._start = start

    @property
    def end(self):
        return self._end

    @end.setter
    def end(self, end):
        self._end = end


class Phone(object):
    def __init__(self):
        self._country_code = None
        self._number = None
        self._phone_type = None
        self._extension = None
        self._display = None
        self._display_international = None

    @property
    def country_code(self):
        return self._country_code

    @country_code.setter
    def country_code(self, country_code):
        self._country_code = country_code

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, number):
        self._number = number

    @property
    def phone_type(self):
        return self._phone_type

    @phone_type.setter
    def phone_type(self, phone_type):
        self._phone_type = phone_type

    @property
    def extension(self):
        return self._extension

    @extension.setter
    def extension(self, extension):
        self._extension = extension

    @property
    def display(self):
        return self._display

    @display.setter
    def display(self, display):
        self._display = display

    @property
    def display_international(self):
        return self._display_international

    @display_international.setter
    def display_international(self, display_international):
        self._display_international = display_international


class UserIDs(object):
    def __init__(self):
        self._user_id = None

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        self._user_id = user_id


class Person(object):
    def __init__(self):
        self._names = list()
        self._emails = list()
        self._usernames = list()
        self._user_ids = list()
        self._phones = list()
        self._gender = Gender()
        self._dob = DateofBirth()
        self._languages = list()
        self._ethnicities = list()
        self._origin_countries = list()
        self._addresses = list()
        self._jobs = list()
        self._educations = list()
        self._relationships = list()
        self._images = list()
        self._urls = list()

    def __str__(self):
        tmp = Fore.YELLOW + 'Name(s):' + Fore.RESET
        for name in self._names:
            tmp += '\n\t{}'.format(name.display)
        if self._gender.gender is not None:
            tmp += Fore.YELLOW + '\nGender: {}'.format(self._gender.gender) + Fore.RESET
        tmp += Fore.YELLOW + '\nEmail(s):' + Fore.RESET
        for email in self._emails:
            tmp += '\n\t{}'.format(email.address)
        tmp += Fore.YELLOW + '\nUsername(s):' + Fore.RESET
        for username in self._usernames:
            tmp += '\n\t{}'.format(username.name)
        tmp += Fore.YELLOW + '\nImage(s):' + Fore.RESET
        for image in self._images:
            tmp += '\n\t{}'.format(image.url)
        if self._dob.display is not None:
            tmp += Fore.YELLOW + '\nDOB: {}'.format(self._dob.display) + Fore.RESET
        tmp += Fore.YELLOW + '\nUrl(s):' + Fore.RESET
        for url in self._urls:
            tmp += '\n\t{}'.format(url.url)
        tmp += Fore.YELLOW + '\nEducation:' + Fore.RESET
        for education in self._educations:
            tmp += '\n\t{}'.format(education.display)
        tmp += Fore.YELLOW + '\nJob:' + Fore.RESET
        for job in self._jobs:
            tmp += '\n\t{}'.format(job.industry)
        tmp += Fore.YELLOW + '\nUser ID:' + Fore.RESET
        for user_id in self._user_ids:
            tmp += '\n\t{}'.format(user_id.user_id)
        tmp += Fore.RESET + '\n'
        tmp += Fore.CYAN + '=' * 100 + Fore.RESET
        return tmp

    def parse_json(self, data):
        # TODO: Split into methods and have proper exception handlings
        if 'names' in data:
            for name in data['names']:
                tmp = Name()
                try:
                    tmp.first_name = name['first']
                    tmp.last_name = name['last']
                    tmp.display = name['display']
                    tmp.middle_name = name['middle']
                except KeyError:
                    pass
                finally:
                    self._names.append(tmp)

        if 'usernames' in data:
            for username in data['usernames']:
                tmp = Username()
                try:
                    tmp.name = username['content']
                except KeyError:
                    pass
                finally:
                    self._usernames.append(tmp)

        if 'urls' in data:
            for url in data['urls']:
                tmp = Url()
                try:
                    tmp.url = url['url']
                    tmp.domain = url['@domain']
                    tmp.category = url['@category']
                    tmp.name = url['@name']
                except KeyError:
                    pass
                finally:
                    self._urls.append(tmp)

        if 'origin_countries' in data:
            for origin in data['origin_countries']:
                tmp = OriginCountry()
                try:
                    tmp.country = origin['country']
                except KeyError:
                    pass
                finally:
                    self._origin_countries.append(tmp)

        if 'images' in data:
            for image in data['images']:
                tmp = Image()
                try:
                    tmp.url = image['url']
                except KeyError:
                    pass
                finally:
                    self._images.append(tmp)

        if 'gender' in data:
            self._gender = Gender()
            self._gender.gender = data['gender']['content']

        if 'languages' in data:
            for language in data['languages']:
                tmp = Language()
                try:
                    tmp.language = language['language']
                    tmp.region = language['region']
                    tmp.display = language['display']
                except KeyError:
                    pass
                finally:
                    self._languages.append(tmp)

        if 'user_ids' in data:
            for ID in data['user_ids']:
                tmp = UserIDs()
                try:
                    tmp.user_id = ID['content']
                except KeyError:
                    pass
                finally:
                    self._user_ids.append(tmp)

        if 'addresses' in data:
            for address in data['addresses']:
                tmp = Address()
                try:
                    tmp.display = address['display']
                    tmp.country = address['country']
                    tmp.city = address['city']
                    tmp.state = address['state']
                    tmp.street = address['street']
                    tmp.house_no = address['house']
                    tmp.apartment_no = address['apartment']
                    tmp.zip_code = address['zip_code']
                except KeyError:
                    pass
                finally:
                    self._addresses.append(tmp)

        if 'educations' in data:
            for education in data['educations']:
                tmp = Education()
                try:
                    tmp.display = education['display']
                    tmp.school = education['school']
                    if 'date_range' in education:
                        tmp2 = DateRange()
                        tmp2.start = education['date_range']['start']
                        tmp2.end = education['date_range']['end']
                        tmp.date_range = tmp2
                    tmp.degree = education['degree']
                except KeyError:
                    pass
                finally:
                    self._educations.append(tmp)

        if 'jobs' in data:
            for job in data['jobs']:
                tmp = Job()
                try:
                    tmp.industry = job['industry']
                    tmp.title = job['title']
                    tmp.organisation = job['organization']
                    tmp.display = job['display']
                    if 'date_range' in job:
                        tmp2 = DateRange()
                        tmp2.start = job['date_range']['start']
                        tmp2.end = job['date_range']['end']
                        tmp.date_range = tmp2
                except KeyError:
                    pass
                finally:
                    self._jobs.append(tmp)

        if 'emails' in data:
            for email in data['emails']:
                tmp = Email()
                try:
                    tmp.address = email['address']
                    tmp.email_provider = email['@email_provider']
                except KeyError:
                    pass
                finally:
                    self._emails.append(tmp)

    def add_name(self, name_obj):
        if isinstance(name_obj, Name):
            self._names.append(name_obj)
        else:
            raise TypeError("A Name object is required")

    def add_email(self, email_obj):
        if isinstance(email_obj, Email):
            self._emails.append(email_obj)
        else:
            raise TypeError("An Email object is required")

    def add_username(self, username_obj):
        if isinstance(username_obj, Username):
            self._usernames.append(username_obj)
        else:
            raise TypeError("An Username object is required")

    def add_phone(self, phone_obj):
        if isinstance(phone_obj, Phone):
            self._phones.append(phone_obj)
        else:
            raise TypeError("A Phone object is required")

    def set_gender(self, gender_obj):
        if isinstance(gender_obj, Gender):
            self._gender = gender_obj
        else:
            raise TypeError("A Gender object is required")

    def set_dob(self, dob_obj):
        if isinstance(dob_obj, DateofBirth):
            self._dob = dob_obj
        else:
            raise TypeError("A DateofBirth object is required")

    def add_origin_country(self, origin_obj):
        if isinstance(origin_obj, OriginCountry):
            self._origin_countries.append(origin_obj)
        else:
            raise TypeError("An OriginCountry object is required")

    def add_address(self, address_obj):
        if isinstance(address_obj, Address):
            self._addresses.append(address_obj)
        else:
            raise TypeError("An Address object is required")

    def add_job(self, job_obj):
        if isinstance(job_obj, Job):
            self._jobs.append(job_obj)
        else:
            raise TypeError("A Job object is required")

    def add_education(self, education_obj):
        if isinstance(education_obj, Education):
            self._educations.append(education_obj)
        else:
            raise TypeError("An Education object is required")

    def add_image(self, image_obj):
        if isinstance(image_obj, Image):
            self._images.append(image_obj)
        else:
            raise TypeError("An Image object is required")

    def add_url(self, url_obj):
        if isinstance(url_obj, Url):
            self._urls.append(url_obj)
        else:
            raise TypeError("An Url object is required")

    def add_language(self, language_obj):
        if isinstance(language_obj, Language):
            self._languages.append(language_obj)
        else:
            raise TypeError("A Language object is required")

    def add_relationship(self, relationship_obj):
        if isinstance(relationship_obj, Relationship):
            self._relationships.append(relationship_obj)
        else:
            raise TypeError("A Relationship object is required")


if __name__ == '__main__':
    p = Person()
    data = json.loads('''{
    "@http_status_code": 200,
    "@visible_sources": 3,
    "@available_sources": 3,
    "@search_id": "1510210815255949377596975554993797861",
    "query": {
        "names": [
            {
                "first": "Thanat",
                "last": "Sirithawornsant",
                "display": "Thanat Sirithawornsant"
            }
        ]
    },
    "possible_persons": [
        {
            "@match": 0.0004,
            "@search_pointer": "9cccc2b829d581c24bfd1b94d565063e7f211bd57e9687f16e935a450820e3f33fdbabfb1cf7be0ae0a8cedf3560dd67b073629f97b1c5624958cb3c317149d6528647334710fbb12e85931b88718834ca4d7e32eb68492b13ac3747811fe72875bdb75648d9548c09df24154b690019b6d702efd876b825bcdd70c4bb214a2888bc28ada082dd5fa3088867a1b9723e441d252939beef3d064d07067e55346a5f694c3fbda1123b7a6e54551d8fc7ce201be6f2300fbde6216a057a2bc8e4b49b586b8effd9f2e43ef1a9639d3cc87e50f1a4dd2656c56a41ee85721b6b62d3b073629f97b1c5624958cb3c317149d6aa2d6b16b47889bf08bee173a7ee3a6e",
            "names": [
                {
                    "first": "Thanat",
                    "last": "Sirithawornsant",
                    "display": "Thanat Sirithawornsant"
                }
            ],
            "usernames": [
                {
                    "content": "neew0llah"
                }
            ],
            "gender": {
                "content": "male"
            },
            "languages": [
                {
                    "@inferred": true,
                    "region": "US",
                    "language": "en",
                    "display": "en_US"
                }
            ],
            "origin_countries": [
                {
                    "@inferred": true,
                    "country": "TH"
                }
            ],
            "user_ids": [
                {
                    "content": "1392009737@facebook"
                }
            ],
            "images": [
                {
                    "url": "http://graph.facebook.com/1392009737/picture?type=large",
                    "thumbnail_token": "AE2861B242686E6ACBCD539D133B8AE59A9AE962DB1FA5AA7AF08DA8D66F09F912648682D9CDB2322ADF85744B699B543C4E5FE3AC5A92&dsid=39830"
                }
            ]
        },
        {
            "@match": 0.0004,
            "@search_pointer": "976a2f041d0434c2d3939b266eb92bb06b3d79b154f170bc76699d5476ca8ef1260ace39d223c15461d9bea1d5346d171ce0fe6b5e31cbd6b38f6976576fe8d82a086b684fee8f6f470752bc33a1e83fd722a24c7517effd8fcfc5b9e60dba85f67f8740aa62fadd7a04527163cb8ec9b198afef8ada52b65cb6880f5f63fa3465a4ff0f2b0a8dc8378e13339b5baa701bcccabd66bdf2a95f4c9bb61a6e6f15220f3606f4d09a9fc9a63b08bf3624f9dc187a68c73b22f7b34e4dfdb0ba4c366280a383d48ede618435c55ef80b6ab36bcc489b827427ff6a7ea041e7f0166429cbd9de2c91415619a28312fdc047beac30a39ad97d4b69f123678f8564532a19d4a5f9fc23fb7512de069db5f9e1d2df11187373942e0c25c27caf9e3697b889600bf0a925a33a55dc81a902394e011925d7974e051643db8511a07d905bb1d8e67bc4b6b95365f52adce3a54958645361904b489c1d68b745f4910de88cf116c6e645d849bd5f2f6b08db5046cfb07b2a5816d27b50b1820ee1b4994c38b4c89ca2d704e974566b8683831630f786eabc00b7e418415ed228944896b521a4",
            "names": [
                {
                    "first": "Thanat",
                    "last": "Sirithawornsant",
                    "display": "Thanat Sirithawornsant"
                }
            ],
            "languages": [
                {
                    "@inferred": true,
                    "language": "th",
                    "display": "th"
                }
            ],
            "origin_countries": [
                {
                    "@inferred": true,
                    "country": "TH"
                }
            ],
            "addresses": [
                {
                    "country": "TH",
                    "display": "Thailand"
                }
            ],
            "jobs": [
                {
                    "industry": "Computer Software"
                }
            ],
            "educations": [
                {
                    "degree": "Bachelor's degree",
                    "school": "King Mongkut's Institute of Technology Ladkrabang",
                    "date_range": {
                        "start": "2012-01-01",
                        "end": "2015-12-31"
                    },
                    "display": "Bachelor's degree from King Mongkut's Institute of Technology Ladkrabang (2012-2015)"
                },
                {
                    "@valid_since": "2010-01-01",
                    "school": "KMITL",
                    "display": "KMITL"
                },
                {
                    "@valid_since": "2010-01-01",
                    "school": "Sarasas Ektra School",
                    "date_range": {
                        "start": "2000-01-01",
                        "end": "2011-12-31"
                    },
                    "display": "Sarasas Ektra School (2000-2011)"
                }
            ],
            "user_ids": [
                {
                    "content": "152968298@linkedin"
                },
                {
                    "@valid_since": "2010-01-01",
                    "content": "43/28B/3A2@linkedin"
                }
            ]
        }
    ]
}''')
    p.parse_json(data['possible_persons'][1])
    print(p)
