# main project file where all functions from other files are imported here

# People who worked on this CMPUT 291 Project 1:
# Date: Monday Nov 6 2017
# Monica Bui  LEC A1 LAB D06
# Minghan Li LEC A1 LAB D01
# Cijie Xia LEC A1 LAB D08
# Did not collaborate with anyone else


import sqlite3
import time
import hashlib
import sys

import customer_options as cust
import agents_options as agt


connection = None
cursor = None


def connect(path):
    # function that allows us to connect to the given database and create the cursor object
    
    global connection, cursor

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute('PRAGMA foreign_keys=ON; ')
    connection.commit()
    return

    
def main():
    # main function that connects to the database with sqlite 3 and shows the beginning interface for the user to select customer options or agent options
    global connection, cursor

    path = "./" + sys.argv[1] #the database name provided in the command line argument
    try: # we make sure that we can connect to the database with sqlite3
        connect(path)
    except:
        print("Path does not work")

    while True:
        print("---------USER SELECTION SCREEN-------\n")
        user_selection = input("1.Customer Login\n2.Agent Login\n3.Exit\n>>")
        
        if user_selection == "1":
            cust.customer_screen(connection, cursor) # go to the customer screen options found in the customer_options.py file
        elif user_selection == "2": # go to the agent screen options found in the agent_options.py file
            agt.agent_screen(connection, cursor)
        elif user_selection == "3": # log out of the whole program
            break
        else:
            print("Try again")
        
        
    connection.commit()
    connection.close()    

if __name__ == "__main__":
    main()
