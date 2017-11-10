import sqlite3
import time

def search_screen(conn,cursor):# search interface 
	while True:
		print ("\n-----------SEARCH SCREEN----------\n")
		choice = input("1.Search Products\n2.Products details\n3.Add to basket\n4.Show basket\n5.Back\n>>")
		if choice == "1":
			keywords = input("Enter the product's name you want to search\n>>")
			search(keywords, conn, cursor)
		elif choice == "2":
			more_details(conn, cursor)
		elif choice == "3":
			add_to_basket(conn, cursor)			
		elif choice == "4":
			show_basket(conn, cursor)
		elif choice == '5':
			return
		else:
			continue

def search(keyword, conn, cursor): # main search function

	# create a temporary table for storing search results
	cursor.execute('''drop table if exists temp;''') 
	cursor.execute('''CREATE TABLE temp (
                        pid text,
                        name text,
                        unit text,
                        num_stores int,
                        min_price real,
                        num_orders int,
                        PRIMARY KEY (pid)
                         );''')
	conn.commit()

	# split the keywords
	keywords = keyword.split(' ')
	
	if keyword not in keywords:
		keywords.append(keyword)
	
	if keywords == ['']:
		print("Please enter non-empty string!\n")
		return 
		
	for key in keywords:
		rows = accurate_search(key, conn, cursor)
		# if the keyword doesn't exist in produts table, continue
		if rows is None:
			continue
		#store the results in the temporary table, and rank the results later
		for i in range(len(rows)):
			cursor.execute('''insert or ignore into temp values (?,?,?,?,?,?);''',rows[i])
		conn.commit()
		
	show_results(keywords, conn, cursor)

# accurate search, return the names that contain the complete keyword 
def accurate_search(key, conn, cursor):
	cursor.execute(''' select p.pid, p.name, p.unit, count(c.sid), min(c.uprice), count(distinct or1.oid)
					from products p, carries c
					left outer join olines ol on p.pid = ol.pid and ol.sid = c.sid
					left outer join orders or1 on or1.oid = ol.oid and or1.odate between date('now', '-7 days') and date('now', '+1 day')
					where p.pid = c.pid
					and p.name like :product_name collate nocase
					group by p.pid, p.name, p.unit
					order by c.uprice;
					''',{"product_name":'%'+key+'%'})
								
	rows = cursor.fetchall()
	return rows 

def take_second(elem):#helper function for _show_results
	return elem[1]

# show the first five results and rank the data before passing to the true show results
def _show_results(keywords, conn, cursor):
	cursor.execute("select * from temp")
	rows = cursor.fetchall()
	data = []
	#rank the results based on the similarity to the keywords	
	for row in rows:
		max_match = 0.0
		match = 0.0
		for key in keywords:
			if key in row[1]:
				match = len(key)
			match /= len(row[1])
			if match > max_match:
				max_match = match
		data.append((row, -max_match))
	
	data.sort(key = take_second)
	data = [d[0] for d in data]
	
	#call the formatted print function
	title = ["pid", "name", "unit", "num_stores", "min_price","num_orders"]
	if 0 < len(data) < 5:
		print_table(title, data)
	else:	
		print_table(title, data[0:5])

	return data
					
def show_results(keywords, conn, cursor):
	data = _show_results(keywords, conn, cursor)

	if len(data) == 0:
		print("There is no such product!\n")
		return 
	
	# enter show results loop; show five results in each page
	i = 1 # page number
	while True:
		choice = input("Do you want to see more search results [y/n]\n>>")
		if choice == 'y':
			title = ["pid", "name", "unit", "num_stores", "min_price","num_orders"]
			if len(data) <= 5: # if total results are less than five results in one page
				print_table(title, data)
				i = 0# keep looping
				continue
				
			if (i+1)*5 >= len(data): # if there are less than five results in one page
				print_table(title, data[i*5:])
				i = 0# back to the beginning and keep looping
				continue
			else:# print five results in each page
				print_table(title, data[i*5:(i+1)*5])	
		else:
			return
		i += 1

def more_details(conn, cursor):# see the details of the products from search results
	while True:
		print ("Product details.")
		pid = input("Enter the product id and see more details of it\n>>")
		cursor.execute(''' select p.pid, p.name, p.unit, p.cat, c.sid, c.qty, c.uprice, count(distinct ol.oid)
								from carries c, products p
								left outer join olines ol on p.pid = ol.pid and ol.sid = c.sid
								where p.pid = c.pid
								and p.pid =:pid
								and c.qty > 0
								group by p.pid, p.name, p.unit, p.cat, c.sid, c.qty, c.uprice
								order by c.uprice;
								''',{"pid":pid})
		
		data1 = cursor.fetchall() # rank the stores that have the product in stock

		cursor.execute(''' select p.pid, p.name, p.unit, p.cat, c.sid, c.qty, c.uprice, count(distinct ol.oid)
								from carries c, products p
								left outer join olines ol on p.pid = ol.pid
								where p.pid = c.pid
								and p.pid =:pid
								and c.qty = 0
								group by p.pid, p.name, p.unit, p.cat, c.sid, c.qty, c.uprice
								order by c.uprice;
								''',{"pid":pid})

		data2 = cursor.fetchall()# rank the stores that don't have the product in stock

		if len(data1) == 0 and len(data2) == 0:
			print("No such product in the search result!\n")
			
			choice = input("Enter the pid again?[y/n]\n>>")
			if choice == 'y':
				continue
			else:
				return
			
		else:
			title = ["pid", "name", "unit", "category", "sid", "quantity", "uprice", "num_orders"]
			if len(data1) != 0:
				print_table(title, data1)
			if len(data2) != 0:
				print_table(title, data2)

			choice = input("Do you want to see details of other products [y/n]\n>>")
			if choice == 'y':
				continue
			else:
				return


def add_to_basket(conn, cursor):# add the produts to the basket
	flag = True
	while True:
		print ("-----Your basket-----")
		show_basket(conn, cursor)
		if not flag:# do not ask the customer when adding the first product
			choice = input ("Do you want to keep adding products [y/n]\n>>")
			if choice == 'n':
					return
		flag = False

		sid = input("Enter the store id\n>>")
		cursor.execute('''select * from stores where sid = :sid''',{"sid":sid})
		data = cursor.fetchall()

		if len(data) == 0:# check store
			print("Store ID not exists!\n")
			continue
    		
		pid = input("Enter the product id and add it to the basket\n>>")
		cursor.execute('''select * from products where pid = :pid''',{"pid":pid})
		data = cursor.fetchall()
		if len(data) == 0:# check product
			print("Product ID not exists!\n")
			continue
    	
		cursor.execute('''select * from carries where pid = :pid and sid=:sid''',{"pid":pid, "sid":sid})
		data= cursor.fetchall()
		if len(data) == 0:# check if the product in the store
			print("The product ", pid, " is not in the store ", sid, " !\n")
			continue
			
		qty = input("Enter the quantity you want to buy[default 1]\n>>") or "1"
		
		cursor.execute('''select sid, pid from basket where sid = :sid and pid = :pid''',{"pid":pid,"sid":sid})
		data = cursor.fetchall()
		if len(data) == 0:# if no such product in the basket, add the product
			cursor.execute('''insert into basket values (?, ?, ?);''', (sid, pid, qty))
		else:# if there are same products in the basket, just change the quantity 
			cursor.execute("update basket set qty = qty+'%s' where pid = :pid and sid = :sid "%qty,{"pid":pid,"sid":sid})

		conn.commit()
      
def show_basket(conn, cursor):# show the product in the basket
	cursor.execute("select * from basket")
	data = cursor.fetchall()
	title = ["sid", "pid", "quantity"]
	if len(data) is 0:
		print("The basket is empty!\n")
	else:
		print_table(title, data)

#----------helper functions----------
	
def print_table(title, data):# helper function, formatted printing 
	if len(data) == 0:
		return

	row_format ="{:>15}" * (len(title) + 1)
	print(row_format.format("", *title))	
	for row in data:
		print(row_format.format(" ", *row))
	print("\n")


	
	
	
	
	
	
	
