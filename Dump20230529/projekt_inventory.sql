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
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS `inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inventory` (
  `prodID` int NOT NULL,
  `prodName` varchar(20) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `category` varchar(45) NOT NULL,
  `available` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inventory`
--

LOCK TABLES `inventory` WRITE;
/*!40000 ALTER TABLE `inventory` DISABLE KEYS */;
INSERT INTO `inventory` VALUES (1,'Mjölk',10.00,'Mejeri',66),(2,'Bröd',15.00,'Bageri',56),(3,'Yoghurt',12.00,'Mejeri',24),(4,'Ost',20.00,'Mejeri',31),(5,'Kaffe',25.00,'Drycker',24),(6,'Te',18.00,'Drycker',14),(7,'Kött',40.00,'Kött',81),(8,'Kyckling',30.00,'Kött',12),(9,'Fisk',35.00,'Kött',65),(10,'Ägg',8.00,'Mejeri',96),(11,'Smör',22.00,'Mejeri',65),(12,'Frukt',14.00,'Frukt och grönt',83),(13,'Grönsaker',16.00,'Frukt och grönt',40),(14,'Ris',10.00,'Spannmål',24),(15,'Pasta',12.00,'Spannmål',3),(16,'Soppa',15.00,'Konserver',42),(17,'Socker',8.00,'Bakning',81),(18,'Salt',6.00,'Bakning',56),(19,'Kryddor',10.00,'Bakning',31),(20,'Tvål',20.00,'Skönhetsprodukter',9),(21,'Schampo',25.00,'Skönhetsprodukter',48),(22,'Tandkräm',15.00,'Skönhetsprodukter',97),(23,'Tvättmedel',30.00,'Städning',97),(24,'Diskmedel',12.00,'Städning',16),(25,'Toalettpapper',18.00,'Hushållsartiklar',46),(26,'Hushållspapper',8.00,'Hushållsartiklar',26),(27,'Tvättlappar',10.00,'Hushållsartiklar',74),(28,'Plåster',6.00,'Hälsa och hygien',20),(29,'Solkräm',40.00,'Hälsa och hygien',17),(30,'Tvättmedel',30.00,'Städning',66),(31,'Borstar',15.00,'Städning',28),(32,'Batterier',25.00,'Elektronik',44),(33,'Lampor',12.00,'Elektronik',91),(34,'Rakblad',18.00,'Hälsa och hygien',30),(35,'Raklödder',10.00,'Hälsa och hygien',31),(36,'Rakhyvlar',20.00,'Hälsa och hygien',60),(37,'Paraply',35.00,'Kläder och accessoarer',94),(38,'Handdukar',30.00,'Hushållsartiklar',62),(39,'Strumpor',12.00,'Kläder och accessoarer',73),(40,'Trosor',15.00,'Kläder och accessoarer',55),(41,'Kalsonger',18.00,'Kläder och accessoarer',49),(42,'Skor',60.00,'Kläder och accessoarer',84),(43,'Tröjor',40.00,'Kläder och accessoarer',15),(44,'Byxor',50.00,'Kläder och accessoarer',32),(45,'Jackor',80.00,'Kläder och accessoarer',82),(46,'Vantar',25.00,'Kläder och accessoarer',82),(47,'Mössor',20.00,'Kläder och accessoarer',22),(142,'Pennor',34.00,'Kontorsmaterial',72);
/*!40000 ALTER TABLE `inventory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-05-29  0:42:49
