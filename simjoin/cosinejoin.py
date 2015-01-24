from collections import Counter
import itertools as it

import util as ut

import pandas as pd
import numpy as np

class CosineSimilarityJoin():
    """ Class used to do a similarity join between list(s) of strings (records)
    
    This class can be used to find similar records, either:
    1. Between two lists R and S: for each record in R find all similar records
       in S, or
    2. Within a single list R: foreach record in R, find all similar records 
       in R.

    Similarity in this class is definded as the cosine distance between records.
    
    Each record is represented in vector space by tokenizing into q-grams.
    The cosine distances are calculated in the vector representation. 

    For efficiency reasons there is an option to approximate the join result.
    When approximating (the default) larger inputs can be processed due to 
    a lower memory food print.

    The amount of memory required is proportional to number of records in the 
    input, the length of each record, but also on many similar records exist 
    between the inputs.

    """
    def __init__(self, approximate=True, q=3):
        """ Configure the join 

        Args:
          approximate (bool): whether or not to approximate the result of the
                              join.
          q (int): the size of q-grams when tokenizing.

        """
        self._approximate = approximate
        self._q = q

    def prepare_join(self, R, S):
        """ Compute the similarity join between R and S. 
        
        Args:
          R: (list/generator): contains the records for one list
          S: (list/generator): contains the records for other list

        """
        self.R_df = pd.DataFrame(R, columns=['value']).dropna()
        self.S_df = pd.DataFrame(S, columns=['value']).dropna()

        R_tf_idf = self._tf_idf(self.R_df, self._approximate)
        S_tf_idf = self._tf_idf(self.S_df, self._approximate)

        expanded = R_tf_idf.merge(S_tf_idf, on='qgram')
        expanded = expanded.sort(columns=['docid_x', 'docid_y'])
        self._records = expanded.to_records(index=False) 

    def prepare_self_join(self, D):
        """ Convience method, same as prepare_join(list1, list1). """
        R, S = ((w for w in D_) for D_ in it.tee(D))
        prepare_join(R, S)

    def results(self, threshold):
        """ Yields a generator over the join results """
        for (R_id, S_id), d in self._reduce_groups(self._records, threshold):
            yield self.R_df.iloc[R_id,0], self.S_df.iloc[S_id,0], d 

    def _q_grams_from_df(self, df):
        values = df.to_records()
        qgrams = [(i,qgram, count) 
                  for i, value in values 
                  for qgram, count in 
                      Counter(ut.q_grams(value, q=self._q)).items()]
        df = pd.DataFrame(qgrams, columns=['docid', 'qgram', 'docfreq'])
        df['docid'] = df['docid'].astype('int32')
        return df

    def _idf(self, df_qgram, doc_cnt):  
        idf = df_qgram[['qgram']].groupby('qgram', sort=False).count()
        idf['qgram'] = np.log(doc_cnt * 1.0 / idf['qgram'])
        idf = pd.DataFrame(idf).rename(columns={'qgram':'idf'})
        return idf.reset_index()

    def _discard_qgrams(self, tf_idf_frame, keep=0.50):
        discard = int(tf_idf_frame.shape[0] * (1-keep))
        return tf_idf_frame.sort(columns='tfidf').iloc[discard:]

    def _tf_idf(self, df,  discard_freq_qgrams, tf_mode='frequency'):
        tf_frame = self._q_grams_from_df(df)
        idf_frame = self._idf(tf_frame, df.shape[0] * 1.0)
        
        tf_idf = tf_frame.merge(idf_frame)
        if tf_mode == 'frequency':
            tf_idf['tfidf'] = (tf_idf['docfreq'] * tf_idf['idf'])
        else:
            tf_idf['tfidf'] = tf_idf['idf']
        tf_idf['tfidf'] = self._to_unit(tf_idf)
        tf_idf = self._discard_qgrams(tf_idf) if discard_freq_qgrams else tf_idf
        
        return tf_idf[['docid', 'qgram', 'tfidf']]

    def _to_unit(self, df):
        g = df[['docid', 'tfidf']].groupby('docid', sort=False)['tfidf']
        return g.apply(lambda x: (x/np.linalg.norm(x)).astype('float16'))
        
    def _reduce_groups(self, expanded, threshold):
        rowiter = ut.PeekableIterator((r for r in expanded))
        while rowiter.has_next():
            a = np.array(list(self._take_group(rowiter)))
            d = np.dot(a[:,2], a[:,3])
            if d > threshold:
                yield a[0,:2].astype(int), d

    def _take_group(self, rowiter):
        for row in rowiter:
            yield (row[0],row[3],row[2],row[4],)
            if rowiter.has_next():
                nxt = rowiter.peek()
                if not (nxt[0] == row[0] and nxt[3] == row[3]):
                    break
