import mysqlx
from mysqlx.errors import DatabaseError

# Connect to server on localhost
session = mysqlx.get_session({
    "host": "localhost",
    "port": 33060,
    "user": "root",
    "password": "testing1234"
})

DB_NAME = 'projekt'
session.sql("USE {}".format(DB_NAME)).execute()

cart_insert_trigger = """
CREATE TRIGGER insert_into_cart AFTER INSERT ON customers
FOR EACH ROW
BEGIN
    INSERT INTO cart (uniqueID, prodlist) VALUES (NEW.uniqueID, '');
    UPDATE cart SET prodlist = '' WHERE uniqueID = (SELECT uniqueID FROM customers ORDER BY uniqueID DESC LIMIT 1);
END;
"""


try:
        print("Creating trigger insert_into_cart: ")
        session.sql(cart_insert_trigger).execute()
except DatabaseError as de:
    if de.errno == 1050:
        print("insert_into_cart already exists.")
    else:
        print(de.msg)
else:
    print("OK")

cart_delete_trigger = """before_delete 
before delete on customers
for each row
delete from cart where uniqueID = old.uniqueID;"""
        
try:
    session.sql(cart_delete_trigger).execute()
except:
    print("this trigger already exits")

create_check_cart = "DELIMITER // "\
"CREATE PROCEDURE CheckCart(IN cartID INT)"\
"BEGIN "\
"    DECLARE prodItem VARCHAR(100);"\
"    DECLARE done INT DEFAULT FALSE;"\
"    DECLARE cursorCartItems CURSOR FOR"\
"        SELECT prodList FROM cart WHERE uniqueID = cartID;"\
"    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;"\
"    CREATE TEMPORARY TABLE IF NOT EXISTS tempItemPrices ( "\
"        item VARCHAR(100), "\
"        price DECIMAL(10, 2), "\
"        available INT "\
"    ); "\
"    OPEN cursorCartItems; "\
"    read_loop: LOOP"\
"        FETCH cursorCartItems INTO prodItem; "\
"        IF done THEN "\
"            LEAVE read_loop; "\
"        END IF;"\
"        WHILE LENGTH(prodItem) > 0 DO"\
"            SET @pos := LOCATE(',', prodItem);"\
"            IF @pos = 0 THEN "\
"                SET @item := prodItem; "\
"                SET prodItem := '';"\
"            ELSE"\
"                SET @item := SUBSTRING(prodItem, 1, @pos - 1); "\
"                SET prodItem := SUBSTRING(prodItem, @pos + 1); "\
"            END IF; "\
"            SET @itemPrice := (SELECT price FROM inventory WHERE prodID = TRIM(@item));"\
"            SET @itemAvailable := (SELECT available FROM inventory WHERE prodID = TRIM(@item));"\
"            IF @itemPrice IS NOT NULL THEN "\
"                SET @memberType := (SELECT memberType FROM customers WHERE uniqueID = cartID);"\
"                SET @discount := (SELECT discount FROM discounts WHERE prodID = TRIM(@item) AND FIND_IN_SET(@memberType, memberType)); "\
"                IF @discount IS NOT NULL THEN "\
"                    SET @itemPrice := @itemPrice * @discount; "\
"                END IF; "\
"                INSERT INTO tempItemPrices (item, price, available) VALUES (TRIM(@item), @itemPrice, @itemAvailable); "\
"            END IF; "\
"        END WHILE; "\
"    END LOOP; "\
"   CLOSE cursorCartItems; "\
"   create table realCart( "\
"    item VARCHAR(100) default 0, "\
"    price Decimal(10,2) default 0.0, "\
"    quantity INT default 0 "\
" ); "\
"	insert into realCart "\
"	select * from  tempItemPrices;"\
"	UPDATE realCart t"\
"	JOIN ("\
"		SELECT item, COUNT(item) AS quantity, price"\
"		FROM tempItemPrices"\
"		GROUP BY price, item"\
"	) AS sub ON t.item = sub.item"\
"	SET t.item = (select prodName from inventory where prodID = t.item), t.quantity = sub.quantity, t.price = t.price * sub.quantity;"\
"	INSERT INTO realCart (item, price, quantity) VALUES ('Total', (select sum(price) from tempItemPrices), NULL);"\
"	select distinct * from realcart;"\
"   drop table realCart;"\
"   drop table tempItemPrices;"\
"END // "\
"DELIMITER ;"\

try:
        print("Creating trigger insert_into_cart: ")
        session.sql(create_check_cart).execute()
except DatabaseError as de:
    if de.errno == 1304:
        print("create cart already exists.")
    else:
        print(de.msg)


create_check_fav = "DELIMITER // "\
"CREATE PROCEDURE CheckFav(IN cartID INT) "\
"BEGIN "\
"    DECLARE prodItem VARCHAR(100); "\
"    DECLARE done INT DEFAULT FALSE; "\
"    DECLARE cursorFavItems CURSOR FOR "\
"        SELECT favoriteProd FROM customers WHERE uniqueID = cartID;"\
"    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE; "\
"    CREATE TEMPORARY TABLE IF NOT EXISTS favorites ( "\
"        item VARCHAR(100), "\
"        price DECIMAL(10, 2) "\
"    );"\
"    OPEN cursorFavItems; "\
"    read_loop: LOOP "\
"        FETCH cursorFavItems INTO prodItem;"\
"        IF done THEN"\
"            LEAVE read_loop;"\
"        END IF;"\
"        WHILE LENGTH(prodItem) > 0 DO"\
"            SET @pos := LOCATE(',', prodItem);"\
"            IF @pos = 0 THEN"\
"                SET @item := prodItem;"\
"                SET prodItem := '';"\
"            ELSE"\
"                SET @item := SUBSTRING(prodItem, 1, @pos - 1);"\
"                SET prodItem := SUBSTRING(prodItem, @pos + 1);"\
"            END IF;"\
"            SET @itemPrice := (SELECT price FROM inventory WHERE prodID = TRIM(@item));"\
"            IF @itemPrice IS NOT NULL THEN"\
"                INSERT INTO favorites (item, price) VALUES ((SELECT prodName FROM inventory WHERE prodID = TRIM(@item)), @itemPrice);"\
"           END IF;"\
"        END WHILE;"\
"    END LOOP;"\
"    CLOSE cursorFavItems;"\
"   SELECT * FROM favorites;"\
"    DROP TABLE IF EXISTS favorites;"\
"END //"\

try:
        print("Creating trigger favt: ")
        session.sql(create_check_cart).execute()
except DatabaseError as de:
    if de.errno == 1304:
        print("create fav already exists.")
    else:
        print(de.msg)


# query med JOIN
mailing_list = "SELECT uniqueID, mail, discounts.prodName, discounts.discount " \
        "FROM customers " \
        "LEFT JOIN discounts " \
        "on discounts.memberType like concat('%',customers.memberType,'%') and customers.favoriteProd like concat('%',discounts.prodName,'%') " \
        "or discounts.memberType like concat('%',customers.memberType,'%') and customers.favoriteCategory like concat('%',discounts.category,'%') " \
        "or discounts.memberType = 'none' and customers.favoriteProd like concat('%',discounts.prodName,'%') " \
        "or discounts.memberType = 'none' and customers.favoritecategory like concat('%',discounts.category,'%'); " \



discount_query = "SELECT discounts.prodName, discounts.discount "\
"FROM customers "\
"LEFT JOIN discounts "\
"    ON discounts.memberType LIKE CONCAT('%', customers.memberType, '%') "\
"    or discounts.memberType = 'none'"



