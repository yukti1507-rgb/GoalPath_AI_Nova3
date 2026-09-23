from db import get_connection
from users import set_token

conn = get_connection()

def delete_one_user(conn, name):
    cur = conn.cursor()
    sql = 'DELETE FROM users WHERE username = ?'
    param = (name,)
    cur.execute(sql, param)
    conn.commit()

def delete_db(conn):
    cur = conn.cursor()
    cur.execute("DELETE FROM users")
    conn.commit()


