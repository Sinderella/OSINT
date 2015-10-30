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


class Organisation(object):
    def __init__(self):
        self._name = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


class Location(object):
    def __init__(self):
        self._name = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name


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
        self._organisations = list()
        self._locations = list()

    def __str__(self):
        tmp = Fore.YELLOW + 'Name(s):' + Fore.RESET
        for name in self._names:
            tmp += '\n\t{}'.format(name.display)
        if self._gender.gender is not None:
            tmp += Fore.YELLOW + '\nGender:' + Fore.RESET + '{}'.format(self._gender.gender)
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
            if 'facebook' in user_id.user_id:
                tmp += '\n\t{} https://www.facebook.com/profile.php?id={}'.format(user_id.user_id,
                                                                                  user_id.user_id.split('@')[0])
            elif 'linkedin' in user_id.user_id and '/' in user_id.user_id:
                tmp += '\n\t{} https://www.linkedin.com/pub/{}-{}/{}'.format(user_id.user_id, self.names[0].first_name,
                                                                             self.names[0].last_name,
                                                                             user_id.user_id.split('@')[0])
            else:
                tmp += '\n\t{}'.format(user_id.user_id)
        tmp += Fore.YELLOW + '\nOrganisation:' + Fore.RESET
        for organisation in self._organisations:
            tmp += '\n\t{}'.format(organisation.name)
        tmp += Fore.YELLOW + '\nLocation:' + Fore.RESET
        for location in self._locations:
            tmp += '\n\t{}'.format(location.name)
        tmp += Fore.RESET + '\n'
        tmp += Fore.CYAN + '=' * 100 + Fore.RESET
        return tmp

    def parse_json(self, data):
        # TODO: Split into methods and have proper exception handlings
        if 'names' in data:
            for name in data['names']:
                tmp = Name()
                tmp.first_name = name.get('first')
                tmp.last_name = name.get('last')
                tmp.display = name.get('display')
                tmp.middle_name = name.get('middle')
                self._names.append(tmp)

        if 'usernames' in data:
            for username in data['usernames']:
                tmp = Username()
                tmp.name = username.get('content')
                self._usernames.append(tmp)

        if 'urls' in data:
            for url in data['urls']:
                tmp = Url()
                tmp.url = url.get('url')
                tmp.domain = url.get('@domain')
                tmp.category = url.get('@category')
                tmp.name = url.get('name')
                self._urls.append(tmp)

        if 'origin_countries' in data:
            for origin in data['origin_countries']:
                tmp = OriginCountry()
                tmp.country = origin.get('country')
                self._origin_countries.append(tmp)

        if 'images' in data:
            for image in data['images']:
                tmp = Image()
                tmp.url = image.get('url')
                self._images.append(tmp)

        if 'gender' in data:
            self._gender = Gender()
            self._gender.gender = data['gender'].get('content')

        if 'languages' in data:
            for language in data['languages']:
                tmp = Language()
                tmp.language = language.get('language')
                tmp.region = language.get('region')
                tmp.display = language.get('display')
                self._languages.append(tmp)

        if 'user_ids' in data:
            for ID in data['user_ids']:
                tmp = UserIDs()
                tmp.user_id = ID.get('content')
                self._user_ids.append(tmp)

        if 'addresses' in data:
            for address in data['addresses']:
                tmp = Address()
                tmp.display = address.get('display')
                tmp.country = address.get('country')
                tmp.city = address.get('city')
                tmp.state = address.get('state')
                tmp.street = address.get('street')
                tmp.house_no = address.get('house')
                tmp.apartment_no = address.get('apartment')
                tmp.zip_code = address.get('zip_code')
                self._addresses.append(tmp)

        if 'educations' in data:
            for education in data['educations']:
                tmp = Education()
                tmp.display = education.get('display')
                tmp.school = education.get('school')
                if 'date_range' in education:
                    tmp2 = DateRange()
                    tmp2.start = education['date_range'].get('start')
                    tmp2.end = education['date_range'].get('end')
                    tmp.date_range = tmp2
                tmp.degree = education.get('degree')
                self._educations.append(tmp)

        if 'jobs' in data:
            for job in data['jobs']:
                tmp = Job()
                tmp.industry = job.get('industry')
                tmp.title = job.get('title')
                tmp.organisation = job.get('organization')
                tmp.display = job.get('display')
                if 'date_range' in job:
                    tmp2 = DateRange()
                    tmp2.start = job['date_range'].get('start')
                    tmp2.end = job['date_range'].get('end')
                    tmp.date_range = tmp2
                self._jobs.append(tmp)

        if 'emails' in data:
            for email in data['emails']:
                tmp = Email()
                tmp.address = email.get('address')
                tmp.email_provider = email.get('@email_provider')
                self._emails.append(tmp)

    def add_person(self, person):
        self._addresses += person.addresses
        if self._dob is None:
            self._dob = person.dob
        self._educations += person.educations
        self._emails += person.emails
        self._ethnicities += person.ethnicities
        if self._gender is None:
            self._gender = person.gender
        self._images += person.images
        self._jobs += person.jobs
        self._languages += person.languages
        self._names += person.names
        self._origin_countries += person.origin_countries
        self._phones += person.phones
        self._relationships += person.relationships
        self._urls += person.urls
        self._user_ids += person.user_ids
        self._usernames += person.usernames

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

    def add_organisation(self, organisation_obj):
        if isinstance(organisation_obj, Organisation):
            self._organisations.append(organisation_obj)
        else:
            raise TypeError("An Organisation object is required")

    def add_location(self, location_obj):
        if isinstance(location_obj, Location):
            self._locations.append(location_obj)
        else:
            raise TypeError("A Location object is required")

    @property
    def addresses(self):
        return self._addresses

    @addresses.setter
    def addresses(self, addresses):
        self._addresses = addresses

    @property
    def dob(self):
        return self._dob

    @dob.setter
    def dob(self, dob):
        self._dob = dob

    @property
    def educations(self):
        return self._educations

    @educations.setter
    def educations(self, educations):
        self._educations = educations

    @property
    def educations(self):
        return self._educations

    @educations.setter
    def educations(self, educations):
        self._educations = educations

    @property
    def emails(self):
        return self._emails

    @emails.setter
    def emails(self, emails):
        self._emails = emails

    @property
    def ethnicities(self):
        return self._ethnicities

    @ethnicities.setter
    def ethnicities(self, ethnicities):
        self._ethnicities = ethnicities

    @property
    def gender(self):
        return self._gender

    @gender.setter
    def gender(self, gender):
        self._gender = gender

    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, images):
        self._images = images

    @property
    def jobs(self):
        return self._jobs

    @jobs.setter
    def jobs(self, jobs):
        self._jobs = jobs

    @property
    def languages(self):
        return self._languages

    @languages.setter
    def languages(self, languages):
        self._languages = languages

    @property
    def names(self):
        return self._names

    @names.setter
    def names(self, names):
        self._names = names

    @property
    def origin_countries(self):
        return self._origin_countries

    @origin_countries.setter
    def origin_countries(self, origin_countries):
        self._origin_countries = origin_countries

    @property
    def phones(self):
        return self._phones

    @phones.setter
    def phones(self, phones):
        self._phones = phones

    @property
    def relationships(self):
        return self._relationships

    @relationships.setter
    def relationships(self, relationships):
        self._relationships = relationships

    @property
    def urls(self):
        return self._urls

    @urls.setter
    def urls(self, urls):
        self._urls = urls

    @property
    def user_ids(self):
        return self._user_ids

    @user_ids.setter
    def user_ids(self, user_ids):
        self._user_ids = user_ids

    @property
    def usernames(self):
        return self._usernames

    @usernames.setter
    def usernames(self, usernames):
        self._usernames = usernames

    @property
    def organisations(self):
        return self._organisations

    @organisations.setter
    def organisations(self, organisations):
        self._organisations = organisations

    @property
    def locations(self):
        return self._locations

    @locations.setter
    def locations(self, locations):
        self._locations = locations
