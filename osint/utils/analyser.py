import pandas as pd
import numpy as np
import sqlite3
import json

from pandas import DataFrame, Series

from osint.utils.requesters import Requester


class Analyser(object):
    def __init__(self, db_name):
        super(Analyser, self).__init__()
        self.db_name = db_name
        self.cur_db = sqlite3.connect(self.db_name + '/documents.db')
        self.cursor = self.cur_db.cursor()

        self.google_api_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}"

        # https://developers.google.com/maps/documentation/geocoding/intro#Types
        self.location_score_chart = {
            'type_10': ['street_address', 'subpremise', 'airport', 'park', 'point_of_interest'],
            'type_9': ['intersection', 'neighborhood', 'premise', 'postal_code'],
            'type_8': ['route', 'administrative_area_level_5', 'sublocality_level_5', 'locality', 'ward'],
            'type_7': ['administrative_area_level_4', 'sublocality_level_4'],
            'type_6': ['administrative_area_level_3', 'sublocality_level_3'],
            'type_5': ['political', 'administrative_area_level_2', 'sublocality_level_2'],
            'type_4': ['administrative_area_level_1', 'sublocality_level_1'],
            'type_3': ['country']}

    def analyse(self):
        combined_df = DataFrame(columns=['e_type', 'entity', 'score'])

        frequency_df = self.compute_frequency()
        tf_idf_df = self.compute_tf_idf()
        ambiguity_df = self.compute_ambiguity()

        combined_df = frequency_df.copy()
        del combined_df['term_freq']
        combined_df['score'] = 0
        combined_df = self.normalise_and_combine(frequency_df, combined_df)
        combined_df = self.normalise_and_combine(tf_idf_df, combined_df)
        combined_df = self.normalise_and_combine(ambiguity_df, combined_df)

        combined_df['score'] = combined_df['score'].apply(lambda x: x/3)

        print(self.get_category_top5(combined_df, 'score'))

        # print('Frequency:\n{}'.format(self.compute_frequency()))
        # print('TF.IDF:\n{}'.format(self.compute_tf_idf()))
        # print('Ambiguity:\n{}'.format(self.compute_ambiguity()))

    @staticmethod
    def normalise_and_combine(src_df, dst_df):
        column = None
        lower_bound = 0
        upper_bound = 0
        if 'term_freq' in src_df.columns:
            column = 'term_freq'
        elif 'tf_idf' in src_df.columns:
            column = 'tf_idf'
        elif 'score' in src_df.columns:
            column = 'score'
        lower_bound = float(src_df[column].min())
        upper_bound = float(src_df[column].max())
        src_df[column] = src_df[column].apply(lambda x: (x - lower_bound)/(upper_bound - lower_bound))
        src_df.rename(columns={column: 'score'}, inplace=True)
        output = pd.merge(dst_df, src_df, on=["e_type", "entity"])
        output['score'] = output['score_x'] + output['score_y']
        del output['score_x']
        del output['score_y']
        return output

    @staticmethod
    def get_category_top5(df, sort_by, ascending=False):
        result = None
        for e_type in df['e_type'].unique():
            if result is None:
                result = df[df['e_type'] == e_type].sort_values(sort_by, ascending=ascending).iloc[0:5]
            else:
                result = pd.concat([result, df[df['e_type'] == e_type]
                                   .sort_values(sort_by, ascending=ascending).iloc[0:5]])

        return result.sort_values(['e_type', sort_by], ascending=[not ascending, ascending], ).to_string(index=False)

    def compute_ambiguity(self):
        results = self.cursor.execute('SELECT type, entity FROM entities')
        tmp = results.fetchall()
        freq_df = DataFrame(tmp, columns=['e_type', 'entity'])
        freq_df['score'] = 1
        freq_df = freq_df.drop_duplicates()
        result_computed_location = self._compute_location_ambiguity(freq_df)
        result_computed_name = self._compute_name_ambiguity(result_computed_location)
        return result_computed_name

    def _compute_location_ambiguity(self, df):
        location_df = df[df['e_type'] == 'Location']
        location_se = location_df.drop_duplicates()['entity']
        for location_name in location_se.get_values():
            url = self.google_api_url.format(location_name)
            req = Requester()
            res = req.get(url)
            api_result = json.loads(res.content)
            if api_result['status'] != 'OK':
                continue
            location_types = api_result['results'][0]['address_components'][0]['types']
            location_score = max(self.__measure_location_ambiguity(location_type) for location_type in location_types)
            location_index = location_se[location_se == location_name].index[0]
            df.set_value(location_index, 'score', location_score)
        return df

    def __measure_location_ambiguity(self, location):
        score = 0
        for score_type in self.location_score_chart:
            if location in self.location_score_chart[score_type]:
                score = int(score_type.split('_')[-1])
                break
        return score

    def _compute_name_ambiguity(self, df):
        name_df = df[df['e_type'] == 'Name']
        name_se = name_df.drop_duplicates()['entity']
        for name_name in name_se.get_values():
            name_score = self.__compute_name_ambiguity(name_name)
            name_index = name_se[name_se == name_name].index[0]
            df.set_value(name_index, 'score', name_score)
        return df

    @staticmethod
    def __compute_name_ambiguity(name):
        score = 0
        if len(name.split(' ')) > 1:
            score = 1
        return score

    def compute_frequency(self):
        return self._compute_frequency()

    def _compute_frequency(self):
        results = self.cursor.execute('SELECT did, type, entity FROM entities')
        tmp = results.fetchall()
        df = DataFrame(tmp, columns=['did', 'e_type', 'entity'])
        tmp = df.groupby(['e_type', 'entity']).size().reset_index()
        tmp.rename(columns={0: 'term_freq'}, inplace=True)

        return tmp

    def compute_tf_idf(self):
        # Find total number of document
        results = self.cursor.execute('SELECT seq FROM sqlite_sequence WHERE name=\'{}\''.format('documents'))
        tmp = results.fetchone()
        total_doc = tmp[0]

        results = self.cursor.execute('SELECT did, type, entity FROM entities')
        tmp = results.fetchall()
        df = DataFrame(tmp, columns=['did', 'e_type', 'entity'])

        base_df = df[['e_type', 'entity']]
        base_df = base_df.drop_duplicates()

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
            tf_idf_list.append([entity, tf_idf])

        tf_idf_df = DataFrame(tf_idf_list, columns=['entity', 'tf_idf'])
        tf_idf_df = tf_idf_df.groupby('entity').agg('sum')

        base_df.loc[:, 'tf_idf'] = base_df['entity'].apply(lambda x: tf_idf_df['tf_idf'][x])

        return base_df

if __name__ == '__main__':
    a = Analyser('/Users/Sinderella/PycharmProjects/OSINT/db/20160124_203417')
    a.analyse()
