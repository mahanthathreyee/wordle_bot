import psycopg2

from constants.db_constants import *
from constants.app_constants import *

class WordleDB:
    _db_conn = None

    def __init__(self, readonly: bool=True) -> None:
        self._db_conn = WordleDB._configure_connection()
        if readonly:
            self._db_conn.set_session(readonly=True)
    
    def insert_word_info(self, word: str, info_gain: float, info_level: int, parent_id: int=None):
        with self._db_conn.cursor() as cursor:
            if info_level == 1:
                cursor.execute(
                    query=INSERT_FIRST_LEVEL_INFO_GAIN,
                    vars=(word, info_gain)
                )
            else:
                cursor.execute(
                    query=INSERT_SECOND_LEVEL_INFO_GAIN,
                    vars=(word, info_gain, parent_id)
                )
            self._db_conn.commit()

    #region First Word Table
    def get_first_word_info(self, word: str):
        res = None
        with self._db_conn.cursor() as cursor:
            cursor.execute(
                query=SELECT_FIRST_WORD_INFO,
                vars=(word, )
            )
            res = cursor.fetchone()
            self._db_conn.commit()
        return res
    #endregion

    #region Second Word Table
    def get_second_word_info(self, word_pattern: str, parent_id: int):
        res = None
        with self._db_conn.cursor() as cursor:
            cursor.execute(
                query=SELECT_SECOND_WORD_INFO,
                vars=(word_pattern, parent_id)
            )
            res = cursor.fetchone()
            self._db_conn.commit()
        return res
    #endregion

    #region Second Word Status Table
    def insert_second_word_status(self, word_id: int):
        with self._db_conn.cursor() as cursor:
            cursor.execute(
                query=INSERT_SECOND_WORD_STATUS,
                vars=(word_id,)
            )
            self._db_conn.commit()

    def update_second_word_status(self, word_id: int, word_status: bool):
        with self._db_conn.cursor() as cursor:
            cursor.execute(
                query=UPDATE_SECOND_WORD_STATUS,
                vars=(word_id, word_status)
            )
            self._db_conn.commit()

    def get_second_word_status(self, word_id: int):
        res = None
        with self._db_conn.cursor() as cursor:
            cursor.execute(
                query=SELECT_SECOND_WORD_STATUS,
                vars=(word_id,)
            )
            res = cursor.fetchone()
            self._db_conn.commit()
        return res
    #endregion
        
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
