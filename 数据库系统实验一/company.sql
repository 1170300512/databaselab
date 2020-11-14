-- MySQL dump 10.13  Distrib 8.0.11, for Win64 (x86_64)
--
-- Host: localhost    Database: company
-- ------------------------------------------------------
-- Server version	8.0.11

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `department` (
  `DNO` int(11) NOT NULL,
  `DNAME` varchar(5) DEFAULT NULL,
  `MGRSSN` char(5) DEFAULT NULL,
  `MGRSTARTDATE` datetime DEFAULT NULL,
  PRIMARY KEY (`DNO`),
  KEY `index_name2` (`DNAME`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES (1,'研发部','12301','2016-01-01 00:00:00'),(2,'财务部','12311','2016-01-01 00:00:00'),(3,'人事部','12321','2016-01-01 00:00:00'),(4,'营销部','12331','2016-01-01 00:00:00'),(5,'公关部','12341','2016-01-01 00:00:00');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `employee` (
  `ESSN` char(5) NOT NULL,
  `ENAME` varchar(3) DEFAULT NULL,
  `ADDRESS` char(3) DEFAULT NULL,
  `SALARY` int(11) DEFAULT NULL,
  `SUPERSSN` char(5) DEFAULT NULL,
  `DNO` int(11) DEFAULT NULL,
  PRIMARY KEY (`ESSN`),
  KEY `FK_1` (`DNO`),
  KEY `index_name1` (`SALARY`),
  CONSTRAINT `FK_1` FOREIGN KEY (`DNO`) REFERENCES `department` (`dno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `employee`
--

LOCK TABLES `employee` WRITE;
/*!40000 ALTER TABLE `employee` DISABLE KEYS */;
INSERT INTO `employee` VALUES ('12301','张一','A01',7000,'12301',1),('12302','张二','A02',6000,'12301',1),('12303','张三','A03',6000,'12301',1),('12304','张四','A04',6000,'12301',1),('12305','张五','A05',6000,'12301',1),('12306','张六','A06',6000,'12301',1),('12307','张七','A07',6000,'12301',1),('12308','张八','A08',6000,'12301',1),('12309','张九','A09',2500,'12301',1),('12310','张十','A10',2600,'12301',1),('12311','宋一','B01',3000,'12311',2),('12312','宋二','B02',2500,'12311',2),('12313','宋三','B03',2100,'12311',2),('12314','宋四','B04',1700,'12311',2),('12315','宋五','B05',1700,'12311',2),('12316','宋六','B06',1700,'12311',2),('12317','宋七','B07',1500,'12311',2),('12318','宋八','B08',1500,'12311',2),('12319','宋九','B09',900,'12311',2),('12320','宋十','B10',900,'12311',2),('12321','李一','C01',10000,'12321',3),('12322','李二','C02',6000,'12321',3),('12323','李三','C03',6000,'12321',3),('12324','李四','C04',6000,'12321',3),('12325','李五','C05',6000,'12321',3),('12326','李六','C06',6000,'12321',3),('12327','李七','C07',6000,'12321',3),('12328','李八','C08',6000,'12321',3),('12329','李九','C09',6000,'12321',3),('12330','李十','C10',6000,'12321',3),('12331','周一','D01',10000,'12331',4),('12332','周二','D02',6000,'12331',4),('12333','周三','D03',6000,'12331',4),('12334','周四','D04',6000,'12331',4),('12335','周五','D05',6000,'12331',4),('12336','周六','D06',6000,'12331',4),('12337','周七','D07',6000,'12331',4),('12338','周八','D08',6000,'12331',4),('12339','周九','D09',6000,'12331',4),('12340','周十','D10',6000,'12331',4),('12341','王一','E01',10000,'12341',5),('12342','王二','E02',6000,'12341',5),('12343','王三','E03',6000,'12341',5),('12344','王四','E04',6000,'12341',5),('12345','王五','E05',6000,'12341',5),('12346','王六','E06',6000,'12341',5),('12347','王七','E07',6000,'12341',5),('12348','王八','E08',6000,'12341',5),('12349','王九','E09',6000,'12341',5),('12350','王十','E10',6000,'12341',5),('12360','赵四','F30',5000,'12301',1),('12370','赵五','P40',3000,'12301',1);
/*!40000 ALTER TABLE `employee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `project`
--

DROP TABLE IF EXISTS `project`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `project` (
  `PNO` char(3) NOT NULL,
  `PNAME` varchar(5) DEFAULT NULL,
  `PLOCATION` char(3) DEFAULT NULL,
  `DNO` int(11) DEFAULT NULL,
  PRIMARY KEY (`PNO`),
  KEY `FK_2` (`DNO`),
  KEY `index_name3` (`PNAME`),
  CONSTRAINT `FK_2` FOREIGN KEY (`DNO`) REFERENCES `department` (`dno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `project`
--

LOCK TABLES `project` WRITE;
/*!40000 ALTER TABLE `project` DISABLE KEYS */;
INSERT INTO `project` VALUES ('P1','A','F01',1),('P10','J','F10',5),('P2','B','F02',1),('P3','C','F03',2),('P4','D','F04',2),('P5','E','F05',3),('P6','F','F06',3),('P7','G','F07',4),('P8','H','F08',4),('P9','I','F09',5);
/*!40000 ALTER TABLE `project` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `works_on`
--

DROP TABLE IF EXISTS `works_on`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `works_on` (
  `ESSN` char(5) NOT NULL,
  `PNO` char(3) NOT NULL,
  `HOURS` int(11) DEFAULT NULL,
  PRIMARY KEY (`ESSN`,`PNO`),
  KEY `index_name4` (`ESSN`),
  KEY `index_name5` (`PNO`),
  CONSTRAINT `FK_3` FOREIGN KEY (`ESSN`) REFERENCES `employee` (`essn`),
  CONSTRAINT `FK_4` FOREIGN KEY (`PNO`) REFERENCES `project` (`pno`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `works_on`
--

LOCK TABLES `works_on` WRITE;
/*!40000 ALTER TABLE `works_on` DISABLE KEYS */;
INSERT INTO `works_on` VALUES ('12301','P1',10),('12302','P1',10),('12303','P1',10),('12304','P1',10),('12304','P10',1),('12304','P2',9),('12304','P3',8),('12304','P4',7),('12304','P5',6),('12304','P6',5),('12304','P7',4),('12304','P8',3),('12304','P9',2),('12305','P1',4),('12305','P2',5),('12305','P3',3),('12306','P1',10),('12306','P2',10),('12307','P2',4),('12307','P3',3),('12308','P2',10),('12309','P2',10),('12310','P2',10),('12311','P3',3),('12311','P4',2),('12311','P6',1),('12311','P9',1),('12312','P3',9),('12313','P3',9),('12314','P3',9),('12315','P3',9),('12316','P4',9),('12317','P4',9),('12318','P4',9),('12319','P4',9),('12320','P4',9),('12321','P5',8),('12322','P5',8),('12323','P5',8),('12324','P1',1),('12324','P10',10),('12324','P2',2),('12324','P3',3),('12324','P4',4),('12324','P5',5),('12324','P6',6),('12324','P7',7),('12324','P8',8),('12324','P9',9),('12325','P5',8),('12326','P6',8),('12327','P6',2),('12327','P7',1),('12327','P8',1),('12328','P6',8),('12329','P6',8),('12330','P6',8),('12331','P7',9),('12332','P7',9),('12333','P7',9),('12334','P7',9),('12335','P7',9),('12336','P8',9),('12337','P8',9),('12338','P8',9),('12339','P8',9),('12340','P8',9),('12341','P9',9),('12342','P9',9),('12343','P9',9),('12344','P1',3),('12344','P10',1),('12344','P2',5),('12344','P3',2),('12344','P4',1),('12344','P5',6),('12344','P6',5),('12344','P7',8),('12344','P8',3),('12344','P9',9),('12345','P9',9),('12346','P10',9),('12347','P10',9),('12348','P10',9),('12349','P10',9),('12350','P1',1),('12350','P10',1),('12350','P3',2),('12350','P6',2),('12350','P8',1);
/*!40000 ALTER TABLE `works_on` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-04 22:24:57
