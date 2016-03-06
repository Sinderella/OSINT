import string

from osint.utils.cleaners import EntityCleaner


class TestEntityCleaner(object):
    def __init__(self):
        self.ec = EntityCleaner()
        self.expected = 'test'
        self.exclude = list(string.punctuation.replace('@', '').replace('.', ''))

    def test_entity_cleaner_exclamation(self):
        content = self.expected + '!'
        cleaned = self.ec.clean(content)
        assert not any(letter in self.exclude for letter in cleaned) and cleaned == self.expected

    def test_entity_cleaner_double_quote(self):
        content = self.expected + '"'
        cleaned = self.ec.clean(content)
        assert not any(letter in self.exclude for letter in cleaned) and cleaned == self.expected

    def test_entity_cleaner_sharp(self):
        content = self.expected + '#'
        cleaned = self.ec.clean(content)
        assert not any(letter in self.exclude for letter in cleaned) and cleaned == self.expected

    def test_entity_cleaner_dollar(self):
        content = self.expected + '$'
        cleaned = self.ec.clean(content)
        assert not any(letter in self.exclude for letter in cleaned) and cleaned == self.expected

    def test_entity_cleaner_percent(self):
        content = self.expected + '%'
        cleaned = self.ec.clean(content)
        assert not any(letter in self.exclude for letter in cleaned) and cleaned == self.expected

    def test_entity_cleaner_single_quote(self):
        content = self.expected + '%'
        cleaned = self.ec.clean(content)
        assert not any(letter in self.exclude for letter in cleaned) and cleaned == self.expected

    def test_entity_cleaner_parentheses(self):
        content = self.expected + '(){}[]'
        cleaned = self.ec.clean(content)
        assert not any(letter in self.exclude for letter in cleaned) and cleaned == self.expected

    def test_entity_cleaner_operators(self):
        content = self.expected + '*+-/'
        cleaned = self.ec.clean(content)
        assert not any(letter in self.exclude for letter in cleaned) and cleaned == self.expected

    def test_entity_cleaner_colon(self):
        content = self.expected + ':'
        cleaned = self.ec.clean(content)
        assert not any(letter in self.exclude for letter in cleaned) and cleaned == self.expected

    def test_entity_cleaner_semi_colon(self):
        content = self.expected + ';'
        cleaned = self.ec.clean(content)
        assert not any(letter in self.exclude for letter in cleaned) and cleaned == self.expected

    def test_entity_cleaner_question(self):
        content = self.expected + '?'
        cleaned = self.ec.clean(content)
        assert not any(letter in self.exclude for letter in cleaned) and cleaned == self.expected

    def test_entity_cleaner_back_slash(self):
        content = self.expected + '\\'
        cleaned = self.ec.clean(content)
        assert not any(letter in self.exclude for letter in cleaned) and cleaned == self.expected

    def test_entity_cleaner_special(self):
        content = self.expected + '^`_|~'
        cleaned = self.ec.clean(content)
        assert not any(letter in self.exclude for letter in cleaned) and cleaned == self.expected
