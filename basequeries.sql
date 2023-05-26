


create database projekt;

create table customers (uniqueID int not null auto_increment, 
customerName varchar(20) not null, mail varchar(20) not null,
memberType varchar(20) not null, favoriteProd varchar(250),
favoriteCategory varchar(250), joindate date, primary key(uniqueID));

create table inventory (prodID int not null,
prodName varchar(20) not null, price decimal(10, 2) not null, category varchar(45) not null, available int(6));

create table discounts(discountID int not null auto_increment,prodID int not null,
 ProdName varchar(20) not null, category varchar(79) not null, discount DECIMAL(3,2), memberType varchar(20) not null, primary key(discountID));

create table cart(uniqueID int not null, prodlist varchar(170) default "", foreign key (uniqueID) references customers(uniqueID)); 

CREATE TRIGGER insert_into_cart AFTER INSERT ON customers
FOR EACH ROW
INSERT INTO cart (uniqueID, prodlist) VALUES (NEW.uniqueID, '');
UPDATE cart SET prodlist = 'new_product' WHERE uniqueID = (SELECT uniqueID FROM customers ORDER BY uniqueID DESC LIMIT 1);

CREATE TRIGGER before_delete 
before delete on customers
for each row
delete from cart where uniqueID = old.uniqueID;

INSERT INTO inventory (prodID, prodName, category, price, available)
VALUES
  (1, 'Mjölk', 'Mejeri', 10, 66),
  (2, 'Bröd', 'Bageri', 15, 56),
  (3, 'Yoghurt', 'Mejeri', 12, 24),
  (4, 'Ost', 'Mejeri', 20, 31),
  (5, 'Kaffe', 'Drycker', 25, 24),
  (6, 'Te', 'Drycker', 18, 14),
  (7, 'Kött', 'Kött', 40, 81),
  (8, 'Kyckling', 'Kött', 30, 12),
  (9, 'Fisk', 'Kött', 35, 65),
  (10, 'Ägg', 'Mejeri', 8, 96),
  (11, 'Smör', 'Mejeri', 22, 65),
  (12, 'Frukt', 'Frukt och grönt', 14, 83),
  (13, 'Grönsaker', 'Frukt och grönt', 16, 40),
  (14, 'Ris', 'Spannmål', 10, 24),
  (15, 'Pasta', 'Spannmål', 12, 3),
  (16, 'Soppa', 'Konserver', 15, 42),
  (17, 'Socker', 'Bakning', 8, 81),
  (18, 'Salt', 'Bakning', 6, 56),
  (19, 'Kryddor', 'Bakning', 10, 31),
  (20, 'Tvål', 'Skönhetsprodukter', 20, 9),
  (21, 'Schampo', 'Skönhetsprodukter', 25, 48),
  (22, 'Tandkräm', 'Skönhetsprodukter', 15, 97),
  (23, 'Tvättmedel', 'Städning', 30, 97),
  (24, 'Diskmedel', 'Städning', 12, 16),
  (25, 'Toalettpapper', 'Hushållsartiklar', 18, 46),
  (26, 'Hushållspapper', 'Hushållsartiklar', 8, 26),
  (27, 'Tvättlappar', 'Hushållsartiklar', 10, 74),
  (28, 'Plåster', 'Hälsa och hygien', 6, 20),
  (29, 'Solkräm', 'Hälsa och hygien', 40, 17),
  (30, 'Tvättmedel', 'Städning', 30, 66),
  (31, 'Borstar', 'Städning', 15, 28),
  (32, 'Batterier', 'Elektronik', 25, 44),
  (33, 'Lampor', 'Elektronik', 12, 91),
  (34, 'Rakblad', 'Hälsa och hygien', 18, 30),
  (35, 'Raklödder', 'Hälsa och hygien', 10, 31),
  (36, 'Rakhyvlar', 'Hälsa och hygien', 20, 60),
  (37, 'Paraply', 'Kläder och accessoarer', 35, 94),
  (38, 'Handdukar', 'Hushållsartiklar', 30, 62),
  (39, 'Strumpor', 'Kläder och accessoarer', 12, 73),
  (40, 'Trosor', 'Kläder och accessoarer', 15, 55),
  (41, 'Kalsonger', 'Kläder och accessoarer', 18, 49),
  (42, 'Skor', 'Kläder och accessoarer', 60, 84),
  (43, 'Tröjor', 'Kläder och accessoarer', 40, 15),
  (44, 'Byxor', 'Kläder och accessoarer', 50, 32),
  (45, 'Jackor', 'Kläder och accessoarer', 80, 82),
  (46, 'Vantar', 'Kläder och accessoarer', 25, 82),
  (47, 'Mössor', 'Kläder och accessoarer', 20, 22),
  (48, 'Halsdukar', 'Kläder och accessoarer', 15, 15);


insert into customers (customerName, mail, memberType, favoriteProd, favoriteCategory, joindate) 
values ("Felix Davidsson", "felix@mail.com", "student","Ris, Ägg","Skönhetsprodukter", "2023-05-05");
insert into customers (customerName, mail, memberType, favoriteProd, favoriteCategory, joindate) 
values ("Dennis", "dennis@mail.com", "student", "", "Frukt och grönt",  "2023-05-05");
insert into customers (customerName, mail, memberType, favoriteProd, favoriteCategory, joindate) 
values ("martin", "martin@mail.com", "guld", "Läsk, Glass", "Bakning", "2023-05-05");
insert into customers (customerName, mail, memberType, favoriteProd, favoriteCategory, joindate) 
values ("martina", "martina@mail.com", "senior","Sallad", "Mejeri", "2023-05-05");

insert into discounts (prodID, ProdName, category, discount, memberType) values (22, "Tandkräm","Skönhetsprodukter", 0.9, "student");
insert into discounts (prodID, ProdName, category, discount, memberType) values (29, "Solkräm","Hälsa och hygien", 0.75, "student, senior");
insert into discounts (prodID, ProdName, category, discount, memberType) values (12, "Frukt","Frukt och grönt", 0.9, "senior");
insert into discounts (prodID, ProdName, category, discount, memberType) values (32, "Batterier","Elektronik", 0.8, "none");
insert into discounts (prodID, ProdName, category, discount, memberType) values (14, "Ris","Spannmål", 0.8, "senior, guld");
insert into discounts (prodID, ProdName, category, discount, memberType) values (12, "Frukt","Frukt och grönt", 0.0, "student");
insert into discounts (prodID, ProdName, category, discount, memberType) values (46, "vantar","Kläder och accessoarer", 0.8, "guld");
select * from customers;
select * from inventory;
select * from discounts;

UPDATE cart
SET prodList = '18, 1, 22, 1, 29, 29, 99'
WHERE uniqueID = 1;
UPDATE cart 
SET prodList = '18, 22, 1, 29, 99'
WHERE uniqueID = 2;

SELECT uniqueID, mail, discounts.prodName, discounts.discount
FROM customers
LEFT JOIN discounts
on discounts.memberType like concat('%',customers.memberType,'%') and customers.favoriteProd like concat('%',discounts.prodName,'%') 
or discounts.memberType like concat('%',customers.memberType,'%') and customers.favoriteCategory like concat('%',discounts.category,'%') 
or discounts.memberType = "none" and customers.favoriteProd like concat('%',discounts.prodName,'%')
or discounts.memberType = "none" and customers.favoritecategory like concat('%',discounts.category,'%');

select category, sum(availiable) as total from inventory group by category; 




