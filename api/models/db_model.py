import json
# import psycopg2
import sqlite3

class DB_Model:
    def __init__(self):
        self.conn = sqlite3.connect('../vend.db')

    def query_db(self, query, args=(), one=False):
        cur = self.conn.cursor()
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
        cur.close()
        return (r[0] if r else None) if one else r

