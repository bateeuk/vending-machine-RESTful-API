
# db interaction
import sqlite3

class Change_Model():
    def __init__(self):
        self.conn = sqlite3.connect('../vend.db')
        
    def get_change(self):
        change = list()
        if(self.conn is not None):
            c = self.conn.cursor()
            c.execute('SELECT coin, quantity FROM change_float')
            change = c.fetchall()
            c.close()
        return change
