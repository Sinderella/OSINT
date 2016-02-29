import re
import string


class EntityCleaner(object):
    exclude = string.punctuation.replace('@', '').replace('.', '')
    regex = re.compile('[%s]' % re.escape(exclude))

    def clean(self, entity):
        if len(entity) < 3:
            return None
        try:
            return self.regex.sub('', entity)
        except TypeError as e:
            print("Error stripping entity: {0}\nEntity: {1}".format(e.message, entity))
            return None
        except AttributeError as e:
            print("Error stripping entity: {0}\nEntity: {1}".format(e.message, entity))
            return None
