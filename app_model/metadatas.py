import pandas as pd
import sqlite3

#populates a db with contents from datasets_metadata.csv
def migrate_datasets_metadata(conn):
    data = pd. read_csv("DATA/datasets_metadata.csv")
    data.to_sql('datasets_metadata', conn, if_exists='replace', index=False)
    conn.close()

def get_all_datasets_metadata(conn):
    sql = 'SELECT * FROM datasets_metadata'
    data = pd.read_sql(sql, conn)
    return (data)