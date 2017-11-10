import sqlite3
import time
import hashlib
import getpass
import datetime
import search

def customer_screen(connection,cursor):
    # the customer screen where they can sign up as a new customer, sign in, or go back to the beginning screen
    
    while True:
        print("\n--------CUSTOMER MAIN SCREEN---------\n")
        user_selection = input("1.Sign in\n2.Sign up\n3.Back\n>>")
            
        if user_selection == "1": # sign in as customer
            customer_signin(connection, cursor)
        elif user_selection == "2": # sign up as a new customer
            customer_signup(connection, cursor)
        elif user_selection == "3": # go back to beginning
            break
        else:
            print("Invalid option")
        


def list_order(cid,connection,cursor):
    # function allows the customer to list all their orders or see an order in more detail 
    
    offset = 0
    while True:
        print("\n-----------LISTING ORDERS------------\n")
        option = input("1.List all orders\n2.See an order in more detail\n3.Back\n>>")
        print("\n")
            
        if option == "1":
            # customer chooses to list all their orders which gives a general view of the total price in the order,
            # order id, when it was ordered, and the amount of unique products bought
            
            cursor.execute("""select orders.oid, orders.odate, count(distinct(olines.pid)), sum(olines.uprice * olines.qty)
                        from orders,olines
                        where orders.cid = :cid and
                        orders.oid = olines.oid
                        group by orders.oid
                        order by orders.oid DESC
                        LIMIT 5 offset :offset;
            """,{"cid":cid,"offset":offset})

            
            entry = cursor.fetchall()
                 
            if len(entry) == 0 or entry == None:
                print("No orders exists")           
            for thing in entry:
                # print appropriate info in listing all orders
                oid = thing[0]
                odate = thing[1]
                number_products = thing[2]
                price = thing[3]
                print("oid: %r, orderdate: %r, numberofproducts: %r, price: %.2f" % (oid,odate,number_products,price))
            print("\n")
            
            # query checks if there are more then 5 orders for the customer to view
            cursor.execute("""select orders.oid, orders.odate, count(distinct(olines.pid)), sum(olines.uprice * olines.qty)
                        from orders,olines
                        where orders.cid = :cid and
                        orders.oid = olines.oid
                        group by orders.oid
                        order by orders.odate DESC
                        LIMIT 5 offset :offset;
            """,{"cid":cid,"offset":offset+5})
            
            entry = cursor.fetchall()           
            
            if len(entry) == 0: # if theres less than 5 orders in the view, then we just ignore the option to view more
                offset = 0
                continue
            
            
            while True:
                # if there are more than 5 orders, they can view more by selecting list all orders again 
                # or stop if they wish which resets the view list back to the first order
                more = input("1.You have more than 5 orders, do you wish to see more\n2.No thank you\n>>").lower()
                if more == "1":
                    print("\nSelect the list all orders option again to see the next 5\n")
                    offset += 5
                    break
                elif more == "2":
                    offset = 0
                    break
                                       
            print("\n")
            
        elif option == "2":
            # customer chooses to see an order in more detail
            # we can see its delivery info, each product in the order and 
            # its details of which store it was bought from, its price, unit, and the qty bought in the order
            
            while True:
                oid = input("Enter the oid for the order you wish to check\n>>")
                cursor.execute("select oid from olines where oid = :oid;",{"oid":oid})
                try:
                    oid = cursor.fetchone()[0]
                    break
                except:
                    print("oid does not exist")
                    continue
            
             
            cursor.execute(""" select deliveries.trackingNo,deliveries.pickUpTime,deliveries.dropOffTime,orders.address,
            olines.pid, olines.sid,stores.name, products.name, olines.qty, products.unit, olines.uprice
            from deliveries,olines,orders,carries,stores,products
            where deliveries.oid = :oid and 
            deliveries.oid = olines.oid and orders.oid = olines.oid and
            olines.sid = stores.sid and carries.sid = olines.sid and products.pid = olines.pid
            group by olines.sid, olines.pid
            ;
            """,{"oid":oid}) 
            
            
            rows = cursor.fetchall()
            
            if len(rows) == 0: 
                # this means that the order has not been put in the system for deliveries by the agent yet but
                # we can still show the products in the delivery and its details.
                
                cursor.execute(""" select orders.address,
                olines.pid, olines.sid,stores.name, products.name, olines.qty, products.unit, olines.uprice
                from olines,orders,carries,stores,products
                where olines.oid = :oid and 
                orders.oid = olines.oid and olines.sid = stores.sid 
                and carries.sid = olines.sid and products.pid = olines.pid
                group by olines.sid, olines.pid
                ;
                """,{"oid":oid})   
                
                rows = cursor.fetchall()
                
                for index in range(len(rows)):
                    address = rows[index][0]
                    pid = rows[index][1]
                    sid = rows[index][2]
                    store_name = rows[index][3]
                    product_name = rows[index][4]
                    qty = rows[index][5]
                    unit = rows[index][6]
                    uprice = rows[index][7]  
                    
                    if index == 0:
                        print("Order has not been verified with an agent to deliver it yet!")
                        print("\nDelivery info is unknown!")
                        print("Delivery address for order #%s : %s\n"%(oid,address))
                        print("%-15s%-15s%-15s%-15s%-15s%-15s%-15s"%("pid","sid","store_name","product_name","qty","unit","uprice"))
                        print("%-15s%-15s%-15s%-15s%-15s%-15s%-15s" % (pid,sid,store_name,product_name,qty,unit,uprice))

                    else:
                        print("%-15s%-15s%-15s%-15s%-15s%-15s%-15s" % (pid,sid,store_name,product_name,qty,unit,uprice))
                continue
            
            for index in range(len(rows)): 
                # we can print its delivery info since it exists, each product in the order, 
                # its details in the order, and the order it is associated with
                
                tracking = rows[index][0]
                pickup = rows[index][1]
                dropoff = rows[index][2]
                address = rows[index][3]
                pid = rows[index][4]
                
                sid = rows[index][5]
                store_name = rows[index][6]
                product_name = rows[index][7]
                qty = rows[index][8]
                unit = rows[index][9]
                uprice = rows[index][10]
                if index == 0:
                    print("Order #%s is included in delivery #%s"%(oid,tracking))
                    print("pickup time: %r, dropoff time: %r, delivery_address: %r\n" % (pickup,dropoff,address))
                    print("%-15s%-15s%-15s%-15s%-15s%-15s%-15s"%("pid","sid","store_name","product_name","qty","unit","uprice"))
                    print("%-15s%-15s%-15s%-15s%-15s%-15s%-15s" % (pid,sid,store_name,product_name,qty,unit,uprice))
                    
                else:
                    print("%-15s%-15s%-15s%-15s%-15s%-15s%-15s" % (pid,sid,store_name,product_name,qty,unit,uprice))
                      
        elif option == "3": # customer wishes to go back to their main menu
            break
            
        else:
            print("Invalid option please try again")
    
    connection.commit()
    return

def place_order(cid,connection,cursor):
    print("\n------------- PLACE ORDERS -------------\n")
  
    cursor.execute("SELECT * from basket; ")
    basket_rows = cursor.fetchall()
    
    if len(basket_rows) == 0:
        print("Your basket is empty")
        return 
    # check if there are products whose quantity is set too high

    for row in basket_rows:
        pid = row[1]
        sid = row[0]
        order_qty = row[2]
        cursor.execute("SELECT qty from carries where sid=:sid and pid = :pid",{"sid":sid,"pid":pid})
        carry_qty = cursor.fetchone()[0]
        cursor.execute("SELECT name from products where pid=:pid",{"pid":pid})
        name = cursor.fetchone()[0]

        if order_qty > carry_qty:
            print("The product in store #%s: %s's quantity you set is too high! " % (sid,name))
            print("Your quantity: %d Quantity left in store: %d " % (order_qty,carry_qty))
            while True:
                choice = input("1.Delete this product from the basket\n2.Change the quantity\n>>")
                if choice == "1":
                    break
                elif choice =="2" and carry_qty == 0:
                    print("The quantity left in store is 0. You can only delete it")
                    continue
                elif choice == "2":
                    break
                else:
                    print("Invalid option!")
                    continue

            if choice == "1":
                cursor.execute("DELETE FROM basket where pid = :pid and sid = :sid",{"pid":pid,"sid":sid})
                print("Delete successfully!")
                print("\n")
            elif choice == "2":
                while True:
                    try:
                        new_qty=int(input("Please reset the quantity for %s\n>>" % name))
                        if new_qty > carry_qty or new_qty <= 0:
                            print("Invalid value!")
                            print("\n")
                            continue
                        else:
                            print("new set qyt is %d"%new_qty)
                            cursor.execute("update basket set qty = '%d' where pid = :pid and sid =:sid;"%new_qty,{"pid":pid,"sid":sid})
                            print("Quantity Changed!")
                            print("\n")
                            break
                    except:
                        print("Invalid value!")

    # update the corresponding table
    # 1.update the orders table

    address = input("Please enter the address you want this order to be delivered to\n>>")
    cursor.execute("select count(*) from orders;")
    order_count = cursor.fetchone()[0]
    new_oid = 1 + order_count
    date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    order_data = (new_oid,cid,date,address)
    cursor.execute('''insert into orders values
                        (?,?,?,?);''',order_data)

    # 2.update the olines table and deduct the qty from the carries table

    cursor.execute("SELECT * from basket; ")
    basket_rows = cursor.fetchall()
    for row in basket_rows:
        pid = row[1]
        sid = row[0]
        qty = row[2]
        
        cursor.execute("select uprice from carries where sid = :sid and pid = :pid",{"pid":pid,"sid":sid})
        uprice = cursor.fetchone()[0]

        oline_data = (new_oid,sid,pid,qty,uprice)
        cursor.execute(''' insert into olines values
                            (?,?,?,?,?)''',oline_data)

        # deduct the quantity
        cursor.execute("update carries set qty = qty-'%s' where pid = :pid and sid = :sid "%qty,{"pid":pid,"sid":sid})
    cursor.execute("delete from basket;") # clear the basket 
    print("Your order #%d is placed successfully!"%new_oid)
    connection.commit()


    return


def customer_menu(cid,connection,cursor):
    # function that shows the main customer menu options
    # can choose to search for products to place in basket, place an order with their basket,
    # or list all their current orders
    
    cursor.execute("drop table if exists basket;")
    # create basket for the customer to put their products in to order later
    basket_query = '''CREATE TABLE basket (
                        sid int,
                        pid text,
                        qty int,
                        PRIMARY KEY (sid,pid)
                         );
                    '''
    cursor.execute(basket_query)
    
    while True:
        print("\n-------------CUSTOMER OPTIONS MENU-------------\n")
        choice = input("1.Search\n2.Place an Order\n3.List Orders\n4.Logout\n>>")
        if choice == "1": # searching products to put in basket functionality
            search.search_screen(connection,cursor)
        elif choice == "2": # place orders functionality
            place_order(cid,connection,cursor)
        elif choice == "3": # listing orders functionality
            list_order(cid,connection,cursor)
        elif choice == "4":
            cursor.execute("DROP table basket;") # when customer logs out, we drop values in their shopping basket
            print("Logout Successfully!")
            break
        else:
            print("Invalid option!")
            continue
    
    connection.commit()

def customer_signin(connection,cursor):
    # function that allows the customer to signin with their unique cid and password
    
    while True:
        print("\n---------CUSTOMER SIGNIN-------------\n")
        cid = input("Enter your customer id\n>>")
        pwd = getpass.getpass() # enter password in thats non visible
        
        # query checks that their cid exists and if the password in the database and the password
        # the customer inputted is the same otherwise they have to try logging in again
        cursor.execute(""" select pwd from customers where cid = :cid;""",{"cid":cid})
        password = cursor.fetchone()
        
        if password == None:
            print("Try logging in again!")
            continue
        
        if password[0] == pwd:
            print("Login Successfully!")
            customer_menu(cid,connection,cursor) # brought to the main customer options menu
            break
        else:
            print("Try logging in again!")
            continue
    
    
    connection.commit()
    return
    
     
    
def customer_signup(connection, cursor):
    # function that allows for a new customer to sign up in the system
    # Database checks if their cid is unique in the system, and if not they have to input a new one
    # We store their unique cid, name, address, and password for them to login later
    
    while True: 
        print("\n---------SIGN UP-------------\n")
        cid = input("Enter your customer id\n>>")
        name = input("Enter your name\n>>")
        address = input("Enter your address\n>>")
        pwd = getpass.getpass() # allow customer to type in a non visible password
    
        cursor.execute(""" select * from customers where cid = :cid;""",{"cid":cid}) 
        row = cursor.fetchone()

        if row != None: # checks if customer exists is in the customers table
            print("Customer already exists. Try another cid!")
            continue
        else:
            break
            
    data = (cid,name,address,pwd)
    cursor.execute("""insert into customers values (?,?,?,?);""",data) # store customer info in its table
    print("Sign up successfully!")
    connection.commit()
    return        
