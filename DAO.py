########################################################## Data Access Objects:    DAO
# All of these are meant to be singletons
from DTO import *


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