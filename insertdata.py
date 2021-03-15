import mysql.connector
import csv
from mysql.connector import errorcode


### The method reads the data from the given file
#   and returns a ... 
def read_data_from_file(path):
    l = []
    count = 0
    try:
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = '|')
            for row in reader:
                if count != 0: # skipping 1st row in file
                    values = []
                    for value in row:
                        if(value == ''):
                            value = None
                        values.append(value)
                    l.append(tuple(values))
                count += 1
    except FileNotFoundError:
        print("File: " + path + " not found")
        exit(1)
    return l
                


def insert_into_tables(cnx, path, insert_data):
    cursor = cnx.cursor()
    data = read_data_from_file(path)
    try:
        for t in data:
            cursor.execute(insert_data, t)
    except mysql.connector.Error as err:
        print("HÄR: ", err.msg)
    else:
        cnx.commit()
    