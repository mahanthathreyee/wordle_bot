#region Database
DB_HOST     = 'localhost'
DB_USER     = 'wordle_bot'
DB_PASSWORD = 'abcd1234'
DB_NAME     = 'wordle'
#endregion

#region DB Process Map Key
DB_KEY_INSERT_PREFIX          = 'INSERT_WORD_INFO'
#endregion

#region SQL Queries
# First Level Table
QUERY_INSERT_PREFIX_INFO_GAIN = 'INSERT INTO prefix_info_gain (prefix, word, info_gain) \
                                                       VALUES (%s,       %s,        %s) ON CONFLICT DO NOTHING;'
QUERY_SELECT_PREFIX_INFO_GAIN = 'SELECT word, info_gain FROM prefix_info_gain \
                                                        WHERE prefix=%s;'
#endregion
