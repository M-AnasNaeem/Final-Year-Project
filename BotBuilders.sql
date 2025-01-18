-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Oct 27, 2024 at 10:53 AM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `BotBuilders`
--

-- --------------------------------------------------------

--
-- Table structure for table `ACCOUNT`
--

CREATE TABLE `ACCOUNT` (
  `Account_id` int(6) NOT NULL,
  `Create_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ACCOUNT`
--

INSERT INTO `ACCOUNT` (`Account_id`, `Create_date`) VALUES
(100001, '2024-10-26 17:57:13'),
(100002, '2024-10-26 17:57:48'),
(100003, '2024-10-26 17:57:48'),
(100004, '2024-10-26 17:58:43'),
(100005, '2024-10-26 17:58:43'),
(100006, '2024-10-26 17:59:00'),
(100007, '2024-10-26 17:59:00');

-- --------------------------------------------------------

--
-- Table structure for table `ARRIVED_CAR`
--

CREATE TABLE `ARRIVED_CAR` (
  `Arrived_car_id` int(6) NOT NULL,
  `Car_id` int(6) NOT NULL,
  `Warehouse_id` int(6) NOT NULL,
  `Towing_status_id` int(6) NOT NULL,
  `Delivered_date` varchar(255) NOT NULL,
  `Delivered_title` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ARRIVED_CAR`
--

INSERT INTO `ARRIVED_CAR` (`Arrived_car_id`, `Car_id`, `Warehouse_id`, `Towing_status_id`, `Delivered_date`, `Delivered_title`) VALUES
(1, 1, 300652, 1, '2024-10-10', 1),
(2, 2, 300652, 1, '2024-10-10', 1),
(3, 3, 300652, 2, '2024-10-10', 1),
(4, 4, 693974, 2, '2024-10-20', 1),
(5, 5, 693974, 1, '2024-10-20', 1),
(6, 6, 300652, 2, '2024-10-10', 1),
(7, 7, 693974, 1, '2024-10-20', 1);

-- --------------------------------------------------------

--
-- Table structure for table `AUCTION`
--

CREATE TABLE `AUCTION` (
  `Auction_id` int(6) NOT NULL,
  `Account_id` int(6) NOT NULL,
  `Title` varchar(255) NOT NULL,
  `Create_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `Update_date` timestamp NULL DEFAULT current_timestamp(),
  `US_dollar_rate` float(7,5) NOT NULL,
  `Status` tinyint(4) NOT NULL,
  `Create_by` int(6) NOT NULL,
  `Auction_transfer_currency` int(255) NOT NULL,
  `Auction_transfer_rate` float(7,5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `AUCTION`
--

INSERT INTO `AUCTION` (`Auction_id`, `Account_id`, `Title`, `Create_date`, `Update_date`, `US_dollar_rate`, `Status`, `Create_by`, `Auction_transfer_currency`, `Auction_transfer_rate`) VALUES
(1, 100002, '2016 Hyundai Elantra', '2024-10-26 18:25:33', NULL, 3.67250, 0, 200007, 840, 0.98234),
(2, 100003, '2019 Subaru Outback', '2024-10-26 18:25:33', NULL, 3.67250, 1, 200006, 840, 1.07543),
(3, 100001, '2018 GMC Sierra', '2024-10-26 18:25:33', NULL, 3.67250, 2, 200005, 840, 1.21562),
(4, 100006, '2015 Volkswagen Jetta', '2024-10-26 18:25:33', NULL, 3.67250, 2, 200004, 124, 1.07543),
(5, 100004, '2020 Mazda CX-5', '2024-10-26 18:25:33', NULL, 3.67250, 0, 200003, 124, 1.07543),
(6, 100007, '2018 BMW X3', '2024-10-26 18:25:33', NULL, 3.67250, 1, 200001, 840, 1.21562),
(7, 100005, '2019 Ford Explorer', '2024-10-26 18:25:33', NULL, 3.67250, 2, 200002, 124, 0.98234);

-- --------------------------------------------------------

--
-- Table structure for table `AUCTION_LOCATION`
--

CREATE TABLE `AUCTION_LOCATION` (
  `Auction_location_id` int(6) NOT NULL,
  `Auction_location_name` varchar(255) NOT NULL,
  `Auction_id` int(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `AUCTION_LOCATION`
--

INSERT INTO `AUCTION_LOCATION` (`Auction_location_id`, `Auction_location_name`, `Auction_id`) VALUES
(1, 'Los Angeles, CA, USA', 1),
(2, 'Miami, FL, USA', 2),
(3, 'New York, NY, USA\r\n', 3),
(4, 'Vancouver, BC, Canada', 4),
(5, 'Toronto, ON, Canada', 5),
(6, 'Chicago, IL, USA\r\n', 6),
(7, 'Calgary, AB, Canada', 7);

-- --------------------------------------------------------

--
-- Table structure for table `BILL`
--

CREATE TABLE `BILL` (
  `Bill_id` int(6) NOT NULL,
  `Customer_id` int(6) NOT NULL,
  `Total_amount` double(10,2) NOT NULL,
  `Total_required` double(10,2) NOT NULL,
  `Remaining_amount` double(10,2) DEFAULT NULL,
  `Description` text DEFAULT NULL,
  `Inv_no` varchar(50) NOT NULL,
  `Inv_type` varchar(50) NOT NULL,
  `inv_file` text DEFAULT NULL,
  `Payment_method` varchar(50) NOT NULL,
  `Advanced` float(10,2) DEFAULT NULL,
  `Deposit` int(6) DEFAULT NULL,
  `Receipt_journal` int(6) DEFAULT NULL,
  `Create_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Create_by` int(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `BILL`
--

INSERT INTO `BILL` (`Bill_id`, `Customer_id`, `Total_amount`, `Total_required`, `Remaining_amount`, `Description`, `Inv_no`, `Inv_type`, `inv_file`, `Payment_method`, `Advanced`, `Deposit`, `Receipt_journal`, `Create_date`, `Create_by`) VALUES
(700010, 1, 14000.00, 14000.00, NULL, 'Payment for auction 1: 2016 Hyundai Elantra', 'INV001', 'Auction Payment', NULL, 'Credit Card', NULL, NULL, NULL, '2024-09-01 06:15:23', 200001),
(700011, 2, 20000.00, 28000.00, 8000.00, 'Payment for auction 2: 2019 Subaru Outback', 'INV002', 'Auction Payment', NULL, 'Cash', 5000.00, 500, NULL, '2024-09-12 10:30:45', 200002),
(700012, 3, 32000.00, 32000.00, NULL, 'Payment for auction 3: 2018 GMC Sierra', 'INV003', 'Auction Payment', NULL, 'Bank Transfer', NULL, NULL, NULL, '2024-09-15 05:05:12', 200003),
(700013, 4, 10500.00, 10500.00, NULL, 'Payment for auction 4: 2015 Volkswagen Jetta', 'INV004', 'Auction Payment', '', 'Credit Card', 2000.00, NULL, NULL, '2024-09-22 07:45:33', 200004),
(700014, 5, 26000.00, 26000.00, NULL, 'Payment for auction 5: 2020 Mazda CX-5', 'INV005', 'Auction Payment', NULL, 'Cash', NULL, NULL, NULL, '2024-10-26 19:31:36', 200005),
(700015, 6, 19000.00, 34000.00, 15000.00, 'Payment for auction 6: 2018 BMW X3', 'INV006', 'Auction Payment', '', 'Bank Transfer', 500.00, NULL, NULL, '2024-09-05 04:10:55', 200006),
(700016, 7, 30000.00, 30000.00, NULL, 'Payment for auction 7: 2019 Ford Explorer', 'INV007', 'Auction Payment', NULL, 'Credit Card', NULL, NULL, NULL, '2024-09-10 13:55:40', 200007);

-- --------------------------------------------------------

--
-- Table structure for table `BILL_DETAILS`
--

CREATE TABLE `BILL_DETAILS` (
  `Bill_details_id` int(6) NOT NULL,
  `Bill_id` int(6) NOT NULL,
  `Car_id` int(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `BILL_DETAILS`
--

INSERT INTO `BILL_DETAILS` (`Bill_details_id`, `Bill_id`, `Car_id`) VALUES
(1, 700010, 1),
(2, 700011, 2),
(3, 700012, 3),
(4, 700013, 4),
(5, 700014, 5),
(6, 700015, 6),
(7, 700016, 7);

-- --------------------------------------------------------

--
-- Table structure for table `CAR`
--

CREATE TABLE `CAR` (
  `Car_id` int(6) NOT NULL,
  `External_car` enum('Yes','No') NOT NULL,
  `Year` varchar(250) NOT NULL,
  `Lotnumber` varchar(250) NOT NULL,
  `Vin` varchar(250) NOT NULL,
  `Auction_id` int(6) NOT NULL,
  `Auction_location_id` int(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `CAR`
--

INSERT INTO `CAR` (`Car_id`, `External_car`, `Year`, `Lotnumber`, `Vin`, `Auction_id`, `Auction_location_id`) VALUES
(1, 'Yes', '2016	', '12345678', '1HGCM82633A123456', 1, 1),
(2, 'No', '2019', '23456789', '2FTRX18L1XCA12345', 2, 2),
(3, 'Yes', '2018', '34567890', '5TBBT441X5S123456', 3, 3),
(4, 'No', '2015', '45678901', '1GNEK13ZX3R123456', 4, 4),
(5, 'Yes', '2020', '56789012', '4T1BF1FK0FU123456', 5, 5),
(6, 'No', '2018', '67890123', 'WBA8E9G54GNT12345', 6, 6),
(7, 'Yes', '2019', '78901234', '1FMJU1JT5JEA12345', 7, 7);

-- --------------------------------------------------------

--
-- Table structure for table `COMPLAINT_MESSAGE`
--

CREATE TABLE `COMPLAINT_MESSAGE` (
  `Complaint_message_id` int(6) NOT NULL,
  `Title` varchar(255) NOT NULL,
  `Message` text NOT NULL,
  `Lot_vin` varchar(255) DEFAULT NULL,
  `Complaint_source` smallint(6) DEFAULT NULL,
  `Customer_id` int(6) NOT NULL,
  `Name` varchar(100) NOT NULL,
  `Email` varchar(100) NOT NULL,
  `Phone` varchar(100) NOT NULL,
  `Source_department_id` int(6) DEFAULT NULL,
  `Department` int(6) DEFAULT NULL,
  `Create_by` int(6) DEFAULT NULL,
  `Create_date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Redirect_date` timestamp NULL DEFAULT '0000-00-00 00:00:00',
  `Answer_date` timestamp NULL DEFAULT '0000-00-00 00:00:00',
  `Answer_by` int(6) DEFAULT NULL,
  `Redirect_by` int(6) DEFAULT NULL,
  `Parent_id` int(6) DEFAULT NULL,
  `Feedback` int(6) DEFAULT NULL,
  `Status` smallint(6) DEFAULT NULL,
  `Priority` smallint(6) DEFAULT NULL,
  `Show_to_Customer` smallint(6) DEFAULT NULL,
  `Token_no` varchar(50) NOT NULL,
  `Lang` varchar(5) NOT NULL,
  `Token_issued_date` datetime NOT NULL,
  `Complaint_type` int(6) NOT NULL,
  `Complaint_file` varchar(255) DEFAULT NULL,
  `Deleted` int(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `COMPLAINT_MESSAGE_CHAT`
--

CREATE TABLE `COMPLAINT_MESSAGE_CHAT` (
  `Complaint_chat_id` int(6) NOT NULL,
  `Complaint_message_id` int(6) NOT NULL,
  `Message` text NOT NULL,
  `Attachment` varchar(255) DEFAULT NULL,
  `Voice_message` varchar(255) DEFAULT NULL,
  `Source` tinyint(1) DEFAULT NULL,
  `Created_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `Seen_at` timestamp NULL DEFAULT '0000-00-00 00:00:00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `CUSTOMER`
--

CREATE TABLE `CUSTOMER` (
  `Customer_id` int(6) NOT NULL,
  `Account_id` int(6) NOT NULL,
  `Membership_id` varchar(255) NOT NULL,
  `Full_name` varchar(255) NOT NULL,
  `Full_name_ar` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `CUSTOMER`
--

INSERT INTO `CUSTOMER` (`Customer_id`, `Account_id`, `Membership_id`, `Full_name`, `Full_name_ar`) VALUES
(1, 100001, '1XA3CEQL', 'Ethan Parker', ''),
(2, 100002, 'A1MFT765', 'Ava Mitchell', ''),
(3, 100003, 'I8JC9OVM', 'Liam Turner', ''),
(4, 100004, 'KH6VTCAS', 'Sophia Collins', ''),
(5, 100005, '3OK18LJ6', 'Mason Rivera', ''),
(6, 100006, 'Y69L0NJO', 'Isabella Bennett', ''),
(7, 100007, '4OWR4K6W', 'Oliver Brooks', '');

-- --------------------------------------------------------

--
-- Table structure for table `SELLER`
--

CREATE TABLE `SELLER` (
  `Seller_id` int(6) NOT NULL,
  `Seller_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `SELLER`
--

INSERT INTO `SELLER` (`Seller_id`, `Seller_name`) VALUES
(200001, 'Mia Campbell'),
(200002, 'James Foster'),
(200003, 'Charlotte Gray'),
(200004, 'Benjamin Hayes'),
(200005, 'Amelia Hughes'),
(200006, 'Lucas Edwards'),
(200007, 'Ella Russell');

-- --------------------------------------------------------

--
-- Table structure for table `TOWING_LIST`
--

CREATE TABLE `TOWING_LIST` (
  `Towing_list_id` int(6) NOT NULL,
  `Title` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `TOWING_LIST`
--

INSERT INTO `TOWING_LIST` (`Towing_list_id`, `Title`) VALUES
(1, 'Towed'),
(2, 'Not Towed'),
(3, 'Scheduled for Towing'),
(4, 'In Transit'),
(5, 'Towing Completed'),
(6, 'Ready for Pickup');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ACCOUNT`
--
ALTER TABLE `ACCOUNT`
  ADD PRIMARY KEY (`Account_id`);

--
-- Indexes for table `ARRIVED_CAR`
--
ALTER TABLE `ARRIVED_CAR`
  ADD PRIMARY KEY (`Arrived_car_id`),
  ADD KEY `Arrived_car_Car_id_FK1` (`Car_id`);

--
-- Indexes for table `AUCTION`
--
ALTER TABLE `AUCTION`
  ADD PRIMARY KEY (`Auction_id`) USING BTREE,
  ADD KEY `Auction_FK1` (`Account_id`),
  ADD KEY `Auction_FK2` (`Create_by`);

--
-- Indexes for table `AUCTION_LOCATION`
--
ALTER TABLE `AUCTION_LOCATION`
  ADD PRIMARY KEY (`Auction_location_id`),
  ADD KEY `AL_Auction_id_FK1` (`Auction_id`);

--
-- Indexes for table `BILL`
--
ALTER TABLE `BILL`
  ADD PRIMARY KEY (`Bill_id`),
  ADD KEY `Bill_Customer_id_FK1` (`Customer_id`),
  ADD KEY `Bill_Create_by_FK2` (`Create_by`);

--
-- Indexes for table `BILL_DETAILS`
--
ALTER TABLE `BILL_DETAILS`
  ADD PRIMARY KEY (`Bill_details_id`),
  ADD KEY `Bill_id_FK1` (`Bill_id`),
  ADD KEY `Car_id_FK2` (`Car_id`);

--
-- Indexes for table `CAR`
--
ALTER TABLE `CAR`
  ADD PRIMARY KEY (`Car_id`),
  ADD KEY `Car_Auction_id_FK1` (`Auction_id`),
  ADD KEY `Car_Auction_loc_id_FK2` (`Auction_location_id`);

--
-- Indexes for table `COMPLAINT_MESSAGE`
--
ALTER TABLE `COMPLAINT_MESSAGE`
  ADD PRIMARY KEY (`Complaint_message_id`),
  ADD KEY `Complaint_Customer_id_FK1` (`Customer_id`);

--
-- Indexes for table `COMPLAINT_MESSAGE_CHAT`
--
ALTER TABLE `COMPLAINT_MESSAGE_CHAT`
  ADD PRIMARY KEY (`Complaint_chat_id`),
  ADD KEY `Chat_Complaint_id_FK1` (`Complaint_message_id`);

--
-- Indexes for table `CUSTOMER`
--
ALTER TABLE `CUSTOMER`
  ADD PRIMARY KEY (`Customer_id`),
  ADD KEY `Customer_Account_id_FK1` (`Account_id`);

--
-- Indexes for table `SELLER`
--
ALTER TABLE `SELLER`
  ADD PRIMARY KEY (`Seller_id`);

--
-- Indexes for table `TOWING_LIST`
--
ALTER TABLE `TOWING_LIST`
  ADD PRIMARY KEY (`Towing_list_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `ARRIVED_CAR`
--
ALTER TABLE `ARRIVED_CAR`
  ADD CONSTRAINT `Arrived_car_Car_id_FK1` FOREIGN KEY (`Car_id`) REFERENCES `CAR` (`Car_id`);

--
-- Constraints for table `AUCTION`
--
ALTER TABLE `AUCTION`
  ADD CONSTRAINT `Auction_FK1` FOREIGN KEY (`Account_id`) REFERENCES `ACCOUNT` (`Account_ID`),
  ADD CONSTRAINT `Auction_FK2` FOREIGN KEY (`Create_by`) REFERENCES `SELLER` (`Seller_id`);

--
-- Constraints for table `AUCTION_LOCATION`
--
ALTER TABLE `AUCTION_LOCATION`
  ADD CONSTRAINT `AL_Auction_id_FK1` FOREIGN KEY (`Auction_id`) REFERENCES `AUCTION` (`Auction_id`);

--
-- Constraints for table `BILL`
--
ALTER TABLE `BILL`
  ADD CONSTRAINT `Bill_Create_by_FK2` FOREIGN KEY (`Create_by`) REFERENCES `SELLER` (`Seller_id`),
  ADD CONSTRAINT `Bill_Customer_id_FK1` FOREIGN KEY (`Customer_id`) REFERENCES `CUSTOMER` (`Customer_id`);

--
-- Constraints for table `BILL_DETAILS`
--
ALTER TABLE `BILL_DETAILS`
  ADD CONSTRAINT `Bill_id_FK1` FOREIGN KEY (`Bill_id`) REFERENCES `BILL` (`Bill_id`),
  ADD CONSTRAINT `Car_id_FK2` FOREIGN KEY (`Car_id`) REFERENCES `CAR` (`Car_id`);

--
-- Constraints for table `CAR`
--
ALTER TABLE `CAR`
  ADD CONSTRAINT `Car_Auction_id_FK1` FOREIGN KEY (`Auction_id`) REFERENCES `AUCTION` (`Auction_id`),
  ADD CONSTRAINT `Car_Auction_loc_id_FK2` FOREIGN KEY (`Auction_location_id`) REFERENCES `AUCTION_LOCATION` (`Auction_location_id`);

--
-- Constraints for table `COMPLAINT_MESSAGE`
--
ALTER TABLE `COMPLAINT_MESSAGE`
  ADD CONSTRAINT `Complaint_Customer_id_FK1` FOREIGN KEY (`Customer_id`) REFERENCES `CUSTOMER` (`Customer_id`);

--
-- Constraints for table `COMPLAINT_MESSAGE_CHAT`
--
ALTER TABLE `COMPLAINT_MESSAGE_CHAT`
  ADD CONSTRAINT `Chat_Complaint_id_FK1` FOREIGN KEY (`Complaint_message_id`) REFERENCES `COMPLAINT_MESSAGE` (`Complaint_message_id`);

--
-- Constraints for table `CUSTOMER`
--
ALTER TABLE `CUSTOMER`
  ADD CONSTRAINT `Customer_Account_id_FK1` FOREIGN KEY (`Account_id`) REFERENCES `ACCOUNT` (`Account_ID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
