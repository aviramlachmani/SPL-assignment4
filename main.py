import atexit
import sqlite3
import sys
from DTO import *
from Repository import repo


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




def main(args):
    repo.create_tables()
    insert_data(repo, args[1])

    print(repo.logistics.find(1).name)  # test
    print(repo.clinics.find(4).location)  # test
    print(repo.vaccines.pool_the_oldest().id)  # test
    print(repo.vaccines.find(2).date)  # test


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv)
