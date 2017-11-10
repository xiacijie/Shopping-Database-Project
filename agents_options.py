import sqlite3
import time
import hashlib
import getpass


def agent_screen(connection,cursor):
    # function that shows the beginning main screen for the agent where they can login 
    # or go back to the very beginning
    
    while True:
        print("\n-----------AGENT MAIN SCREEN ----------\n")
        user_selection = input("1.Sign in\n2.Back\n>>")
        if user_selection == "1":
            agent_signin(connection, cursor)
        elif user_selection == "2":
            break
        else:
            print("Invalid option!")
    return

def set_up_delivery(connection,cursor):
    print("\n-----------SETUP DELIVERY--------\n")
    # show all the orders 
    cursor.execute("select oid from orders;")
    rows = cursor.fetchall()
    print("order No.")
    for row in rows:
        print("Order #%d"%row[0])
    print("\n")	


    print("Please enter the order number(s) you want to include in this delivery(separate by space)\n>>")
    order_num_str = input()
    order_list = order_num_str.split(" ")

    for oid in order_list:
        cursor.execute("select * from deliveries where oid = :oid;",{"oid":oid})
        row = cursor.fetchone()
        if row != None: # check is the order has been delivered
            print("Order #%s has already been deliveried"%oid)
            return
    cursor.execute(''' select count(distinct trackingNo) from deliveries;''' )
    track_count = cursor.fetchone()[0]
    
    track_no = 1 + track_count # generate a unique tracking number

    for oid in order_list:
        cursor.execute("select * from orders where oid = :oid;",{"oid":oid})
        if (cursor.fetchone() == None): # when the oid to be deleted does not eixist
            print("Order No. #%s does not exist!"%oid)
            continue

        while True: # set the pick up time
            selection = input("Do you want to set a pick-up date for order:%s?\n1.Yes\n2.No\n>>"%oid)
            
            if selection == "1":
                pick_up_date = input("Please enter the pick-up date for order:%s YYYY-MM-DD\n>>"%oid)
                break
            elif selection == "2":
                pick_up_date = "NULL"
                break
            else:
                print("Invalid option!")
            
        
        drop_off_date = "NULL"
        delivery_data =(track_no,int(oid),pick_up_date,drop_off_date)
        
        # update the database
        cursor.execute('''insert into deliveries values
                           (?,?,?,?)''',delivery_data)
        print("Order #%s successfully added into the delivery #%d!"%(oid,track_no))

def update_delivery(connection,cursor):
    
    
    print("\n--------------UPDATE DELIVERY -----------\n")
    cursor.execute("select trackingNo from deliveries;" )

    # print all the current tracking numbers
    print("Tracking numbers")
    rows = cursor.fetchall()
    for row in rows:
        print("Tracking #%d"%row[0])
    print("\n")

    while True: # update delivery screen
        selection = input("1.See details\n2.Update pick up and drop off time\n3.remove an order\n4.back\n>>")
        
        if selection == "1": # list all the order numbers included in this delivery
            track_no = input("Enter the tracking number\n>>")
            cursor.execute("select oid,pickUpTime,dropOffTime from deliveries where trackingNo = :trackingNo",{"trackingNo":track_no})
            
            rows = cursor.fetchall()
            if len(rows) == 0: #in case that the track No does not exist
                print("There are no orders included in delivery track No.#%s!"%track_no)
                return

            print("The order No. included in this delivery are listed below:") #list the details in the delivery
            for row in rows:
                print("Order #%s pickUpTime: %s DropOffTime: %s"%(row[0],row[1],row[2]))
            print("\n")
                
        elif selection == "2": # update the pick up and drop off time 
            oid = input("Enter the order number you want to change its pickup and dropoff date\n>>")
            cursor.execute("select * from deliveries where oid = :oid",{"oid":oid})
            if cursor.fetchone() == None: #in case that the oid does not exist
                print("The order number does not exist in the delivery!")
                return 
            
            while True: # for the pick up time
                selection = input("Update the pick up time\n1.YES\n2.NO\n>>")
                if selection == "1":
                    new_pickup_time = input("Enter a new pick up time YYYY-MM-DD\n>>")
                    cursor.execute("update deliveries set pickUpTime = '%s' where oid = :oid"%new_pickup_time,{"oid":oid})
                    break
                elif selection == "2":
                    break
                else:
                    continue

            while True: # for the drop off time
                selection = input("Change the drop off time\n1.YES\n2.NO\n>>")
                if selection == "1":
                    new_dropoff_time = input("Enter a new drop off time YYYY-MM-DD\n>>")
                    cursor.execute("update deliveries set dropOffTime = '%s' where oid = :oid"%new_dropoff_time,{"oid":oid})
                    break
                elif selection == "2":
                    break
                else:
                    continue

        elif selection == "3": # remove an order
            cursor.execute("select oid from deliveries;")
            print("Order No.")
            rows = cursor.fetchall()
            for row in rows:
                print("Order #%d"%row[0])
            print("\n")
            oid = input("Please enter the order No. you want to remove\n>>")
            cursor.execute("select * from deliveries where oid = :oid",{"oid":oid})

            if cursor.fetchone() == None: #in case that the oid does not exist
                print("The order number does not exist in the delivery!")
                return
            cursor.execute("delete from deliveries where oid = :oid",{"oid":oid})
            print("Delete the Order #%s successfully!"%oid)
            print("\n")
        elif selection == "4": # back
            break
        else:
            print("Invalid option!")
    connection.commit()



def add_stock(connection,cursor):
    # Add to stock function that updates the qty of product carried by the store and the agent is given the choice 
    # to update the price if they wish to do so. Function also checks if the pid and sid exist in the database.
    # If the product does not exist for a store, we add it to the store with its new qty and price values.
    
    while True:
        print("\n---------------ADD TO STOCK -------------\n")
        option = input("1.Add to stock\n2.Exit\n>>")
        print("\n")
        if option == "1": # agent wishes to add to stock
            
            pid = input("Enter the pid you wish to select\n>>")
            cursor.execute("select pid from carries where pid = :pid;",{"pid":pid})
            check = cursor.fetchone() # checks if product exists in database
            if check == None:
                print("Product does not exist")
                continue            
            
            sid = input("Enter the sid you wish to select\n>>")
            cursor.execute("select sid from carries where sid = :sid;",{"sid":sid})
            check = cursor.fetchone() # checks if store exists in database
            if check == None:
                print("Store does not exist")
                continue
            
            cursor.execute("select pid,sid from carries where pid = :pid and sid = :sid;",{"pid":pid,"sid":sid})
            check = cursor.fetchone() 
            
            if check == None: # if current product does not exist in store, make a new entry
                print("Product does not exist in store so let's add a new product to this store")
                while True:
                    new_qty = input("Number of products you wish to add for the designated pid and store\n>>")
                    try:
                        new_qty  = int(new_qty) #checks if qty given is valid
                        if new_qty  > 0:
                            break
                        else:
                            print("Invalid number")
                    except:
                        print("Invalid input")
                        continue       
                    
                    
                while True:
                    price = input("Input your new price for this product\n>>")
                    try:
                        price = float(price) #checks if price given is valid
                        if price > 0:
                            break
                        else:
                            print("Invalid price")
                    except:
                        print("Error with updating new price, make sure its in decimal format")
                        continue     
                    
                carries_data = (sid, pid, new_qty, price)                  
                cursor.execute("insert into carries values (?,?,?,?);",carries_data) # insert new product values in the carries table for the selected store
                
                print("Inserted product: %r at store: %r is successful" % (pid,sid))
                
            elif check[0] == pid and str(check[1]) == sid: # if product already exists in current store
                
                while True:
                    new_qty = input("Number of products you wish to add for the designated pid and store\n>>")
                    try:
                        new_qty = int(new_qty) # check if given qty is valid
                        if new_qty > 0:
                            break
                    except:
                        print("Invalid number of products to add")
                        continue
                
                
                cursor.execute("update carries set qty = qty +'%d' where pid = :pid and sid =:sid;" % new_qty,{"pid":pid,"sid":sid}) #update the qty for the product at the designated store
                
                
                while True:
                    # give option for agent to change the price if they wish
                    
                    option = input("Do you wish to also change the unit price for this pid? (y/n)\n>>").lower() 
                    if option == "y": 
                        while True:
                            price = input("Input your new price\n>>")
                            try:
                                price = float(price) # check if price is valid
                                if price > 0:
                                    break
                            except:
                                print("Error with updating new price, make sure its in decimal format")
                                continue
                        
                        cursor.execute("update carries set uprice ='%f' where pid = :pid and sid =:sid;" % price,{"pid":pid,"sid":sid}) # update the price for the product at the designated store
                        
                        print("Add to stock for product: %r at store: %r is completed" % (pid,sid))
                        break
                        
                    elif option == "n":
                        print("Add to stock for product: %r at store: %r is successful" % (pid,sid))   
                        break
                    else:
                        print("Invalid option")
                
        elif option == "2": # agent wishes to go back to the main menu
            break   
        else:
            print("Invalid option")
        
    connection.commit()
    return

def agent_menu(connection,cursor):
    # function that shows the interface for the options that agents can access once logged in
    
    while True:
        print("\n------------AGENT OPTION MENU------------\n")
        choice = input("1.Set up Delivery\n2.Update Delivery\n3.Add to Stock\n4.Logout\n>>")
        
        if choice == "1": # agent chooses to set up a new delivery
            set_up_delivery(connection,cursor)
        elif choice == "2": # agent chooses to update an existing delivery
            update_delivery(connection,cursor)
        elif choice == "3": # agent chooses to add stock for a product at a store
            add_stock(connection,cursor)
        elif choice == "4": # logging out
            print("Log out successfully!")
            break
        else:
            print("Invalid option!")
            continue

def agent_signin(connection,cursor):
    # function that shows the interface for the agent sign in option. 
    # allows agent to type their id and their password to access their agent option screen
    
    while True:
        print("\n---------------AGENT SIGNIN--------------\n")
        aid = input("Enter your agent id\n>>") # agent inputs their aid
        pwd = getpass.getpass() # agent inputs password that is non visible on screen
        
        
        # below we compare if the password the agent inputs and the password stored in the database match
        # if it is wrong or they input nothing, they are prompted to enter it again.
        # if both passwords match, the agent is then brought to their menu screen
        cursor.execute(""" select pwd from agents where aid = :aid;""",{"aid":aid})
        password = cursor.fetchone()
        if password == None:
            print("Try logging in again!")
            continue       
    
        if password[0] == pwd: 
            print("Log in successfully!")
            agent_menu(connection,cursor)
            break
        else:
            print("Try logging in again!") 
            continue
    
    connection.commit()
    return
    
     
    
