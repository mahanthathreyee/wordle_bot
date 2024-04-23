import psycopg2

from constants.db_constants import *
from constants.app_constants import *

class WordleDB:
    _db_conn = None

    def __init__(self) -> None:
        self._db_conn = WordleDB._configure_connection()
    
    def insert_prefix(self, prefix: str, word: str, info_gain: float):
        with self._db_conn.cursor() as cursor:
            cursor.execute(
                query=QUERY_INSERT_PREFIX_INFO_GAIN,
                vars=(prefix, word, info_gain)
            )
            self._db_conn.commit()

    def get_prefix(self, prefix: str):
        res = None
        with self._db_conn.cursor() as cursor:
            cursor.execute(
                query=QUERY_SELECT_PREFIX_INFO_GAIN,
                vars=(prefix, )
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
