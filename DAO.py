# ######################################################### Data Access Objects:    DAO
# All of these are meant to be singletons
from DTO import *




class _Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
               INSERT INTO vaccines (id, date,supplier,quantity) VALUES (?, ?,?,?)
           """, [vaccine.id, vaccine.date, vaccine.supplier, vaccine.quantity])

    def find(self, vaccine_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM vaccines WHERE id = ?
        """, [vaccine_id])

        return Vaccine(*c.fetchone())

    def pull_the_oldest(self):  # david this function help for your impl
        c = self._conn.cursor()

        c.execute("""SELECT * FROM vaccines
        ORDER BY date(date)""")

        ans = Vaccine(*c.fetchone())
        return ans

    def update_quantity(self, id, amount):  # david this function help for your impl
        c = self._conn.cursor()
        tmp = self.find(id)
        c.execute(""" UPDATE vaccines
             SET quantity = ? 
             WHERE id = ?""", [tmp.quantity - amount, id])

    def remove(self,id):
        c = self._conn.cursor()
        c.execute(""" DELETE FROM vaccines WHERE id = ? """, [id])

    def maxId(self):
        c = self._conn.cursor()
        c.execute("SELECT MAX(id) FROM vaccines")
        return c.fetchone()[0]

class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                INSERT INTO suppliers (id,name,logistic) VALUES (?,?, ?)
        """, [supplier.id, supplier.name, supplier.logistic])

    def find(self,id):
        c = self._conn.cursor()
        c.execute("""
                SELECT * FROM suppliers WHERE id = ?
            """, [id])

        return Supplier(*c.fetchone())

    def findByName(self,name):
        c = self._conn.cursor()
        c.execute("""
            SELECT * From suppliers where name = ?
        """, [name])
        return Supplier(*c.fetchone())



class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
            INSERT INTO clinics (id,location, demand, logistic) VALUES (?, ?, ?, ?)
        """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM clinics WHERE id = ? 
        """, [id])

        return Clinic(*c.fetchone())

    def findByLocation(self,location):
        c = self._conn.cursor()
        c.execute("""
                    SELECT * FROM clinics WHERE location = ?
                """, [location])
        # c.execute("SELECT * FROM Clinics")
        # list = c.fetchall()
        #print("line 98, find by Location:" + list)
        list = c.fetchone()
        return Clinic(*list)

    def find_logistic_id_by_location(self,location):
        c = self._conn.cursor()
        c.execute("""
            SELECT logistic FROM clinics WHERE location = ?
        """,[location])
        return c.fetchone()

    def update_demand(self, location, num):  # david this function help for your impl
        c = self._conn.cursor()
        tmp = self.findByLocation(location)
        c.execute(""" UPDATE clinics
             SET demand = ? 
             WHERE location = ?""", [tmp.demand - num, location])


class _Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""
            INSERT INTO logistics (id,name,count_sent,count_received) VALUES (?, ?, ?,?)
        """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""
            SELECT * FROM logistics WHERE id = ? 
        """, [id])
        return Logistic(*c.fetchone())

    def update_receive(self, id, amount):  # david this function help for your impl
        c = self._conn.cursor()
        tmp = self.find(id)
        c.execute(""" UPDATE logistics
        SET count_received = ? 
        WHERE id = ?""", [amount + tmp.count_received, id])

    def update_sent(self, id, amount):  # david this function help for your impl
        c = self._conn.cursor()
        tmp = self.find(id)
        c.execute(""" UPDATE logistics
        SET count_sent = ? 
        WHERE id = ?""", [amount + tmp.count_sent, id])