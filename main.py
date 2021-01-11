import sqlite3
import atexit
import sys


def insert_data(table, path):
    with open(path, 'r') as inputFile:
        size = inputFile.readline().split(",")
        for i in range(0, int(size[0])):
            list1 = inputFile.readline().split(",")
            table.vaccines.insert(Vaccine(int(list1[0]), list1[1], int(list1[2]), int(list1[3])))
        for i in range(0, int(size[1])):
            list1 = inputFile.readline().split(",")
            table.suppliers.insert(Supplier(int(list1[0]), list1[1], int(list1[2])))
        for i in range(0, int(size[2])):
            list1 = inputFile.readline().split(",")
            table.clinics.insert(Clinic(int(list1[0]), list1[1], int(list1[2])))
        for i in range(0, int(size[3])):
            list1 = inputFile.readline().split(",")
            table.logistics.insert(Logistic(int(list1[0]), list1[1], int(list1[2]), int(list1[3])))


########################################################## Data Access Objects:    DAO
# All of these are meant to be singletons
class _Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
               INSERT INTO Vaccines (id, date,supplier,quantity) VALUES (?, ?,?,?)
           """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def find(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM Vaccines WHERE id = ?
        """, [vaccine_id])

        return Vaccine(*c.fetchone())

    def pool_the_oldest(self):  # david this function help for your impl
        c = self._conn.cursor()
        c.execute("""SELECT * FROM Vaccines
        ORDER BY DATE""")
        ans = Vaccine(*c.fetchone())
        c.execute(""" DELETE FROM Vaccines WHERE id = ? """, [ans.id])
        return ans


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                INSERT INTO Suppliers (id,name,logistic) VALUES (?,?, ?)
        """, [supplier.id, supplier.name, supplier.logistic])

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""
                SELECT * FROM Suppliers WHERE id = ?
            """, [id])

        return Supplier(*c.fetchone())


class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
            INSERT INTO Clinics (id,location, demand) VALUES (?, ?, ?)
        """, [clinic.id, clinic.location, clinic.demand])

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM Clinics WHERE id = ? 
        """, [id])

        return Clinic(*c.fetchone())

    def update_demand(self, location, num):  # david this function help for your impl
        c = self._conn.cursor()
        tmp = self.find(id)
        c.execute(""" UPDATE Clinics
             SET demand = ? 
             WHERE location = ?""", [tmp.demand + num, location])


class _Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""
            INSERT INTO Logistics (id,name,count_sent,count_received) VALUES (?, ?, ?,?)
        """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM Logistics WHERE id = ? 
        """, [id])

        return Logistic(*c.fetchone())

    def update_receive(self, id, num):  # david this function help for your impl
        c = self._conn.cursor()
        tmp = self.find(id)
        c.execute(""" UPDATE Logistics
        SET count_receive = ? 
        WHERE id = ?""", [num + tmp.count_received, id])

    def update_sent(self, id, num):  # david this function help for your impl
        c = self._conn.cursor()
        tmp = self.find(id)
        c.execute(""" UPDATE Logistics
        SET count_sent = ? 
        WHERE id = ?""", [num + tmp.count_sent, id])


################################################################ Data Transfer Objects: DTO
class Vaccine:
    def __init__(self, id, date, supplier, quantity):
        self.id = id
        self.date = date
        self.supplier = supplier
        self.quantity = quantity


class Supplier:
    def __init__(self, id, name, logistic):
        self.id = id
        self.name = name
        self.logistic = logistic


class Clinic:
    def __init__(self, id, location, demand):
        self.id = id
        self.location = location
        self.demand = demand


class Logistic:
    def __init__(self, id, name, count_sent, count_received):
        self.id = id
        self.name = name
        self.count_sent = count_sent
        self.count_received = count_received


##################################################### The Repository
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


def main(args):
    repo.create_tables()
    insert_data(repo, args[2])
    print(repo.logistics.find(1).name)  # test
    print(repo.clinics.find(4).location)  # test
    print(repo.vaccines.pool_the_oldest().id)  # test
    print(repo.vaccines.find(2).date)  # test


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv)
