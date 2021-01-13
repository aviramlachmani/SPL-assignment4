##################################################### The Repository
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

    def create_tables(self):
        self._conn.executescript("""
        CREATE TABLE Vaccines (
            id      INTEGER     PRIMARY KEY,
            date    DATE        NOT NULL,
            supplier INTEGER            ,
            quantity INTEGER    NOT NULL, 
            FOREIGN KEY (supplier) REFERENCES Suppliers(id)
        );

        CREATE TABLE Suppliers (
            id                 INTEGER     PRIMARY KEY,
            name     TEXT    NOT NULL,
            logistic     INTEGER ,
            FOREIGN KEY (logistic) REFERENCES Logistic(id)
        );

        CREATE TABLE Clinics (
            id            INTEGER     PRIMARY KEY ,
            location          TEXT    NOT NULL,
            demand         INTEGER     NOT NULL

        );

        CREATE TABLE Logistics (
            id            INTEGER     PRIMARY KEY ,
            name          TEXT    NOT NULL,
            count_Sent    INTEGER     NOT NULL,
            count_received INTEGER NOT NULL 
        );

    """)
        self._conn.commit()


repo = _Repository()
atexit.register(repo._close)
