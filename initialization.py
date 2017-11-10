# this file connects to our database and loads the tables and test data we give it into
# We would run this first to load the data before using the main.py file to run the actual project

import sqlite3
import time
import hashlib
import sys


import definetables
import definedata


def connect(path):
    # function that allows us to connect to the given database and create the cursor object
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

def initialize():
    global connection, cursor

    path = "./" + sys.argv[1] # the database name provided in the command line argument
    try: # makes sure we can connect to the database with sqlite3
        connect(path)
    except:
        print("Path does not work")
        
    definetables.define(connection, cursor) # create the tables here to put in the database 
    definedata.define(connection,cursor) # load the test data into the database
    
    
initialize()