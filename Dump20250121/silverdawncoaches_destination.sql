-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: silverdawncoaches
-- ------------------------------------------------------
-- Server version	8.4.0

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
-- Table structure for table `destination`
--

DROP TABLE IF EXISTS `destination`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `destination` (
  `destination_id` int NOT NULL AUTO_INCREMENT,
  `destination_name` varchar(100) NOT NULL,
  `destination_hotel` varchar(100) DEFAULT NULL,
  `destination_cost` float NOT NULL,
  `destination_city` varchar(100) NOT NULL,
  `number_of_days` int NOT NULL,
  PRIMARY KEY (`destination_id`),
  UNIQUE KEY `destination_id_UNIQUE` (`destination_id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `destination`
--

LOCK TABLES `destination` WRITE;
/*!40000 ALTER TABLE `destination` DISABLE KEYS */;
INSERT INTO `destination` VALUES (1,'1','1',1,'1',1),(2,'Hilton Hotel - Glasgow','Hilton',30,'Glasgow',3),(3,'Chester - Roman Trip','Grosvenor',199,'Chester',2),(4,'Norwich','',20,'Norwich',1),(5,'Winchester','',27,'Winchester',1),(6,'Salisbury','',27,'Salisbury',1),(7,'Calais Shopping Trip','',39,'Calais',1),(8,'Edinburgh Hogmanay','Hilton',399,'Edinburgh',3),(9,'Cardiff the Welsh Capital','Royal Welsh',299,'Cardiff',3),(10,'York City Visit','Fenland Hotel',299,'York',3),(11,'Lincoln Xmas Market','White Hart',199,'Lincoln',2),(12,'Torquay Break','The Cliffdown',299,'Torquay',3),(13,'Sunny Brighton','',25,'Brighton',1);
/*!40000 ALTER TABLE `destination` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-01-21 11:34:38
