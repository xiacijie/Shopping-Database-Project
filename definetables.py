import sqlite3
import time
import hashlib

def define(connection,cursor):
    # create the database structure and tables with this function
    
    cursor.execute("drop table if exists deliveries;")
    cursor.execute("drop table if exists olines;")
    cursor.execute("drop table if exists orders;")
    cursor.execute("drop table if exists customers;")
    cursor.execute("drop table if exists carries;")
    cursor.execute("drop table if exists products;")
    cursor.execute("drop table if exists categories;") 
    cursor.execute("drop table if exists stores;")
    cursor.execute("drop table if exists agents;")
    
    agents_query=   '''
                        CREATE TABLE agents (
                                    aid text,
                                    name text,
                                    pwd text,
                                    PRIMARY KEY (aid)
                                    );
                    '''

    stores_query=  '''
                        create table stores (
                               sid int,
                               name text,
                               phone text,
                               address text,
                               primary key (sid)
                               );
                    '''

    categories_query= '''
                        create table categories (
                               cat char(3),
                               name text,
                               primary key (cat)
                               );
                    '''
    
    products_query = '''
                    create table products (
                    pid char(6),
                    name text,
                    unit text,
                    cat	char(3),
                    primary key (pid),
                    foreign key (cat) references categories
                    );
                '''
    
    carries_query = '''
                    create table carries (
                    sid		int,
                    pid		char(6),
                    qty		int,
                    uprice	real,
                    primary key (sid,pid),	
                    foreign key (sid) references stores,
                    foreign key (pid) references products);
    
    '''
    
    customers_query = '''
                    create table customers (
                    cid		text,
                    name		text,
                    address	text,
                    pwd		text,
                    primary key (cid)
                    );
    
                    '''
    
    orders_query = '''
                    create table orders (
                    oid		int,
                    cid		text,
                    odate		date,
                    address	text,
                    primary key (oid),
                    foreign key (cid) references customers
                    );
                  '''
    
    olines_query = '''
                create table olines (
                oid		int,
                sid		int,
                pid		char(6),
                qty		int,
                uprice	real,
                primary key (oid,sid,pid),
                foreign key (oid) references orders,
                foreign key (sid) references stores,
                foreign key (pid) references products
                );
    '''
    
    deliveries_query = '''
                create table deliveries (
                trackingNo	int,
                oid		int,
                pickUpTime	date,
                dropOffTime	date,
                primary key (trackingNo,oid),
                foreign key (oid) references orders
                );
    '''
    cursor.execute(agents_query)
    cursor.execute(stores_query)
    cursor.execute(categories_query)
    cursor.execute(products_query)
    cursor.execute(carries_query)
    cursor.execute(customers_query)
    cursor.execute(orders_query)
    cursor.execute(olines_query)
    cursor.execute(deliveries_query)    
    connection.commit()

    return    
    