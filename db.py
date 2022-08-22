import logging

import sqlite3 as sl
from sqlite3 import OperationalError
from pathlib import PosixPath

__all__ = []

def handler(func, *args, posthook=None, **kwargs):
    def wrap(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except OperationalError as e:
            logging.warning(f'Suppressing OperationalError {e}')
        finally:
            if posthook != None:
                posthook(*args, **kwargs)
    return wrap

def strip(s):
    return s.replace(';','')

class Driver:
    '''
    Open a new db at `filepath` and initialize schema
    '''
    def __init__(self, filepath=str(PosixPath(__file__).parent/'default.db')):
        self._filepath = filepath
        self._con = sl.connect(self._filepath)

        self._init_db()

    @property
    def con(self):
        return self._con

    def safe_execute(self, s):
        return self.con.execute(s.replace(';','')+';')

    @handler
    def _init_db(self):
        sql = """CREATE TABLE IF NOT EXISTS keytable (
                    id TEXT PRIMARY KEY,
                    data BLOB NOT NULL,
                    iv BLOB NOT NULL,
                    salt BLOB NOT NULL
                );"""
        cur = self.con.execute(sql)

    @handler
    def insert(self, item):
        '''
        item = (id,data,iv,salt)
        '''
        sql = """INSERT INTO keytable (id,data,iv,salt) values (?,?,?,?)"""
        cur = self.con.execute(sql, item)

    @handler
    def select(self, query):
        # cur = self.safe_execute(f"""SELECT {} FROM {} WHERE {} = {}""")
        sql = """SELECT (?) FROM keytable WHERE (?) = (?)"""
        breakpoint()
        cur = self.con.execute(sql, query)
        return cur.fetchone()

    @handler
    def get_user(self, user):
        pass

    @handler
    def update(self):
        # cur = self.safe_execute("""UPDATE (?) SET (?) = (?) WHERE (?) = (?);""")
        pass

    @handler
    def delete(self):
        # cur = self.safe_execute("""DELETE FROM (?) values (?);""")
        pass

__all__ += ['Driver']

if __name__ == '__main__':
    d = Driver(filepath=':memory:')
    d.insert(('cat',b'trash',b'mod',b'initv'))
    breakpoint()
    n = d.select(('*','id','cat'))
    breakpoint()
