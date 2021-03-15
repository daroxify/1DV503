import mysql.connector
from mysql.connector import errorcode

### The four functions below creates the different tables.
# Catches exception if the table already exists or if something else goes wrong.
# If the table is created successfully, it will print that it has created.

def create_table_patient(cursor):
    create_patient = "CREATE TABLE `patient` (" \
                    "  `ID` varchar(30) NOT NULL," \
                    "  `name` varchar(50)," \
                    "  `adress` varchar(70)," \
                    "  `contact_number` varchar(50)," \
                    "  `blood_group` varchar(4)," \
                    "  `disease` varchar(10000)," \
                    "  PRIMARY KEY (`ID`)" \
                    ") ENGINE=InnoDB"
    
    try:
        print("Creating table patient.")
        cursor.execute(create_patient)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("The table already exists")
        else:
            print(err.msg)
    else:
        print("Created table patient successfully!")

def create_table_donor(cursor):
    create_donor = "CREATE TABLE `donor` (" \
                "  `ID` varchar(30) NOT NULL," \
                "  `name` varchar(50)," \
                "  `adress` varchar(70)," \
                "  `contact_number` varchar(50)," \
                "  `blood_group` varchar(4)," \
                "  `medical_report` varchar(10000),"\
                "  PRIMARY KEY (`ID`)" \
                ") ENGINE=InnoDB"

    try:
        print("Creating table donor.")
        cursor.execute(create_donor)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("The table already exists")
        else:
            print(err.msg)
    else:
        print("Created table donor successfully!")

def create_table_blood(cursor):
    create_blood = "CREATE TABLE `blood` (" \
                "  `blood_ID` varchar(30) NOT NULL," \
                "  `donatedby_ID` varchar(30) NOT NULL," \
                "  `givento_ID` varchar(30)," \
                "  `blood_bank` varchar(50) NOT NULL," \
                "  PRIMARY KEY (`blood_ID`)" \
                ") ENGINE=InnoDB"
#"  FOREIGN KEY (`donatedby_ID`) REFERENCES donor(`ID`)," \
#"  FOREIGN KEY (`givento_ID`) REFERENCES patient(`ID`)" \
#"  FOREIGN KEY (`blood_bank`) REFERENCES bloodbank(`name`)"\
    
    try:
        print("Creating table blood.")
        cursor.execute(create_blood)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("The table already exists")
        else:
            print(err.msg)
    else:
        print("Created table blood successfully!")

def create_table_bloodbank(cursor):
    create_bloodbank = "CREATE TABLE `bloodbank` ("\
                    "  `name` varchar(50) NOT NULL," \
                    "  `adress` varchar(70)," \
                    "  PRIMARY KEY (`name`)" \
                    ") ENGINE=InnoDB"
    try:
        print("Creating table bloodbank.")
        cursor.execute(create_bloodbank)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("The table already exists")
        else:
            print(err.msg)
    else:
        print("Created table bloodbank successfully!")