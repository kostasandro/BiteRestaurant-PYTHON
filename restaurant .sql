-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: May 31, 2019 at 01:23 AM
-- Server version: 5.7.24
-- PHP Version: 7.2.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `restaurant`
--

-- --------------------------------------------------------

--
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
CREATE TABLE IF NOT EXISTS `customer` (
  `Customer_ID` int(11) NOT NULL AUTO_INCREMENT,
  `First_name` varchar(20) COLLATE utf8_bin NOT NULL,
  `Last_name` varchar(20) COLLATE utf8_bin NOT NULL,
  `Gender` varchar(10) COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`Customer_ID`)
) ENGINE=MyISAM AUTO_INCREMENT=23 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`Customer_ID`, `First_name`, `Last_name`, `Gender`) VALUES
(22, 'Kostakis', 'Andro', 'male'),
(21, 'Nikos', 'Lyras', 'male');

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS `employee`;
CREATE TABLE IF NOT EXISTS `employee` (
  `Employee_ID` int(11) NOT NULL AUTO_INCREMENT,
  `First_name` varchar(20) COLLATE utf8_bin NOT NULL,
  `Last_name` varchar(20) COLLATE utf8_bin NOT NULL,
  `Address` varchar(50) COLLATE utf8_bin NOT NULL,
  `Phone_number` int(11) NOT NULL,
  PRIMARY KEY (`Employee_ID`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`Employee_ID`, `First_name`, `Last_name`, `Address`, `Phone_number`) VALUES
(4, 'Konstantinos', 'Andronis', 'Gerakas', 69777771),
(3, 'Nikos', 'Lyras', 'Marousi', 7654433);

-- --------------------------------------------------------

--
-- Table structure for table `open_date`
--

DROP TABLE IF EXISTS `open_date`;
CREATE TABLE IF NOT EXISTS `open_date` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date_from` date NOT NULL,
  `date_to` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=31 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `open_date`
--

INSERT INTO `open_date` (`id`, `date_from`, `date_to`) VALUES
(28, '2020-03-01', '2020-03-31'),
(27, '2020-02-01', '2020-02-28'),
(26, '2020-01-01', '2020-01-31'),
(29, '2020-04-01', '2020-07-31'),
(30, '2020-08-01', '2020-12-31');

-- --------------------------------------------------------

--
-- Table structure for table `open_dates_hours`
--

DROP TABLE IF EXISTS `open_dates_hours`;
CREATE TABLE IF NOT EXISTS `open_dates_hours` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `open_date_id` int(11) NOT NULL,
  `work_hours_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `open_dates_hours`
--

INSERT INTO `open_dates_hours` (`id`, `open_date_id`, `work_hours_id`) VALUES
(14, 26, 24),
(13, 26, 23),
(12, 26, 22),
(15, 27, 25),
(16, 27, 26),
(17, 28, 27),
(18, 28, 28),
(19, 29, 29),
(20, 29, 30),
(21, 30, 31),
(22, 30, 32),
(23, 30, 33);

-- --------------------------------------------------------

--
-- Table structure for table `reservation`
--

DROP TABLE IF EXISTS `reservation`;
CREATE TABLE IF NOT EXISTS `reservation` (
  `Reservation_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Date` date NOT NULL,
  `Persons` int(11) NOT NULL,
  `Start_time` varchar(10) COLLATE utf8_bin NOT NULL,
  `Customer_ID` int(11) NOT NULL,
  `Employee_ID` int(11) DEFAULT NULL,
  `Status` int(11) NOT NULL,
  PRIMARY KEY (`Reservation_ID`),
  KEY `Customer_ID` (`Customer_ID`),
  KEY `Employee_ID` (`Employee_ID`),
  KEY `Table_ID` (`Status`)
) ENGINE=MyISAM AUTO_INCREMENT=23 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `reservation`
--

INSERT INTO `reservation` (`Reservation_ID`, `Date`, `Persons`, `Start_time`, `Customer_ID`, `Employee_ID`, `Status`) VALUES
(17, '2020-06-20', 6, '19:00:00', 21, 4, 2),
(18, '2020-06-11', 8, '13:00:00', 21, 3, 2),
(19, '2020-07-26', 2, '19:00:00', 21, 3, 2),
(20, '2020-06-15', 8, '19:00:00', 22, 4, 2),
(21, '2020-06-04', 10, '13:00:00', 22, 3, 3),
(22, '2020-06-01', 7, '13:00:00', 22, 4, 3);

-- --------------------------------------------------------

--
-- Table structure for table `reservation_table`
--

DROP TABLE IF EXISTS `reservation_table`;
CREATE TABLE IF NOT EXISTS `reservation_table` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Table_ID` int(11) NOT NULL,
  `Reservation_ID` int(11) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=33 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `reservation_table`
--

INSERT INTO `reservation_table` (`ID`, `Table_ID`, `Reservation_ID`) VALUES
(27, 4, 17),
(28, 1, 18),
(29, 3, 19),
(30, 1, 20),
(31, 2, 21),
(32, 1, 22);

-- --------------------------------------------------------

--
-- Table structure for table `res_table`
--

DROP TABLE IF EXISTS `res_table`;
CREATE TABLE IF NOT EXISTS `res_table` (
  `Table_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Capacity` int(11) NOT NULL,
  PRIMARY KEY (`Table_ID`)
) ENGINE=MyISAM AUTO_INCREMENT=8 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `res_table`
--

INSERT INTO `res_table` (`Table_ID`, `Capacity`) VALUES
(1, 9),
(2, 10),
(3, 3),
(4, 6),
(5, 3),
(6, 4),
(7, 3);

-- --------------------------------------------------------

--
-- Table structure for table `review`
--

DROP TABLE IF EXISTS `review`;
CREATE TABLE IF NOT EXISTS `review` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `Customer_ID` int(11) NOT NULL,
  `Comment` varchar(255) COLLATE utf8_bin NOT NULL,
  `Date` date NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `review`
--

INSERT INTO `review` (`ID`, `Customer_ID`, `Comment`, `Date`) VALUES
(3, 22, 'Poly euxaristos xwros kai wraia atmosfaira tha xanapaw!', '2020-05-31');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `User_ID` int(11) NOT NULL AUTO_INCREMENT,
  `Role` varchar(10) COLLATE utf8_bin NOT NULL,
  `Email` varchar(20) COLLATE utf8_bin NOT NULL,
  `Password` varchar(50) COLLATE utf8_bin NOT NULL,
  `Employee_ID` int(11) DEFAULT NULL,
  `Customer_ID` int(11) DEFAULT NULL,
  PRIMARY KEY (`User_ID`),
  KEY `Employee_ID` (`Employee_ID`),
  KEY `Customer_ID` (`Customer_ID`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`User_ID`, `Role`, `Email`, `Password`, `Employee_ID`, `Customer_ID`) VALUES
(8, '01', 'lyras@amc.gr', '1234lyras', NULL, 21),
(7, '02', 'Kandronis@amc.gr', 'Kandronis1234', 4, NULL),
(6, '02', 'Nlyras@amc.gr', 'Nlyras1234', 3, NULL),
(9, '01', 'Andronis@amc.gr', '1234Andronis', NULL, 22);

-- --------------------------------------------------------

--
-- Table structure for table `work_hours`
--

DROP TABLE IF EXISTS `work_hours`;
CREATE TABLE IF NOT EXISTS `work_hours` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hour_from` time NOT NULL,
  `hour_to` time NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=34 DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

--
-- Dumping data for table `work_hours`
--

INSERT INTO `work_hours` (`id`, `hour_from`, `hour_to`) VALUES
(24, '20:00:00', '23:00:00'),
(22, '15:00:00', '17:00:00'),
(23, '18:00:00', '20:00:00'),
(25, '14:00:00', '16:00:00'),
(26, '17:00:00', '19:00:00'),
(27, '14:00:00', '15:00:00'),
(28, '18:00:00', '22:00:00'),
(29, '13:00:00', '16:00:00'),
(30, '19:00:00', '23:00:00'),
(31, '15:00:00', '16:00:00'),
(32, '18:00:00', '19:00:00'),
(33, '20:00:00', '23:00:00');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
