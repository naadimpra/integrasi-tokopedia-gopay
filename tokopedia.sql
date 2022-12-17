-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 17, 2022 at 04:18 AM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tokopedia`
--

-- --------------------------------------------------------

--
-- Table structure for table `item`
--

CREATE TABLE `item` (
  `id_item` int(3) NOT NULL,
  `nama_item` varchar(255) NOT NULL,
  `harga_item` int(15) NOT NULL,
  `rating_item` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `item`
--

INSERT INTO `item` (`id_item`, `nama_item`, `harga_item`, `rating_item`) VALUES
(1, 'Jet Washer', 84000, 4.5),
(2, 'Hair Dryer Olike', 46900, 4),
(3, 'Redoxon Vitamin C', 50000, 4.2),
(4, 'Selotip Bening', 3000, 4.8),
(5, 'Adidas Duramo', 900000, 5),
(6, 'Charger Robot 10W', 45000, 4.7),
(7, 'Haylou RS4 Plus', 649000, 3.5),
(8, 'Rexus Daiva RX68SF', 520000, 4.4),
(9, 'Hifiman Susvara', 85000000, 4.6),
(10, 'Apple iPhone 14 Pro', 22999000, 4.7),
(11, 'Google Pixel 7 Pro', 12900000, 5),
(12, 'Stik PS4 Dualshock 4', 250000, 2.5),
(13, 'Razer Viper Mini', 299999, 4.8),
(14, 'Kacamata Hitam', 25000, 1),
(15, 'Mi Band 7', 450000, 3.7),
(16, 'Powerbank 10000mAh', 149000, 3.9),
(17, 'Kabel USB Type-C', 20500, 2.2),
(18, 'Kabel HDMI', 70000, 3.6),
(19, 'Sarung Tangan', 9900, 1.5),
(20, 'Masker KF94 (10Pcs)', 9500, 4.3),
(21, 'Sandisk USB 32GB', 49000, 4.2),
(22, 'Apple AirPods Pro', 3299000, 4.9),
(23, 'Case HP Xiaomi 13', 49500, 5),
(24, 'Tas Gadget', 89000, 4.3),
(25, 'Keyboard Cover', 69900, 3.8);

-- --------------------------------------------------------

--
-- Table structure for table `penjual`
--

CREATE TABLE `penjual` (
  `id_penjual` int(3) NOT NULL,
  `nama_penjual` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `penjual`
--

INSERT INTO `penjual` (`id_penjual`, `nama_penjual`) VALUES
(1, 'Toto Official Store'),
(2, 'OLike Official Store'),
(3, 'Redoxon Official Store'),
(4, 'deli Official Store'),
(5, 'Adidas Official Store'),
(6, 'Robot Official Store '),
(7, 'Haylou Store'),
(8, 'Rexus Official Store'),
(9, 'Hifiman Store'),
(10, 'Digimap Official'),
(11, 'Made by Google'),
(12, 'matahari_game'),
(13, 'Razer Official Store'),
(14, 'acc_store'),
(15, 'Xiaomi Official Store'),
(16, 'Acmic Official Store'),
(17, 'Vivan Official Store'),
(18, 'sakinah'),
(19, 'biomedstore'),
(20, 'Mouson Official Store'),
(21, 'SanDisk Official Store'),
(22, 'iBox Official'),
(23, 'XUNDD'),
(24, 'ACOME'),
(25, 'GDYNMCS');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `telepon` varchar(15) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `gopay_status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`telepon`, `nama`, `gopay_status`) VALUES
('505', 'Ariel', 0),
('899', 'Salman', 1),
('667', 'Kevin', 0),
('777', 'Nadim', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `item`
--
ALTER TABLE `item`
  ADD PRIMARY KEY (`id_item`);

--
-- Indexes for table `penjual`
--
ALTER TABLE `penjual`
  ADD PRIMARY KEY (`id_penjual`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `item`
--
ALTER TABLE `item`
  MODIFY `id_item` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `penjual`
--
ALTER TABLE `penjual`
  MODIFY `id_penjual` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
