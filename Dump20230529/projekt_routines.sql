-- MySQL dump 10.13  Distrib 8.0.33, for Win64 (x86_64)
--
-- Host: localhost    Database: projekt
-- ------------------------------------------------------
-- Server version	8.0.33

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Dumping routines for database 'projekt'
--
/*!50003 DROP PROCEDURE IF EXISTS `CheckCart` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `CheckCart`(IN cartID INT)
BEGIN
    DECLARE prodItem VARCHAR(100);
    DECLARE done INT DEFAULT FALSE;
 
    DECLARE cursorCartItems CURSOR FOR
        SELECT prodList FROM cart WHERE uniqueID = cartID;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

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

        WHILE LENGTH(prodItem) > 0 DO
            SET @pos := LOCATE(',', prodItem);

            IF @pos = 0 THEN
                SET @item := prodItem;
                SET prodItem := '';
            ELSE
                SET @item := SUBSTRING(prodItem, 1, @pos - 1);
                SET prodItem := SUBSTRING(prodItem, @pos + 1);
            END IF;

            SET @itemPrice := (SELECT price FROM inventory WHERE prodID = TRIM(@item));
            SET @itemAvailable := (SELECT available FROM inventory WHERE prodID = TRIM(@item));

            IF @itemPrice IS NOT NULL THEN

                SET @memberType := (SELECT memberType FROM customers WHERE uniqueID = cartID);
                SET @discount := (SELECT discount FROM discounts WHERE prodID = TRIM(@item) AND FIND_IN_SET(@memberType, memberType));

                IF @discount IS NOT NULL THEN
                    SET @itemPrice := @itemPrice * @discount;
                END IF;

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
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `CheckFav` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `CheckFav`(IN cartID INT)
BEGIN
    DECLARE prodItem VARCHAR(100);
    DECLARE done INT DEFAULT FALSE;
 
    DECLARE cursorFavItems CURSOR FOR
        SELECT favoriteProd FROM customers WHERE uniqueID = cartID;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    CREATE TEMPORARY TABLE IF NOT EXISTS favorites (
        item VARCHAR(100),
        price DECIMAL(10, 2)
    );

    OPEN cursorFavItems;

    read_loop: LOOP
        FETCH cursorFavItems INTO prodItem;

        IF done THEN
            LEAVE read_loop;
        END IF;

        WHILE LENGTH(prodItem) > 0 DO
            SET @pos := LOCATE(',', prodItem);

            IF @pos = 0 THEN
                SET @item := prodItem;
                SET prodItem := '';
            ELSE
                SET @item := SUBSTRING(prodItem, 1, @pos - 1);
                SET prodItem := SUBSTRING(prodItem, @pos + 1);
            END IF;

            SET @itemPrice := (SELECT price FROM inventory WHERE prodID = TRIM(@item));

            IF @itemPrice IS NOT NULL THEN
                -- Item exists in the inventory, add it to the temporary table
                INSERT INTO favorites (item, price) VALUES ((SELECT prodName FROM inventory WHERE prodID = TRIM(@item)), @itemPrice);
            END IF;

        END WHILE;

    END LOOP;

    CLOSE cursorFavItems;

    SELECT * FROM favorites;

    DROP TABLE IF EXISTS favorites;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-29  0:42:50
