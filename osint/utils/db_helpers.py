import sqlite3


def insert_keyword(cursor, keyword_type, keyword):
    if not isinstance(cursor, sqlite3.Cursor):
        return False
    try:
        cursor.execute('INSERT INTO keywords(type, keyword) VALUES("{0}", "{1}")'.format(keyword_type, keyword))
    except (sqlite3.OperationalError, ValueError) as e:
        print("Error inserting keyword: {0}\nKeyword Type: {1}\nKeyword: {2}".format(e.message, keyword_type, keyword))


def insert_entity(cursor, did, entity, entity_type):
    if not isinstance(cursor, sqlite3.Cursor):
        return False
    try:
        cursor.execute(
            'INSERT INTO entities(did, entity, type) VALUES({0}, "{1}", "{2}")'.format(did, entity, entity_type))
    except (sqlite3.OperationalError, ValueError) as e:
        print(
            "Error inserting entity: {0}\nDocument ID: {1}\nEntity Type: {2}\nEntity: {3}".format(e.message, did,
                                                                                                  entity,
                                                                                                  entity_type))
