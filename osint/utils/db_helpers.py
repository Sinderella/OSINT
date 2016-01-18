import sqlite3


def insert_entity(cursor, did, entity, type):
    if not isinstance(cursor, sqlite3.Cursor):
        return False
    if did is None:
        cursor.execute(
                'INSERT INTO entities(entity, type) VALUES("{0}", "{1}")'.format(entity.strip(), type))
    else:
        cursor.execute(
            'INSERT INTO entities(did, entity, type) VALUES({0}, "{1}", "{2}")'.format(did, entity.strip(), type))

