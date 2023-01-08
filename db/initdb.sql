/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `workout`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `workout` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `workout`;

--
-- Table structure for table `activity`
--
DROP TABLE IF EXISTS `activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `activity` (
  `id_activity` int unsigned NOT NULL AUTO_INCREMENT,
  `activityid` int NOT NULL,
  `name_activity` varchar(100) NOT NULL,
  `description` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id_activity`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
--
-- Dumping data for table `activity`
--
LOCK TABLES `activity` WRITE;
/*!40000 ALTER TABLE `activity` DISABLE KEYS */;
INSERT INTO `activity` VALUES (1,0,'Walking','Пешие прогулки'),(2,1,'Running','Беговые тренировки'),(3,2,'Cycling','Езда на велосипеде'),(4,3,'Cross-country skiing','Катание на беговых лыжах'),(5,11,'Hiking','Пеший туризм'),(6,12,'Roller skating','Катание на роликах'),(7,21,'Pool swimming','Плавание в бассейне'),(8,23,'Gym','Занятия гантелями'),(9,49,'Ice skating','Катание на коньках');
/*!40000 ALTER TABLE `activity` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workouts`
--
DROP TABLE IF EXISTS `workouts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workouts` (
  `id_workout` int unsigned NOT NULL AUTO_INCREMENT,
  `date_create` timestamp NOT NULL,
  `date_update` timestamp NULL DEFAULT NULL,
  `name` varchar(200) NOT NULL,
  `starttime` bigint NOT NULL,
  `stoptime` bigint NOT NULL,
  `totaltime` float NOT NULL,
  `activityid` int NOT NULL,
  `totaldistance` float DEFAULT NULL,
  `avgspeed` float DEFAULT NULL,
  `workoutkey` varchar(100) NOT NULL,
  `recoverytime` int DEFAULT NULL,
  `energy` int DEFAULT NULL,
  `export` tinyint NOT NULL DEFAULT '0',
  `description` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`id_workout`)
) ENGINE=InnoDB AUTO_INCREMENT=1915 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `workouts_gpx`
--
DROP TABLE IF EXISTS `workouts_gpx`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workouts_gpx` (
  `id_gpx` int unsigned NOT NULL AUTO_INCREMENT,
  `date_create` timestamp NOT NULL,
  `id_workout` int unsigned NOT NULL,
  `path_gpx` varchar(200) NOT NULL,
  PRIMARY KEY (`id_gpx`)
) ENGINE=InnoDB AUTO_INCREMENT=1898 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
