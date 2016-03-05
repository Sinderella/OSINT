import codecs
import hashlib
import re
from urllib import quote

import phonenumbers
from threading import Thread, Timer, Event

import sqlite3

import time
from bs4 import BeautifulSoup
from requests.exceptions import ContentDecodingError

from osint.utils.cleaners import EntityCleaner
from osint.utils.db_helpers import insert_entity
from requests import ConnectionError

from osint.utils.ners import html_ner
from osint.utils.queues import WorkerQueue
from osint.utils.requesters import Requester


class ProcessBase(Thread):
    def __init__(self, item_type, lock):
        super(ProcessBase, self).__init__()
        self.queue = WorkerQueue()
        self.start_time = time.time()
        self.added = False
        self.running = False
        self.completed = False
        self.item_type = item_type
        self.lock = lock

    def timer(self):
        if not self.completed:
            self._update_progress()
            Timer(60, self.timer).start()

    def put(self, item):
        self.queue.put(item)

    def _update_progress(self):
        if not self.running:
            return
        done_url = self.queue.get_done()
        total_url = self.queue.get_total()
        total_percentage = done_url * 100.0 / total_url
        print("\n[{0:5.2f}%] {1} remaining {2}s ({3} total {2}s)".format(total_percentage, total_url - done_url,
                                                                         self.item_type, total_url))


class Scraper(ProcessBase):
    def __init__(self, db_name, lock):
        super(Scraper, self).__init__("URL", lock)
        self.db_name = db_name
        self.cur_db = None

    def run(self):
        self.cur_db = sqlite3.connect(self.db_name + '/documents.db')
        while True:
            self.running = self.lock.acquire()
            url = self.queue.get()
            if not self.added:
                self.timer()
                self.added = True
            self.save_html(url)
            self.running = False
            self.lock.release()
            self.queue.task_done()
            if self.queue.empty():
                # Kill the timer
                self.completed = True
                end_time = time.time()
                hours, rem = divmod(end_time - self.start_time, 3600)
                minutes, seconds = divmod(rem, 60)
                print("\n[*] Scrapping elapsed time: {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
                self.cur_db.close()
                break

    def save_html(self, url):
        req = Requester()
        try:
            res = req.get(url)
        except ContentDecodingError as e:
            print("Error at saving html: {0}\nURL: {1}".format(e.message, url))
            return
        except ConnectionError:
            return
        soup = BeautifulSoup(res.content, 'html.parser')
        raw_text = soup.get_text("\n", strip=True)
        statements = [line for line in raw_text.split('\n')]
        total_word = len(statements)

        hash_filename = hashlib.sha1(self.db_name + '//' + url).hexdigest()
        with codecs.open(self.db_name + '/' + hash_filename + '.html', 'w', encoding='utf8') as fp:
            fp.write(raw_text)
        cur_db_cursor = self.cur_db.cursor()
        try:
            cur_db_cursor.execute("""
            insert into documents (url, total_word, path)
            values ('{}', {}, '{}')
            """.format(quote(url), total_word, self.db_name + '/' + hash_filename + '.html'))
            self.cur_db.commit()
        except sqlite3.OperationalError as e:
            print("Error: {0}\nURL: {1}\nTotal Words: {2}\nPath: {3}".format(e.message, url, total_word, hash_filename))
        except sqlite3.IntegrityError:
            pass


class Extractor(ProcessBase):
    def __init__(self, db_name, lock):
        super(Extractor, self).__init__("document", lock)
        self.entity_cleaner = EntityCleaner()
        self.db_name = db_name
        self.cur_db = None

    def run(self):
        self.cur_db = sqlite3.connect(self.db_name + '/documents.db')
        while True:
            self.running = self.lock.acquire()
            document_id, path_to_html = self.queue.get()
            if not self.added:
                self.timer()
                self.added = True
            self.extract_insert_info(document_id, path_to_html)
            self.running = False
            self.lock.release()
            self.queue.task_done()
            if self.queue.empty():
                # Kill the timer
                self.completed = False
                end_time = time.time()
                hours, rem = divmod(end_time - self.start_time, 3600)
                minutes, seconds = divmod(rem, 60)
                print("[*] Extraction elapsed time: {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
                self.cur_db.close()
                break

    def clean_insert_entity(self, cursor, doc_id, entity, entity_type):
        cleaned_entity = self.entity_cleaner.clean(entity)
        if cleaned_entity is None:
            return
        insert_entity(cursor, doc_id, cleaned_entity, entity_type)

    def extract_insert_info(self, document_id, path_to_html):
        cur_db_cursor = self.cur_db.cursor()
        with codecs.open(path_to_html, 'rt', encoding='utf8') as fp:
            raw_text = fp.read()
        extracted_emails = self._extract_email(raw_text)
        for email in extracted_emails:
            if email.endswith('.png') or email.endswith('.gif'):
                continue
            self.clean_insert_entity(cur_db_cursor, document_id, email, 'Email')

        extracted_phone_nos = self._extract_phone_no(raw_text)
        for phone_no in extracted_phone_nos:
            self.clean_insert_entity(cur_db_cursor, document_id, phone_no, 'Phone')
        # extract using NLP
        entities = html_ner(raw_text)
        for tag, data in entities:
            if tag == 'PERSON':
                self.clean_insert_entity(cur_db_cursor, document_id, data, 'Name')
            elif tag == 'ORGANIZATION':
                self.clean_insert_entity(cur_db_cursor, document_id, data, 'Organisation')
            elif tag == 'LOCATION':
                self.clean_insert_entity(cur_db_cursor, document_id, data, 'Location')
        self.cur_db.commit()

    @staticmethod
    def _extract_email(text):
        results = re.findall(r'[a-z0-9\.]+@[a-z0-9\.]+\.[a-z]{2,}', text, flags=re.IGNORECASE)
        return set(results)

    @staticmethod
    def _extract_phone_no(text):
        def __phone_sanity_check(no):
            open_parent = no.count('(')
            close_parent = no.count(')')
            if open_parent > 1 or close_parent > 1:
                return False
            return open_parent == close_parent

        results = re.findall(r'\+?[0-9\- \(\)]{8,16}[0-9]', text)
        phone_numbers = []
        for result in results:
            if __phone_sanity_check(result):
                try:
                    phone_numbers.append(phonenumbers.parse(result, None))
                except phonenumbers.phonenumberutil.NumberParseException:
                    continue
        phone_numbers = [phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL) for
                         phone_number in phone_numbers if phonenumbers.is_possible_number(phone_number)]
        return phone_numbers
