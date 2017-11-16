# Small-Shopping-Database-Project
A simple project that works like an online shopping website. Customers can search, buy things and check order details. Agents can set up deliveries ,update deliveries and add products to the stock.


                                         Detailed Overview 
Start off with creating the tables and loading test data into the database with initialization.py. This file calls 2 functions imported from definetables.py and definedata.py
Define function in definetables.py creates the tables and puts it in the database
Define function in definedata.py  loads our testdata into the database

Then, we run our project with main.py. Here we connect to the database and let the user choose between customer or agent
If select user: main.py calls customer_screen function from customer_options.py
If select agent: main.py calls the agent_screen function from agent_options.py

In customer_options.py in the customer_screen function:
If user selects sign up:
we call customer_signup function which allows user to input cid, name, address, and password. Function checks that cid is unique otherwise user types a different cid. Then this info is stored in the customers table
If User selects sign in:
we call customer_signin function which allows user to input cid and password and program checks if input is correct from the customers table otherwise try logging in again.
If login is correct: we call the customer_menu function 
If user selects go back:  go back to the main function in main.py

In customer_options.py in the customer_menu function:
if user searches for products: search function from search.py is called
After entering search menu, it will call search, more_details, add_to_basket or show_basket function based on the customer’s choice.
search: match input keywords and rank search results; show 5 results at a time.
more_details: see the details of the product in the specified store after checking the constraints.
add _to_basket: add the product from specific store to the basket, or simply change the quantity if the product is already in the basket.
show_basket: show the products in the basket.  
If user places order, the place_order function  in the same file is called
if qty ordered for each product is less or equal to carries qty, user inputs delivery address and order is placed and stored in olines table
Otherwise we ask user to change the qty in their basket for the order
If user lists orders, list_order function in the same file is called:
if selects list all orders: each order with its appropriate info is shown
if selects details of order: we see more details of one order with delivery,product, and store info

In agents_options.py in the agent_screen function:
if user selects login
we call agent_signin function which allows user to input aid, and password. Program checks if this matches the one in the agents table otherwise try again
If login successful: call agent_menu function in the same file
is user selects back: we go back to main function in main.py

In agents_options.py in the agent_menu function:
if user selects set up delivery, set_up_delivery function is called in same file
We enter the order numbers in one line ( separated by whitespace ) and these orders will be added to one delivery. If any of these orders have already been delivered, program will ban you from adding them again.
if user selects update delivery, update_delivery function is called in same file
If we select to see details:  By entering the tracking number, the program will let us see what orders are included inside this delivery.
If we select to update pick-up and drop-off time: By entering the tracking number, the program will let you to reset the pick-up and drop-off time.
If we select to remove an order: By entering the order number, the program will let you to remove an order from the delivery table. If the order number does not exist in the delivery table, the program will ban you from doing this.
If we select back option: The program will return to the agent menu screen.
if user selects add to stock, add_stock function is called in same file
If add to stock: we check if the pid and sid inputted exists: if not we input again
if pid exists but it doesn’t exist in the store, we add a new entry to the carries table for the store with its qty and price
if pid already exists in store, we update qty and update price (optional step)
If select back: we go back to agent_screen function in agents_options.py 

                                                         Testing Strategy
(1) Divide and conquer: First we run individual tests on each function to make sure its correctness; and then test different function groups before we test the whole project. In this way both correctness of the code and efficiency can be guaranteed. 
(2) Ensure Robustness: 
      a) We designed several versions of test data to debug and to ensure the correctness under different databases. 
      b) We put many “check valid inputs” statement in the code and then test it using random inputs to ensure its robustness. In this way we prevent the code from breaking when the user inputs are invalid.     

                                                             Bugs
Bugs in Search function:
 Use “left outer join” instead of “natural join” on pid because using “natural join” will eliminate the qualified results if the number of orders of that product is 0. 
Use the string match function in sqlite(e.g. where name like :%keyword%) can only give us the products’ name which contain the keyword; we also have to check if the product is a substring of the keyword to give better search results.
A bug in Place Order function: In a particular case, when the quantity carried by the store is 0 and we chose to reset the quantity, we would fall into an infinite loop, that is, whatever quantity you are trying to enter, you will be asked to reenter it again and again. Later we add an extra “ if condition” to our code. It will disable you to select  the ”change quantity” option when the quantity carried by the store is 0.
A bug in List Order function:  we first grouped the orders by sid and oid, because different stores have different price on the products, but it brings inconvenience for calculating the total price; then we realized we can just group the order by oid and use expression sum(uprice * qty) to obtain the same results.  
A bug in Add to stock function: If the user enters a pid and sid  that does not exists in the products and stores table, the program will crash( “ The foreign key constraint fails”). Later we fixed it by checking if the pid and sid exists inside the two tables.


                                                  Group Break Down Strategy
Monica worked on customer functionality #3 and agent function #3. Primarily worked on the interface, program structure, and login screen options of the project. Spent roughly 12 hours.
Minghan worked on creating proper test data, customer functionality #1, and is the main tester for our project. 12 hours
Cijie worked on customer functionality #2 and both the 1st and 2nd agent functions. Also assisted with the interface for improvement and to help fix bugs overall. 12 hours
Testing was done by each member, bugs were reported to Minghan, and then we all pair programmed to fix these bugs. Time Spent 5 hours.
All members worked on the design document. Time spent 3 hours.
We used github to coordinate our project’s progress so we can see each other’s commits and check for potential problems 


