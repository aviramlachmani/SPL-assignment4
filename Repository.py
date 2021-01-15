# #################################################### The Repository
import atexit
import sqlite3

from DAO import _Vaccines, _Suppliers, _Clinics, _Logistics


class _Repository:
    def __init__(self):
        self._conn = sqlite3.connect('database.db')
        self.vaccines = _Vaccines(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.clinics = _Clinics(self._conn)
        self.logistics = _Logistics(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def totals(self):
        c = self._conn.cursor()
        totals = [0, 0, 0, 0]

        c.execute("SELECT quantity FROM vaccines")
        list_from_db = c.fetchall()
        for x in list_from_db:
            totals[0] = totals[0] + x[0]

        c.execute("SELECT demand FROM clinics")
        list_from_db = c.fetchall()
        for x in list_from_db:
            totals[1] = totals[1] + x[0]

        c.execute("SELECT count_received, count_sent FROM logistics")
        list_from_db = c.fetchall()
        for x in list_from_db:
            totals[2] = totals[2] + x[0]
            totals[3] = totals[3] + x[1]

        totals = map(str, totals)  # converts each cell from int to str
        return totals

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE vaccines (
            id      INTEGER     PRIMARY KEY,
            date    DATE        NOT NULL,
            supplier INTEGER    NOT NULL,
            quantity INTEGER    NOT NULL, 
            FOREIGN KEY (supplier) REFERENCES Suppliers(id)
        );

        CREATE TABLE suppliers (
            id                 INTEGER     PRIMARY KEY,
            name     TEXT    NOT NULL,
            logistic     INTEGER ,
            FOREIGN KEY (logistic) REFERENCES Logistic(id)
        );

        CREATE TABLE clinics (
            id            INTEGER     PRIMARY KEY ,
            location          TEXT    NOT NULL,
            demand         INTEGER     NOT NULL,
            logistic       INTEGER    NOT NULL
        );

        CREATE TABLE logistics (
            id            INTEGER     PRIMARY KEY ,
            name          TEXT    NOT NULL,
            count_sent    INTEGER     NOT NULL,
            count_received INTEGER NOT NULL 
        );

    """)
        self._conn.commit()


repo = _Repository()
atexit.register(repo._close)
