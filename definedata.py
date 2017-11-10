import sqlite3
import time
import hashlib

def define(connection,cursor):
    # function puts all of our test data into the database
    
    cursor.executescript("""insert into agents values -- aid,name,pwd
('00001','Jack','123456'),
('00002','Peter','654321'),
('00003','Tom','678910'),
('00004','Tony','456789'),
('00005', 'Monica','234567');

insert into stores values --sid,name,phone,address
(101,'Walmart','5879314567','9023 112 Ave Jasper'),
(102,'Sobey','7802347854','9402 101 Ave Jasper'),
(103,'Safeway','7809873456','9102 98 Ave Jasper'),
(104,'Bestbuy','7806324634','9324 121 Ave Jasper');

insert into categories values --cat,name
('dai','dairy'),
('med', 'medicine'),
('ele','electronics'),
('mea','meat'),
('del','deli'),
('fru','fruit'),
('veg','vegetable'),
('kit','kitchen ware');

insert into customers values --cid,name,address,pwd
('10001','Rose','9111 102 ST Edmonton','188745'),
('10002','Kirk','9112 102 ST Edmonton','123478'),
('10003','James','9113 103 ST Edmonton','789123'),
('10004','Lars','9114 104 ST Edmonton','876543'),
('10005','Levine','9115 105 ST Edmonton','873443'),
('10006','Terence','9122 105 ST Jasper','678910'),
('10007','Tim','9122 100 ST Jasper','456789'),
('10008', 'Mary','9123 122 ST Jasper','234567'),
('10009', 'Jassica','9124 121 ST Jasper','345678'),
('10010', 'Levy','9125 123 ST Jasper','456789');


insert into products values --pid,name,unit,cat
('p001','2L milk','ea','dai'),
('p002','white eggs','ea','dai'),
('p003','goat cheese','ea','dai'),

('p004','vitamins','ea','med'),
('p005','calcium','ea','med'),

('p006','iphone7','ea','ele'),
('p007','38 inch TV','ea','ele'),
('p008','Macbook','ea','ele'),

('p009','pork','kg','mea'),
('p010','chicken breast','kg','mea'),
('p011','lamb','kg','mea'),
('p012','beef','kg','mea'),
('p013','ground beef','kg','mea'),
('p014','ground pork','kg','mea'),
('p015','chicken leg','kg','mea'),
('p016','duck breast','kg','mea'),

('p017','taco','kg','del'),
('p018','roast duck','kg','del'),
('p019','burrito','kg','del'),
('p020','pizza','kg','del'),

('p021','strawberry','kg','fru'),
('p022','grape','kg','fru'),
('p023','banana','kg','fru'),
('p024','apple','kg','fru'),

('p025','potato','kg','veg'),
('p026','lettuce','kg','veg'),
('p027','cucumber','kg','veg'),

('p028','fork','ea','kit'),
('p029','spoon','ea','kit'),
('p030','chopstick','ea','kit');

insert into carries values --sid,pid,qty,uprice
(101,'p001',50,3.8),
(102,'p001',70,0.99),
(103,'p001', 80, 1.7),
(104,'p001', 80, 1.7),

(101,'p002',100,2.8),
(103,'p002', 180, 2.7),
(104,'p002', 150, 2.7),

(101,'p003',100,6.8),
(102,'p003', 180, 5.7),
(103,'p003', 150, 5.7),

(104,'p004',10,6.4),
(102,'p004', 18, 5.4),
(103,'p004', 15, 4.4),

(101,'p005',50,3.8),
(102,'p005',70,4.99),

(101,'p006', 80, 599),
(103,'p006', 80, 599),

(101,'p007', 6, 999),
(104,'p007', 8, 1999),

(101,'p008', 30, 1199),
(104,'p008', 50, 1099),

(102,'p009', 60, 12.99),
(103,'p009', 80, 11.99),

(102,'p010', 90, 12.99),
(104,'p010', 100, 11.99),

(103,'p011', 190, 20.99),
(104,'p011', 200, 18.99),

(101,'p012',50, 13.8),

(102,'p013',70, 8.99),

(103,'p014', 190, 6.99),

(104,'p015', 200, 7.99),

(101,'p016',50,3.8),
(102,'p016',70,0.99),
(103,'p016', 80, 1.7),
(104,'p016', 80, 1.7),

(101,'p017',100,2.8),
(103,'p017', 180, 2.7),
(104,'p017', 150, 2.7),

(101,'p018',100,6.8),
(102,'p018', 180, 5.7),
(103,'p018', 150, 5.7),

(104,'p019',10,6.4),
(102,'p019', 18, 5.4),
(103,'p019', 15, 4.4),

(101,'p020',50,3.8),
(102,'p020',70,4.99),

(101,'p021', 80, 5.99),
(103,'p021', 80, 5.99),

(101,'p022', 6, 9.99),
(104,'p022', 8, 1.99),

(101,'p023', 30, 1.99),
(104,'p023', 50, 1.99),

(102,'p024', 60, 2.99),
(103,'p024', 80, 1.99),

(102,'p025', 90, 1.99),
(104,'p025', 100, 1.99),

(103,'p026', 190, 2.99),
(104,'p026', 200, 1.99),

(101,'p027',50, 13.8),

(102,'p028',70, 1.99),

(103,'p029', 190, 2.99),

(104,'p030', 200, 1.99);""")
    
    connection.commit()
    return
