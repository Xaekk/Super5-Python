/*
SQLyog Ultimate v11.25 (64 bit)
MySQL - 5.0.96-community-nt : Database - superfive
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`superfive` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `superfive`;

/*Table structure for table `nums` */

DROP TABLE IF EXISTS `nums`;

CREATE TABLE `nums` (
  `id` int(225) NOT NULL auto_increment,
  `year` int(225) default NULL,
  `month` int(225) default NULL,
  `day` int(225) default NULL,
  `num1` int(225) default NULL,
  `num2` int(225) default NULL,
  `num3` int(225) default NULL,
  `num4` int(225) default NULL,
  `num5` int(225) default NULL,
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=796 DEFAULT CHARSET=utf8;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
