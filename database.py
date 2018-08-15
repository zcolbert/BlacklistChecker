import sqlite3


class DBConnection:
    def __init__(self, db_addr):
        self.conn = None
        self.cursor = None

    def connect(self):
        pass


class SQLite3DBConnection(DBConnection):
    pass


class DBTable:
    def __init__(self):
        self.name = ''
        self.fields = []


class DBTableField:
    def __init__(self):
        self.name = ''
        self.type = ''


def test():
    # use :memory: to create connection in ram
    conn = sqlite3.connect('test.db')

    cursor = conn.cursor()

    table = DBTable('accounts')
    table.fields = [DBTableField('id, INTEGER')]
    
    cursor.execute('''CREATE TABLE accounts (id INTEGER PRIMARY KEY, name TEXT)''')

    conn.commit()
    conn.close()


if __name__ == '__main__':
    test()