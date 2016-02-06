import sqlite3


def insert_keyword(cursor, keyword_type, keyword):
    if not isinstance(cursor, sqlite3.Cursor):
        return False
    cursor.execute('INSERT INTO keywords(type, keyword) VALUES("{0}", "{1}")'.format(keyword_type, keyword))


def insert_entity(cursor, did, entity, entity_type):
    if not isinstance(cursor, sqlite3.Cursor):
        return False
    cursor.execute(
        'INSERT INTO entities(did, entity, type) VALUES({0}, "{1}", "{2}")'.format(did, entity,  entity_type))
