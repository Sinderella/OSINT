import pandas as pd
import numpy as np
import sqlite3

from pandas import DataFrame, Series


class Analyser(object):
    def __init__(self, db_name):
        super(Analyser, self).__init__()
        self.db_name = db_name
        self.cur_db = sqlite3.connect(self.db_name + '/documents.db')
        self.cursor = self.cur_db.cursor()

    def analyse(self):
        print(self.compute_tf_idf())

    def compute_tf_idf(self):
        # Find total number of document
        results = self.cursor.execute('SELECT seq FROM sqlite_sequence WHERE name=\'{}\''.format('documents'))
        tmp = results.fetchone()
        total_doc = tmp[0]

        results = self.cursor.execute('SELECT did, type, entity FROM entities')
        tmp = results.fetchall()
        df = DataFrame(tmp, columns=['did', 'e_type', 'entity'])

        doc_t_df = df.drop_duplicates().groupby('entity').size()

        results = self.cursor.execute('SELECT did, total_word FROM documents')
        tmp = results.fetchall()
        df2 = DataFrame(tmp, columns=['did', 'total_word'])

        tmp = df[['did', 'entity']].groupby(['did', 'entity']).size().reset_index()
        tmp.rename(columns={0: 'term_freq'}, inplace=True)

        tf_idf_list = []

        for row in tmp.iterrows():
            values = row[1]
            did = values[0]
            entity = values[1]
            term_freq = values[2]
            total_word = df2[df2['did'] == did]['total_word'].get_values()[0]
            tf = float(term_freq) / total_word
            doc_t = doc_t_df.get_value(entity)
            idf = np.log(total_doc / doc_t)
            tf_idf = tf * idf
            tf_idf_list.append([did, entity, tf_idf])

        tf_idf_df = DataFrame(tf_idf_list, columns=['did', 'entity', 'tf_idf'])
        return tf_idf_df
