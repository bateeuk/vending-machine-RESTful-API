
# Import the db system
import sqlite3

class DB_Model:
    """
    Gatekeeper to the database

    ...

    Attributes
    ----------
    conn : sqlite3.Connection
        An instance of the sqlite3.Connection class (for handing sqlite3 database connections)

    Methods
    -------
    query_db_for_list(self, query:str, args=(), one=False)
        Queries the database and turns the query results into a list
    query_db_as_is(self,query:str)
        Queries the database and returns the results
    """
    def __init__(self):
        """ Initialises the sqlite3.Connection """
        self.conn = sqlite3.connect('../vend.db')

    def query_db_for_list(self, query:str, args=(), one=False):
        """
        Queries the database and turns the query results into a list

        if `one` is not provided, it is set to False by default
        if `args` is not provided, it is set to an empty list by default
        
        Parameters
        ----------
        query : str
            The SQL query string
        args : list, optional
            Any arguements to customise the query
        one : bool, optional
            If only one argument is provided

        Returns
        ----------
        list
            a list of the results from the query.

        """
        # Solution from https://stackoverflow.com/a/3287775/2747620
        cur = self.conn.cursor()
        cur.execute(query, args)
        r = [dict((cur.description[i][0], value) \
                for i, value in enumerate(row)) for row in cur.fetchall()]
        self.conn.commit()
        cur.close()
        return (r[0] if r else None) if one else r

    def query_db_as_is(self,query:str):
        """
        Queries the database and returns the results
        
        Parameters
        ----------
        query : str
            The SQL query string

        Returns
        ----------
        any
            the results from the query.

        """
        c = self.conn.cursor()
        c.execute(query)
        r = c.fetchall()
        self.conn.commit()
        c.close()
        return r