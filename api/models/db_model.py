

import sqlite3

class DB_Model:
    def __init__(self):
        self.conn = sqlite3.connect('../vend.db')

    def query_db_for_list(self, query:str, args=(), one=False):
        # Solution from https://stackoverflow.com/a/3287775/2747620
        cur = self.conn.cursor()
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
        self.conn.commit()
        cur.close()
        return (r[0] if r else None) if one else r

    def query_db_as_is(self,query:str):
        c = self.conn.cursor()
        c.execute(query)
        r = c.fetchall()
        self.conn.commit()
        c.close()
        return r