# Programming Assignment 2
# Name: Enida Ahmic
# Student ID: ea223qi

import PySimpleGUI as sg
import mysql.connector
import csv
import tables
from insertdata import insert_into_tables
from mysql.connector import errorcode

DB_NAME = 'BloodDonation'

### Creating the database
# Creates database with the name DB_NAME.
# Catches exception if something goes wrong and prints the error.

def create_database(cursor, DB_NAME):
    try:
        cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database {}".format(err))
        exit(1)

### Try to connect to database
# Set up a connection, establish a session with MySQL server.
# Catches exception if server is down.

def execute_query(query, cursor):
    try:
        cursor.execute(query)
    except mysql.connector.ProgrammingError as err:
        print("Could not execute query")
        print(err)

## Starting the database and creating tables
try:
    cnx = mysql.connector.connect(user = 'root',
                                    password = 'root',
                                    unix_socket = '/Applications/MAMP/tmp/mysql/mysql.sock')
except mysql.connector.errors.DatabaseError as err:
    print('Could not connect: {}'.format(err))
    exit(1)

cursor = cnx.cursor()

try:
    cursor.execute("Use {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exist".format(DB_NAME))

    if err.errno == errorcode.ER_BAD_DB_ERROR:
        create_database(cursor, DB_NAME)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
        tables.create_table_patient(cursor)
        tables.create_table_donor(cursor)
        tables.create_table_bloodbank(cursor)
        tables.create_table_blood(cursor)
        pathPatient = "/Users/Enida A/Desktop/patient.csv"
        insert_data = "INSERT INTO patient (ID, name, adress, contact_number, blood_group, disease) VALUES (%s, %s, %s, %s, %s, %s)"
        insert_into_tables(cnx, pathPatient, insert_data)
        insert_data = "INSERT INTO donor (ID, name, adress, contact_number, blood_group, medical_report) VALUES (%s, %s, %s, %s, %s, %s)"
        pathDonor = "/Users/Enida A/Desktop/donor.csv"
        insert_into_tables(cnx, pathDonor, insert_data)
        pathBloodBank = "/Users/Enida A/Desktop/blood bank.csv"
        insert_data = "INSERT INTO bloodbank (name, adress) VALUES (%s, %s)"
        insert_into_tables(cnx, pathBloodBank, insert_data)
        pathBlood = "/Users/Enida A/Desktop/blood.csv"
        insert_data = "INSERT INTO blood (blood_ID, donatedby_ID, givento_ID, blood_bank) VALUES (%s, %s, %s, %s)"
        insert_into_tables(cnx, pathBlood, insert_data)
    else:
        print(err)
print("Database started")


### APPLICATION BELOW

def reset():
    window['-VIEW1-'].update(visible=False)
    window['-VIEW2-'].update(visible=False)
    window['-VIEW3-'].update(visible=False)
    window['-VIEW4-'].update(visible=False)
    window['-VIEW5-'].update(visible=False)
    window['-VIEW6-'].update(visible=False)
    window['-VIEW7-'].update(visible=False)
    window['-INPUT-'].update(visible=False)
    window['-OPT3-'].update(visible=False)
    window['-OPT44-'].update(visible=False)
    window['-OPT5-'].update(visible=False)
    window['-OPT6-'].update(visible=False)
    window['-VIEW8-'].update(visible=False)

# Define the window's contents
empty = []
VIEW1 = sg.Text('Click on a donor to see medical report', key='-VIEW1-', visible=False)
VIEW2 = sg.Text('Click on a patient to see disease', key='-VIEW2-', visible=False)
VIEW3 = sg.Text('{:15}{:15}{:15}{:25}{:25}'.format("ID", "Name", "Adress", "Contact Number", "Blood Group"), key='-VIEW3-', visible=False)
VIEW4 = sg.Text('{:20}{:20}{:20}{:20}{:20}'.format("ID", "Name", "Adress", "Contact Number", "Blood Group"), key='-VIEW4-', visible=False)
VIEW5 = sg.Text('{:20}{:20}'.format("Name", "Adress"), key='-VIEW5-', visible=False)
VIEW6 = sg.Text('{:20}{:20}{:20}{:20}'.format("Blood ID", "Donated By ID", "Given To ID", "Blood Bank"), key='-VIEW6-', visible=False)
VIEW7 = sg.Text("ID", key = '-VIEW7-', visible = False)
VIEW8 = sg.Text("Define X: ", key = '-VIEW8-', visible=False)

OPT1 = sg.InputOptionMenu(('Show all data', 'Specific Search'), default_value='Show all data', k='-OPT1-')
OPT2 = sg.InputOptionMenu(('Donor', 'Patient', 'Blood Banks', 'Blood'), default_value='Donor', k='-OPT2-')
OPT3 = sg.InputOptionMenu(('Find donors/patients blood type', \
                        'Find how many bags each blood bank has in stock in each blood group', \
                        'Show information about donor and the blood donated', \
                        'Find blood banks where a specific donor has donated',\
                        'See who has donated blood X times', \
                        'Find who patients donor is' ), k = '-OPT3-', visible=False)
OPT4 = sg.InputOptionMenu(('Donor', 'Patient'), k='-OPT44-', visible=False)
OPT5 = sg.InputOptionMenu(('A', 'B', 'AB', 'O', 'ALL'), k='-OPT5-', visible=False)
OPT6 = sg.InputOptionMenu(('Specific Donor','ALL'), k = '-OPT6-', visible = False)

layout = [
            [OPT1, OPT2, OPT3, OPT5, OPT6],
            [sg.Button('OK', enable_events=True, key='-BUTT-'), OPT4],
            [sg.Text('Search for', key = '-SER-', visible=False), VIEW1, VIEW2],
            [VIEW3, VIEW4, VIEW5, VIEW6, VIEW7, VIEW8],
            [sg.Input(size=(70, 1), enable_events=True, key='-INPUT-', visible=False)],
            [sg.Listbox(empty, size=(150, 20), enable_events=True, key='-LIST-')],
            [sg.Button('Exit')]
          ]

window = sg.Window('Listbox with Search', layout)

# Event Loop
while True:
    event, values = window.read()
    showAll = True

    if event == '-BUTT-':
        reset()
        names = []
        if values['-OPT1-'] == 'Show all data':
            window['-OPT2-'].update(visible=True)
            window['-OPT3-'].update(visible=False)
            showAll = True   
            if values['-OPT2-'] == 'Donor':
                window['-VIEW1-'].update(visible=True)
                window['-VIEW3-'].update(visible=True)
                query = "SELECT * FROM donor"
                execute_query(query, cursor)
                for ID, name, adress, cn, bg, med in cursor:
                    data = "{:15}{:15}{:15}{:25}{:25}".format(ID,name,adress,cn,bg)
                    names.append(data)
                window['-LIST-'].update(names)

            elif values['-OPT2-'] == 'Patient':
                window['-VIEW2-'].update(visible=True)
                window['-VIEW4-'].update(visible=True)
                query = "SELECT * FROM patient"
                execute_query(query, cursor)
                for ID, name, adress, cn,bg, dis in cursor:
                    data = "{:20}{:20}{:20}{:20}{:20}".format(ID,name,adress,cn,bg)
                    names.append(data)
                window['-LIST-'].update(names)

            elif values['-OPT2-'] == 'Blood Banks':
                window['-VIEW5-'].update(visible=True)
                query = "SELECT * FROM bloodbank"
                execute_query(query, cursor)
                for name, adress in cursor:
                    data = "{:30}{:30}".format(name, adress)
                    names.append(data)
                window['-LIST-'].update(names)

            elif values['-OPT2-'] == 'Blood':
                window['-VIEW6-'].update(visible=True)
                query = "SELECT * FROM blood"
                execute_query(query, cursor)
                for blID, donby, givto, blbank in cursor:
                    data = "{:20}{:20}{:20}{:20}".format(blID, donby, str(givto), blbank)
                    names.append(data)
                window['-LIST-'].update(names)
            else:
                window['-LIST-'].update(empty)
        elif values['-OPT1-'] == 'Specific Search':
            showAll = False
            window['-LIST-'].update(empty)
            window['-VIEW1-'].update(visible=False)
            window['-LIST-'].update(empty)
            window['-OPT2-'].update(visible=False)
            window['-OPT3-'].update(visible=True)
            window['-OPT44-'].update(visible=False)
            window['-OPT5-'].update(visible=False)
            window['-VIEW8-'].update(visible=False)

            if values['-OPT3-'] == 'Find donors/patients blood type':
                #OK
                window['-OPT5-'].update(visible=False)
                window['-SER-'].update(visible=False)
                window['-INPUT-'].update(visible=False)
                window['-VIEW7-'].update(visible=False)
                window['-OPT6-'].update(visible = False)
                window['-OPT44-'].update(visible=True)

                if values['-OPT44-'] == 'Donor':
                    window['-SER-'].update(visible=True)
                    window['-INPUT-'].update(visible=True)
                    window['-VIEW7-'].update(visible=True)
                    ID = values['-INPUT-']
                    query = "SELECT ID, name, blood_group FROM donor WHERE ID='" + ID + "'"
                    execute_query(query, cursor)
                    for ID, name, bg in cursor:
                        data = "{:25}{:25}{:25}".format(ID, name, bg)
                        names.append(data)
                    window['-LIST-'].update(names)
                elif values['-OPT44-'] == 'Patient':
                    window['-SER-'].update(visible=True)
                    window['-INPUT-'].update(visible=True)
                    window['-VIEW7-'].update(visible=True)
                    ID = values['-INPUT-']
                    query = "SELECT ID, name, blood_group FROM patient WHERE ID='" + ID + "'"
                    execute_query(query, cursor)
                    for ID, name, bg in cursor:
                        data = "{:25}{:25}{:25}".format(ID, name, bg)
                        names.append(data)
                    window['-LIST-'].update(names)
            if values['-OPT3-'] == 'Show information about donor and the blood donated':
                # OK
                window['-INPUT-'].update(visible=False)
                window['-VIEW7-'].update(visible=False)
                window['-OPT5-'].update(visible=True)
                window['-SER-'].update(visible=False)
                window['-OPT44-'].update(visible=False)
                window['-OPT5-'].update(visible=False)
                window['-OPT6-'].update(visible=True)

                if values['-OPT6-'] == 'ALL':
                    query = "SELECT * FROM donor JOIN blood ON donor.ID = blood.donatedby_ID"
                    execute_query(query, cursor)
                elif values['-OPT6-'] == 'Specific Donor':
                    window['-INPUT-'].update(visible=True)
                    window['-SER-'].update(visible=True)
                    window['-VIEW7-'].update(visible=True)
                    ID = values['-INPUT-']
                    query = "SELECT * FROM donor " \
                            "JOIN blood ON donor.ID = blood.donatedby_ID "\
                            "WHERE donor.ID = '" + ID + "'"
                    execute_query(query, cursor)

                for ID, name, adress, cn, bg, mr, bloodID, dbID, gtID, bb in cursor:
                    data = "{:25}{:25}{:25}{:25}{:25}{:25}{:25}{:25}".format(ID, name, adress, cn, bg, bloodID, str(gtID), bb)
                    names.append(data)
                window['-LIST-'].update(names)

            elif values['-OPT3-'] == 'Find how many bags each blood bank has in stock in each blood group':
                #OK
                window['-INPUT-'].update(visible=False)
                window['-VIEW7-'].update(visible=False)
                window['-OPT5-'].update(visible=False)
                window['-SER-'].update(visible=False)
                window['-OPT5-'].update(visible=True)
                
                if values['-OPT5-'] != 'ALL':
                    BG = values['-OPT5-']
                    query = "SELECT blood_bank, donor.blood_group, COUNT(*) " \
                            "FROM blood, donor " \
                            "WHERE givento_ID IS NULL AND " \
                            "donatedby_ID = donor.ID AND " \
                            "blood_group = '" + BG + "' " \
                            "GROUP BY blood_bank, donor.blood_group"

                elif values['-OPT5-'] == 'ALL':
                    query = "SELECT blood_bank, donor.blood_group, COUNT(*) " \
                            "FROM blood, donor " \
                            "WHERE givento_ID IS NULL AND " \
                            "donatedby_ID = donor.ID " \
                            "GROUP BY blood_bank, donor.blood_group"
                
                execute_query(query, cursor)
                for BB, BG, count in cursor:
                    data = "{:25}{:25}{:25}".format(BB, BG, count)
                    names.append(data)

                window['-LIST-'].update(names)

            elif values['-OPT3-'] == 'Find blood banks where a specific donor has donated':
                #OK
                window['-INPUT-'].update(visible = True)
                window['-SER-'].update(visible=True)
                window['-VIEW7-'].update(visible=True)
                ID = values['-INPUT-']
                query = "SELECT donor.name, bloodbank.name, blood.blood_ID "\
                        "FROM donor, bloodbank " \
                        "JOIN blood ON bloodbank.name = blood.blood_bank "\
                        "WHERE donor.ID = blood.donatedby_ID AND donor.ID = '" + ID + "'"
                
                execute_query(query, cursor)
                for dname, bbname, bloodID in cursor:
                    data = "{:25}{:25}{:25}".format(dname, bbname, bloodID)
                    names.append(data)
                window['-LIST-'].update(names)
            elif values['-OPT3-'] == 'Find who patients donor is':
                #OK
                window['-INPUT-'].update(visible = True)
                window['-SER-'].update(visible=True)
                window['-VIEW7-'].update(visible=True)
                ID = values['-INPUT-']
                query = "SELECT donor.name, blood.blood_ID, blood.givento_ID " \
                        "FROM donor, blood "\
                        "WHERE blood.donatedby_ID = donor.ID "\
                        "AND blood.givento_ID = '" + ID + "'"
                execute_query(query, cursor)
                for name, bloodID, GTID in cursor:
                    data = "{} \t {} \t {}".format(name, bloodID, GTID)
                    names.append(data)
                window['-LIST-'].update(names)
            elif values['-OPT3-'] == 'See who has donated blood X times':
                #OK
                window['-INPUT-'].update(visible=True)
                window['-SER-'].update(visible=True)
                window['-VIEW8-'].update(visible=True)
                ID = values['-INPUT-']
                
                if ID != '':
                    query = "CREATE OR REPLACE VIEW donated(donatedby_ID, count) AS "\
                            "SELECT blood.donatedby_ID, COUNT(donatedby_ID) "\
                            "FROM blood "\
                            "GROUP BY donatedby_ID"
                    execute_query(query, cursor)
                    query = "SELECT donor.name, donatedby_ID "\
                            "FROM donated "\
                            "JOIN donor ON donatedby_ID = donor.ID " \
                            "WHERE count = " + ID
                    execute_query(query, cursor)

                    for name, DBID in cursor:
                        data = "{:30}{:30}".format(name, DBID)
                        names.append(data)
                    window['-LIST-'].update(names)


    if event == '-LIST-' and len(values['-LIST-']) and showAll:
        #POPUP SOM FUNKAR PÅ SHOW ALL DATA NÄR MAN KLICKAR PÅ EN DONOR
        if values['-OPT1-'] == 'Show all data':
            n = ''
            val = ''
            if values['-OPT2-'] == 'Donor':
                ID = values['-LIST-'][0][0:13]
                query = "SELECT name, medical_report FROM donor WHERE ID = '" + ID + "'"
                execute_query(query, cursor)
                for name, mr in cursor:
                    n = name
                    val = mr
                sg.popup('Selected donor: {} '.format(n), val)
            elif values['-OPT2-'] == 'Patient':
                ID = values['-LIST-'][0][0:13]
                query = "SELECT name, disease FROM patient WHERE ID = '" + ID + "'"
                execute_query(query, cursor)
                for name, dis in cursor:
                    n = name
                    val = dis
                sg.popup('Selected patient: {}'.format(n), val)

    if event in (sg.WIN_CLOSED, 'Exit'):                # always check for closed window
        break
    

window.close()
