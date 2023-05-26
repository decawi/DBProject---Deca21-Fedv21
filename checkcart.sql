DELIMITER //

CREATE PROCEDURE CheckCart(IN cartID INT)
BEGIN
    DECLARE prodItem VARCHAR(100);
    DECLARE done INT DEFAULT FALSE;
 

    DECLARE cursorCartItems CURSOR FOR
        SELECT prodList FROM cart WHERE uniqueID = cartID;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Temporary table to store item details
    CREATE TEMPORARY TABLE IF NOT EXISTS tempItemPrices (
        item VARCHAR(100),
        price DECIMAL(10, 2),
        available INT
    );

    OPEN cursorCartItems;

    read_loop: LOOP
        FETCH cursorCartItems INTO prodItem;

        IF done THEN
            LEAVE read_loop;
        END IF;

        -- Process the current item
        WHILE LENGTH(prodItem) > 0 DO
            SET @pos := LOCATE(',', prodItem);

            IF @pos = 0 THEN
                SET @item := prodItem;
                SET prodItem := '';
            ELSE
                SET @item := SUBSTRING(prodItem, 1, @pos - 1);
                SET prodItem := SUBSTRING(prodItem, @pos + 1);
            END IF;

            -- Retrieve the price and availability of the item from the inventory table
            SET @itemPrice := (SELECT price FROM inventory WHERE prodID = TRIM(@item));
            SET @itemAvailable := (SELECT available FROM inventory WHERE prodID = TRIM(@item));

            IF @itemPrice IS NOT NULL THEN
                -- Apply discounts based on customer's memberType
                SET @memberType := (SELECT memberType FROM customers WHERE uniqueID = cartID);
                SET @discount := (SELECT discount FROM discounts WHERE prodID = TRIM(@item) AND FIND_IN_SET(@memberType, memberType));

                IF @discount IS NOT NULL THEN
                    SET @itemPrice := @itemPrice * @discount;
                END IF;

                -- Item exists in the inventory, add it to the temporary table
                INSERT INTO tempItemPrices (item, price, available) VALUES (TRIM(@item), @itemPrice, @itemAvailable);
                
            END IF;

        END WHILE;

    END LOOP;

    CLOSE cursorCartItems;
    
    create table realCart(
    item VARCHAR(100) default 0,
    price Decimal(10,2) default 0.0,
    quantity INT default 0
);

	insert into realCart 
	select * from  tempItemPrices;

	UPDATE realCart t
	JOIN (
		SELECT item, COUNT(item) AS quantity, price
		FROM tempItemPrices
		GROUP BY price, item
	) AS sub ON t.item = sub.item
	SET t.item = (select prodName from inventory where prodID = t.item), t.quantity = sub.quantity, t.price = t.price * sub.quantity;

	INSERT INTO realCart (item, price, quantity) VALUES ('Total', (select sum(price) from tempItemPrices), NULL);

	select distinct * from realcart;
    
    drop table realCart;
    drop table tempItemPrices;
END //

DELIMITER ;
CALL CheckCart(1);



