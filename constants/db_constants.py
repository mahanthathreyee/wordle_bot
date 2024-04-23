#region Database
DB_HOST     = 'localhost'
DB_USER     = 'wordle_bot'
DB_PASSWORD = 'abcd1234'
DB_NAME     = 'wordle'
#endregion

#region DB Process Map Key
DB_KEY_INSERT_WORD_INFO          = 'INSERT_WORD_INFO'
DB_KEY_INSERT_SECOND_WORD_STATUS = 'INSERT_SECOND_WORD_STATUS'
DB_KEY_UPDATE_SECOND_WORD_STATUS = 'UPDATE_SECOND_WORD_STATUS'
#endregion

#region SQL Queries
# First Level Table
INSERT_FIRST_LEVEL_INFO_GAIN  = 'INSERT INTO first_level_info_gain (word, info_gain) \
                                    VALUES (%s, %s) ON CONFLICT DO NOTHING;'
SELECT_FIRST_WORD_INFO        = 'SELECT * FROM first_level_info_gain WHERE word=%s;'
SELECT_FIRST_WORD_MAX_INFO    = 'SELECT * FROM first_level_info_gain ORDER BY info_gain DESC LIMIT %s;'

# Second Level Table
INSERT_SECOND_LEVEL_INFO_GAIN = 'INSERT INTO second_level_info_gain (word, info_gain, parent_id) \
                                    VALUES (%s, %s, %s) ON CONFLICT DO NOTHING;'
SELECT_SECOND_WORD_INFO       = 'SELECT * FROM second_level_info_gain WHERE word=%s AND parent_id=%s;'

# Second Level Status Table
INSERT_SECOND_WORD_STATUS    = 'INSERT INTO second_level_word_status (word_id) \
                                    VALUES (%s) ON CONFLICT DO NOTHING;'
UPDATE_SECOND_WORD_STATUS    = 'UPDATE second_level_word_status SET word_status=%s WHERE word_id=%s;'
SELECT_SECOND_WORD_STATUS    = 'SELECT * FROM second_level_word_status WHERE word_id=%s;'
#endregion
