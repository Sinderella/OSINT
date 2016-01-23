import codecs
import hashlib
import re
import phonenumbers
from threading import Thread, Timer, Event

import sqlite3

import time
from bs4 import BeautifulSoup
from osint.utils.db_helpers import insert_entity
from requests import ConnectionError

from osint.utils.ners import html_ner
from osint.utils.queues import WorkerQueue
from osint.utils.requesters import Requester


class ProcessBase(Thread):
    def __init__(self, item_type, lock, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(ProcessBase, self).__init__(group, target, name, args, kwargs, verbose)
        self.queue = WorkerQueue()
        self.start_time = time.time()
        self.added = False
        self.pause = False
        self.item_type = item_type
        self.lock = lock

    def timer(self):
        if not self.added:
            return
        self._update_progress()
        Timer(300, self.timer).start()

    def put(self, item):
        if not self.added:
            self.timer()
        self.queue.put(item)
        self.added = True

    def _update_progress(self):
        done_url = self.queue.get_done()
        total_url = self.queue.get_total()
        total_percentage = done_url * 100.0 / total_url
        print("\n[{0:5.2f}%] {1} remaining {2}s ({3} total {2}s)".format(total_percentage, total_url - done_url,
                                                                         self.item_type, total_url))


class Scraper(ProcessBase):
    def __init__(self, db_name, lock, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(Scraper, self).__init__("URL", lock, group, target, name, args, kwargs, verbose)
        self.db_name = db_name
        self.cur_db = None

    def run(self):
        self.cur_db = sqlite3.connect(self.db_name + '/documents.db')
        while True:
            self.lock.acquire()
            url = self.queue.get()
            # TODO: separate extraction to different thread
            # TODO: optimise db connection overhead
            self.save_html(url)
            self.lock.release()
            self.queue.task_done()
            if self.queue.empty():
                # Kill the timer
                self.added = False
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
        except ConnectionError:
            return
        soup = BeautifulSoup(res.content, 'html.parser')
        raw_text = soup.get_text(strip=True)

        hash_filename = hashlib.sha1(self.db_name + '//' + url).hexdigest()
        with codecs.open(self.db_name + '/' + hash_filename + '.html', 'w', encoding='utf8') as fp:
            fp.write(raw_text)
        cur_db_cursor = self.cur_db.cursor()
        cur_db_cursor.execute("""
        insert into documents (url, path)
        values ('{}', '{}')
        """.format(url, self.db_name + '/' + hash_filename + '.html'))
        self.cur_db.commit()


class Extractor(ProcessBase):
    def __init__(self, db_name, lock, group=None, target=None, name=None, args=(), kwargs=None, verbose=None):
        super(Extractor, self).__init__("document", lock, group, target, name, args, kwargs, verbose)
        self.db_name = db_name
        self.cur_db = None

    def run(self):
        self.cur_db = sqlite3.connect(self.db_name + '/documents.db')
        while True:
            self.lock.acquire()
            document_id, path_to_html = self.queue.get()
            self.extract_insert_info(document_id, path_to_html)
            self.lock.release()
            self.queue.task_done()
            if self.queue.empty():
                # Kill the timer
                self.added = False
                end_time = time.time()
                hours, rem = divmod(end_time - self.start_time, 3600)
                minutes, seconds = divmod(rem, 60)
                print("[*] Extraction elapsed time: {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
                self.cur_db.close()
                break

    def extract_insert_info(self, document_id, path_to_html):
        cur_db_cursor = self.cur_db.cursor()
        with codecs.open(path_to_html, 'rt', encoding='utf8') as fp:
            raw_text = fp.read()
        extracted_emails = self._extract_email(raw_text)
        for email in extracted_emails:
            insert_entity(cur_db_cursor, document_id, email, 'Email')

        extracted_phone_nos = self._extract_phone_no(raw_text)
        for phone_no in extracted_phone_nos:
            insert_entity(cur_db_cursor, document_id, phone_no, 'Phone')
        # extract using NLP
        entities = html_ner(raw_text)
        for tag, data in entities:
            if tag == 'PERSON':
                insert_entity(cur_db_cursor, document_id, data, 'Name')
            elif tag == 'ORGANIZATION':
                insert_entity(cur_db_cursor, document_id, data, 'Organisation')
            elif tag == 'LOCATION':
                insert_entity(cur_db_cursor, document_id, data, 'Location')
        self.cur_db.commit()

    @staticmethod
    def _extract_email(text):
        # results = re.findall(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.(?!PNG|JPG|JS|GIF)[A-Z]{2,}', text, flags=re.IGNORECASE)
        # results = re.findall(r'^([a-z0-9]+(-[a-z0-9]+)*\.)+[a-z]{2,}$', text, flags=re.IGNORECASE)
        # TODO: find a better regex
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
