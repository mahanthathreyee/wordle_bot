import psycopg2

from constants.app_constants import *

class WordleDB:
    _db_conn = None

    def __init__(self, readonly: bool=True) -> None:
        self._db_conn = WordleDB._configure_connection()
        if readonly:
            self._db_conn.set_session(readonly=True)
    
    def insert_word_info(self, word: str, info_gain: float, info_level: int):
        with self._db_conn.cursor() as cursor:
            cursor.execute(
                query=INSERT_INFO_GAIN,
                vars=(word, info_gain, info_level)
            )
            self._db_conn.commit()

    def get_word_info(self, word: str):
        res = None
        with self._db_conn.cursor() as cursor:
            cursor.execute(
                query=SELECT_WORD_INFO,
                vars=(word, )
            )
            res = cursor.fetchone()
            self._db_conn.commit()
        return res
        
    def close(self):
        self._db_conn.close()

    #region Internal Methods
    def _configure_connection():
        return psycopg2.connect(
            host=DB_HOST,

            dbname=DB_NAME,
            user=DB_USER, 
            password=DB_PASSWORD
        )
    #endregion
