-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 14, 2025 at 04:28 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `toko_cendrawasih`
--

-- --------------------------------------------------------

--
-- Table structure for table `barang_masuk`
--

CREATE TABLE `barang_masuk` (
  `id` int(11) NOT NULL,
  `kode_barang` varchar(30) NOT NULL,
  `nama_barang` varchar(100) NOT NULL,
  `jumlah` int(11) NOT NULL,
  `harga_beli` decimal(12,2) NOT NULL,
  `tanggal_kadaluarsa` date NOT NULL,
  `tanggal_masuk` date NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `barang_masuk`
--

INSERT INTO `barang_masuk` (`id`, `kode_barang`, `nama_barang`, `jumlah`, `harga_beli`, `tanggal_kadaluarsa`, `tanggal_masuk`, `created_at`) VALUES
(1, 'BRG001', 'Gula Pasir 1kg', 50, 12000.00, '2025-08-15', '2025-01-10', '2025-12-13 14:20:25'),
(2, 'BRG002', 'Minyak Goreng 1L', 30, 18000.00, '2025-07-01', '2025-01-12', '2025-12-13 14:20:25'),
(3, 'BRG003', 'Beras Premium 5kg', 20, 65000.00, '2025-12-31', '2025-01-15', '2025-12-13 14:20:25');

-- --------------------------------------------------------

--
-- Table structure for table `detail_penjualan`
--

CREATE TABLE `detail_penjualan` (
  `id` int(11) NOT NULL,
  `penjualan_id` int(11) NOT NULL,
  `kode_barang` varchar(30) NOT NULL,
  `nama_barang` varchar(100) NOT NULL,
  `qty` int(11) NOT NULL,
  `harga_jual` decimal(12,2) NOT NULL,
  `subtotal` decimal(12,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `detail_penjualan`
--

INSERT INTO `detail_penjualan` (`id`, `penjualan_id`, `kode_barang`, `nama_barang`, `qty`, `harga_jual`, `subtotal`) VALUES
(1, 1, 'BRG001', 'Gula Pasir 1kg', 3, 15000.00, 45000.00),
(2, 1, 'BRG002', 'Minyak Goreng 1L', 2, 25500.00, 51000.00);

-- --------------------------------------------------------

--
-- Table structure for table `fsn_rop`
--

CREATE TABLE `fsn_rop` (
  `id` int(11) NOT NULL,
  `kode_barang` varchar(30) NOT NULL,
  `nama_barang` varchar(100) NOT NULL,
  `kategori_fsn` enum('Fast','Slow','Non-moving') NOT NULL,
  `rata_penjualan_harian` decimal(10,2) NOT NULL,
  `lead_time` int(11) NOT NULL,
  `reorder_point` int(11) NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `fsn_rop`
--

INSERT INTO `fsn_rop` (`id`, `kode_barang`, `nama_barang`, `kategori_fsn`, `rata_penjualan_harian`, `lead_time`, `reorder_point`, `updated_at`) VALUES
(1, 'BRG001', 'Gula Pasir 1kg', 'Non-moving', 0.01, 3, 0, '2025-12-14 04:36:39'),
(2, 'BRG002', 'Minyak Goreng 1L', 'Non-moving', 0.01, 3, 0, '2025-12-14 04:36:39'),
(3, 'BRG003', 'Beras Premium 5kg', 'Non-moving', 0.00, 3, 0, '2025-12-14 04:36:39'),
(4, 'BRG001', 'Gula Pasir 1kg', 'Non-moving', 0.01, 3, 0, '2025-12-14 04:36:41'),
(5, 'BRG002', 'Minyak Goreng 1L', 'Non-moving', 0.01, 3, 0, '2025-12-14 04:36:41'),
(6, 'BRG003', 'Beras Premium 5kg', 'Non-moving', 0.00, 3, 0, '2025-12-14 04:36:41'),
(7, 'BRG001', 'Gula Pasir 1kg', 'Non-moving', 0.01, 3, 0, '2025-12-14 04:36:43'),
(8, 'BRG002', 'Minyak Goreng 1L', 'Non-moving', 0.01, 3, 0, '2025-12-14 04:36:43'),
(9, 'BRG003', 'Beras Premium 5kg', 'Non-moving', 0.00, 3, 0, '2025-12-14 04:36:43'),
(10, 'BRG001', 'Gula Pasir 1kg', 'Non-moving', 0.01, 3, 0, '2025-12-14 14:50:02'),
(11, 'BRG002', 'Minyak Goreng 1L', 'Non-moving', 0.01, 3, 0, '2025-12-14 14:50:02'),
(12, 'BRG003', 'Beras Premium 5kg', 'Non-moving', 0.00, 3, 0, '2025-12-14 14:50:02'),
(13, 'BRG001', 'Gula Pasir 1kg', 'Non-moving', 0.01, 3, 0, '2025-12-14 14:50:05'),
(14, 'BRG002', 'Minyak Goreng 1L', 'Non-moving', 0.01, 3, 0, '2025-12-14 14:50:05'),
(15, 'BRG003', 'Beras Premium 5kg', 'Non-moving', 0.00, 3, 0, '2025-12-14 14:50:05'),
(16, 'BRG001', 'Gula Pasir 1kg', 'Non-moving', 0.01, 3, 0, '2025-12-14 14:51:20'),
(17, 'BRG002', 'Minyak Goreng 1L', 'Non-moving', 0.01, 3, 0, '2025-12-14 14:51:20'),
(18, 'BRG003', 'Beras Premium 5kg', 'Non-moving', 0.00, 3, 0, '2025-12-14 14:51:20'),
(19, 'BRG001', 'Gula Pasir 1kg', 'Non-moving', 0.01, 3, 0, '2025-12-14 14:52:19'),
(20, 'BRG002', 'Minyak Goreng 1L', 'Non-moving', 0.01, 3, 0, '2025-12-14 14:52:19'),
(21, 'BRG003', 'Beras Premium 5kg', 'Non-moving', 0.00, 3, 0, '2025-12-14 14:52:19'),
(22, 'BRG001', 'Gula Pasir 1kg', 'Non-moving', 0.01, 3, 0, '2025-12-14 14:57:16'),
(23, 'BRG002', 'Minyak Goreng 1L', 'Non-moving', 0.01, 3, 0, '2025-12-14 14:57:16'),
(24, 'BRG003', 'Beras Premium 5kg', 'Non-moving', 0.00, 3, 0, '2025-12-14 14:57:16'),
(25, 'BRG001', 'Gula Pasir 1kg', 'Non-moving', 0.01, 3, 10, '2025-12-14 15:22:29'),
(26, 'BRG002', 'Minyak Goreng 1L', 'Non-moving', 0.01, 3, 10, '2025-12-14 15:22:29'),
(27, 'BRG003', 'Beras Premium 5kg', 'Non-moving', 0.00, 3, 10, '2025-12-14 15:22:29');

-- --------------------------------------------------------

--
-- Table structure for table `penjualan`
--

CREATE TABLE `penjualan` (
  `id` int(11) NOT NULL,
  `tanggal_penjualan` date NOT NULL,
  `kasir_id` int(11) NOT NULL,
  `total_transaksi` decimal(12,2) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `penjualan`
--

INSERT INTO `penjualan` (`id`, `tanggal_penjualan`, `kasir_id`, `total_transaksi`, `created_at`) VALUES
(1, '2025-01-20', 2, 96000.00, '2025-12-13 14:20:25');

-- --------------------------------------------------------

--
-- Table structure for table `stok_barang`
--

CREATE TABLE `stok_barang` (
  `id` int(11) NOT NULL,
  `kode_barang` varchar(30) NOT NULL,
  `nama_barang` varchar(100) NOT NULL,
  `total_stok` int(11) NOT NULL DEFAULT 0,
  `tanggal_kadaluarsa` date NOT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stok_barang`
--

INSERT INTO `stok_barang` (`id`, `kode_barang`, `nama_barang`, `total_stok`, `tanggal_kadaluarsa`, `updated_at`) VALUES
(1, 'BRG001', 'Gula Pasir 1kg', 50, '2025-08-15', '2025-12-13 14:20:25'),
(2, 'BRG002', 'Minyak Goreng 1L', 30, '2025-07-01', '2025-12-13 14:20:25'),
(3, 'BRG003', 'Beras Premium 5kg', 20, '2025-12-31', '2025-12-13 14:20:25');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `nama` varchar(150) DEFAULT NULL,
  `username` varchar(80) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('kasir','gudang','kepala_toko','owner') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `nama`, `username`, `password`, `role`) VALUES
(1, 'Maria', 'kasirmaria', 'maria1234', 'kasir'),
(2, 'Johan', 'gudangjohan', 'johan1234', 'gudang'),
(3, 'Wanda', 'ownerwanda', 'wanda1234', 'owner'),
(4, 'Alma', 'kepalaalma', 'alma1234', 'kepala_toko');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `barang_masuk`
--
ALTER TABLE `barang_masuk`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `detail_penjualan`
--
ALTER TABLE `detail_penjualan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `penjualan_id` (`penjualan_id`);

--
-- Indexes for table `fsn_rop`
--
ALTER TABLE `fsn_rop`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `penjualan`
--
ALTER TABLE `penjualan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `kasir_id` (`kasir_id`);

--
-- Indexes for table `stok_barang`
--
ALTER TABLE `stok_barang`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `barang_masuk`
--
ALTER TABLE `barang_masuk`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `detail_penjualan`
--
ALTER TABLE `detail_penjualan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `fsn_rop`
--
ALTER TABLE `fsn_rop`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;

--
-- AUTO_INCREMENT for table `penjualan`
--
ALTER TABLE `penjualan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `stok_barang`
--
ALTER TABLE `stok_barang`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `detail_penjualan`
--
ALTER TABLE `detail_penjualan`
  ADD CONSTRAINT `detail_penjualan_ibfk_1` FOREIGN KEY (`penjualan_id`) REFERENCES `penjualan` (`id`);

--
-- Constraints for table `penjualan`
--
ALTER TABLE `penjualan`
  ADD CONSTRAINT `penjualan_ibfk_1` FOREIGN KEY (`kasir_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
