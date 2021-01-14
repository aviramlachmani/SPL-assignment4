import atexit
import sqlite3
import sys
from DTO import *
from Repository import repo


def insert_data(database, config):
    with open(config, 'r') as inputFile:
        size = inputFile.readline().split(",")

        for i in range(0, int(size[0])):
            list1 = inputFile.readline().split(",")
            database.vaccines.insert(Vaccine(int(list1[0]), list1[1], int(list1[2]), int(list1[3])))

        for i in range(0, int(size[1])):
            list1 = inputFile.readline().split(",")
            database.suppliers.insert(Supplier(int(list1[0]), list1[1], int(list1[2])))

        for i in range(0, int(size[2])):
            list1 = inputFile.readline().split(",")
            database.clinics.insert(Clinic(list1[0], list1[1], int(list1[2]), int(list1[3])))

        for i in range(0, int(size[3])):
            list1 = inputFile.readline().split(",")
            database.logistics.insert(Logistic(int(list1[0]), list1[1], int(list1[2]), int(list1[3])))

def execute(database, orders):
    numberOflinesExecuted =0 #TODO debugging
    with open(orders,'r') as inputFile:
        line = inputFile.readline().split(",")
        while len(line)>1: #TODO check what happens where there is no more lines on the file
            if len(line) == 2: send(database, *line)
            elif len(line) == 3: receive(database, *line)
            else:
                print("Incorrect line length at orders:" +",".join(line) +" length: "+ str(len(line)) +"""
                number of lines executed by now:""" + str(numberOflinesExecuted))
                break
            line = inputFile.readline().split(",")
            numberOflinesExecuted +=1

def receive(database, name, amount, date):
    supplier = database.suppliers.findByName(name)
    newId = database.vaccines.maxId() +1
    database.vaccines.insert(Vaccine(newId, date, int(supplier.id),int(amount)))
    database.logistics.update_receive(int(supplier.logistic),int(amount))

def send(database, location, amount):
    amount = int(amount)
    database.clinics.update_demand(location,-1*amount) #remove fron the demand of the clinic todo if we only use it for subtraction , change update_demand
    logisticId = database.clinics.find_logistic_id_by_location(location)[0] #pull the logistic id from clinic
    database.logistics.update_sent(logisticId,amount) #update logistic sent

    while amount > 0:  #remove the amount fron inventory
        vaccine = database.vaccines.pull_the_oldest()
        if vaccine.quantity > amount:
            database.vaccines.update_quantity(vaccine.id,amount)
            amount = 0
        else:
            amount = amount - vaccine.quantity
            database.vaccines.remove(vaccine.id)




def main(args):
    repo.create_tables()
    insert_data(repo, args[1])
    execute(repo,args[2])
    repo._close() #TODO ask aviram if i need to call this or it is automatically called
    # print(repo.logistics.find(1).name)  # test
    # print(repo.clinics.find(4).location)  # test
    # print(repo.vaccines.pool_the_oldest().id)  # test
    # print(repo.vaccines.find(2).date)  # test


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv)
