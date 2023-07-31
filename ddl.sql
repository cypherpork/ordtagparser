
SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for addr
-- ----------------------------
DROP TABLE IF EXISTS `addr`;
CREATE TABLE `addr` (
  `id` int(16) unsigned NOT NULL AUTO_INCREMENT,
  `fkid` int(16) NOT NULL,
  `addridx` int(12) NOT NULL,
  `pkaddr` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for inscr
-- ----------------------------
DROP TABLE IF EXISTS `inscr`;
CREATE TABLE `inscr` (
  `id` int(16) unsigned NOT NULL AUTO_INCREMENT,
  `ord_id` int(16) NOT NULL,
  `inscr_id` varchar(255) NOT NULL,
  `gen_trx` varchar(255) DEFAULT NULL,
  `output_no` int(4) DEFAULT NULL,
  `adj_output_no` int(4) DEFAULT NULL,
  `chain` varchar(255) NOT NULL DEFAULT 'mainnet',
  `status` varchar(24) NOT NULL DEFAULT 'NEW',
  `num_tags` int(4) NOT NULL DEFAULT 0,
  `trxid` int(11) DEFAULT NULL,
  `parstatus` varchar(24) NOT NULL DEFAULT 'NEW',
  `parmessage` varchar(255) DEFAULT NULL,
  `shadowing` int(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inscr_uk` (`ord_id`,`chain`) USING BTREE,
  KEY `num_tags_idx` (`num_tags`) USING BTREE,
  KEY `ord_id_idx` (`ord_id`) USING BTREE,
  KEY `inscr_id_idx` (`inscr_id`) USING BTREE,
  KEY `status_idx` (`status`),
  KEY `parstatus_idx` (`parstatus`),
  KEY `driver_idx` (`chain`,`status`,`parstatus`) USING BTREE,
  KEY `trxid_idx` (`trxid`),
  KEY `gentrx_idx` (`gen_trx`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for inscr28
-- ----------------------------
DROP TABLE IF EXISTS `inscr28`;
CREATE TABLE `inscr28` (
  `id` int(16) unsigned NOT NULL AUTO_INCREMENT,
  `ord_id` int(16) NOT NULL,
  `inscr_id` varchar(255) NOT NULL,
  `inscr_loc` varchar(255) NOT NULL,
  `gen_trx` varchar(255) DEFAULT NULL,
  `output_no` int(4) DEFAULT NULL,
  `adj_output_no` int(4) DEFAULT NULL,
  `chain` varchar(255) NOT NULL DEFAULT 'mainnet',
  `status` varchar(24) NOT NULL DEFAULT 'NEW',
  `num_tags` int(4) NOT NULL DEFAULT 0,
  `trxid` int(11) DEFAULT NULL,
  `parstatus` varchar(24) NOT NULL DEFAULT 'NEW',
  `parmessage` varchar(255) DEFAULT NULL,
  `shadowing` int(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inscr28_uk` (`ord_id`,`chain`) USING BTREE,
  KEY `num_tags28_idx` (`num_tags`) USING BTREE,
  KEY `ord_id28_idx` (`ord_id`) USING BTREE,
  KEY `inscr28_id_idx` (`inscr_id`) USING BTREE,
  KEY `status28_idx` (`status`),
  KEY `parstatus28_idx` (`parstatus`),
  KEY `driver28_idx` (`chain`,`status`,`parstatus`) USING BTREE,
  KEY `trxid_idx` (`trxid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for ord_tags
-- ----------------------------
DROP TABLE IF EXISTS `ord_tags`;
CREATE TABLE `ord_tags` (
  `id` int(16) unsigned NOT NULL AUTO_INCREMENT,
  `inscr_tb_id` int(16) unsigned NOT NULL,
  `ord_id` int(16) NOT NULL,
  `tag_no` varchar(2) NOT NULL,
  `tag_value` varchar(2000) DEFAULT NULL,
  `tag_guess` varchar(2000) DEFAULT NULL,
  `note` varchar(1000) DEFAULT NULL,
  `chain` varchar(255) NOT NULL,
  `notation_id` int(11) DEFAULT NULL,
  `format_notation_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE,
  KEY `tag_no_idx` (`tag_no`) USING HASH,
  KEY `ord_id_idx` (`ord_id`) USING BTREE,
  KEY `tag_to_inscr_fk` (`inscr_tb_id`),
  CONSTRAINT `tag_to_inscr_fk` FOREIGN KEY (`inscr_tb_id`) REFERENCES `inscr` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ROW_FORMAT=DYNAMIC;

-- ----------------------------
-- Table structure for shadows
-- ----------------------------
DROP TABLE IF EXISTS `shadows`;
CREATE TABLE `shadows` (
  `id` int(16) unsigned NOT NULL DEFAULT 0,
  `ord_id` int(16) NOT NULL,
  `real_ord_id` int(16) DEFAULT NULL,
  `inscr_id` varchar(255) NOT NULL,
  `gen_trx` varchar(255) DEFAULT NULL,
  `output_no` int(4) DEFAULT NULL,
  `adj_output_no` int(4) DEFAULT NULL,
  `chain` varchar(255) NOT NULL DEFAULT 'mainnet',
  `status` varchar(24) NOT NULL DEFAULT 'NEW',
  `num_tags` int(4) NOT NULL DEFAULT 0,
  `trxid` int(11) DEFAULT NULL,
  `parstatus` varchar(24) NOT NULL DEFAULT 'NEW',
  `parmessage` varchar(255) DEFAULT NULL,
  `shadowing` int(16) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `shadow_light_idx` (`gen_trx`,`adj_output_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for tx
-- ----------------------------
DROP TABLE IF EXISTS `tx`;
CREATE TABLE `tx` (
  `id` int(16) unsigned NOT NULL AUTO_INCREMENT,
  `txid` char(64) NOT NULL,
  `hash` char(64) NOT NULL,
  `version` int(1) NOT NULL,
  `txsize` int(16) NOT NULL,
  `txvsize` int(16) NOT NULL,
  `weight` int(16) NOT NULL,
  `locktime` int(16) NOT NULL,
  `vincount` int(16) unsigned NOT NULL DEFAULT 0,
  `voutcount` int(16) unsigned NOT NULL DEFAULT 0,
  `blockhash` char(64) NOT NULL,
  `unixtime` int(12) NOT NULL,
  `txtimedate` datetime NOT NULL,
  `chainnet` varchar(24) NOT NULL DEFAULT 'mainnet',
  PRIMARY KEY (`id`),
  UNIQUE KEY `txid_uk` (`txid`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for vin
-- ----------------------------
DROP TABLE IF EXISTS `vin`;
CREATE TABLE `vin` (
  `id` int(16) unsigned NOT NULL AUTO_INCREMENT,
  `belongsto_fkid` int(16) NOT NULL,
  `idxvin` int(16) NOT NULL,
  `intxid` char(64) NOT NULL,
  `invoutn` int(16) NOT NULL,
  `vinseq` int(16) unsigned NOT NULL,
  `witsize` int(16) NOT NULL DEFAULT 0,
  `content_status` varchar(16) DEFAULT NULL,
  `scriptsigasm` varchar(255) DEFAULT NULL,
  `scriptsighex` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vin_uk` (`intxid`,`invoutn`) USING BTREE,
  KEY `vin_to_tx_fk` (`belongsto_fkid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for vout
-- ----------------------------
DROP TABLE IF EXISTS `vout`;
CREATE TABLE `vout` (
  `id` int(16) unsigned NOT NULL AUTO_INCREMENT,
  `belongsto_fkid` int(16) NOT NULL,
  `valu` decimal(17,9) unsigned NOT NULL DEFAULT 0.000000000,
  `n` int(16) unsigned NOT NULL,
  `pkasm` varchar(2000) DEFAULT NULL,
  `pkdesc` varchar(255) DEFAULT NULL,
  `pkhex` varchar(255) DEFAULT NULL,
  `reqsigs` int(16) DEFAULT 1,
  `pktype` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `vout_uk` (`n`,`belongsto_fkid`) USING BTREE,
  KEY `vout_to_tx_fk` (`belongsto_fkid`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Table structure for wit
-- ----------------------------
DROP TABLE IF EXISTS `wit`;
CREATE TABLE `wit` (
  `id` int(16) unsigned NOT NULL AUTO_INCREMENT,
  `fkid_vin_tab` int(16) unsigned NOT NULL,
  `belongsto_fkid_txid` int(16) unsigned NOT NULL,
  `idxvin` int(16) NOT NULL,
  `idxwit` int(16) NOT NULL,
  `hashwit` varchar(64) DEFAULT NULL,
  `withex` mediumtext NOT NULL,
  `witbin` blob DEFAULT NULL,
  `content_format` varchar(1000) DEFAULT NULL,
  `unwrapped_content` mediumtext DEFAULT NULL,
  `unhexlified_cont` mediumtext DEFAULT NULL,
  `rstatus` varchar(255) NOT NULL DEFAULT 'NEW',
  `recordclass` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `wit_uk` (`idxwit`,`fkid_vin_tab`) USING BTREE,
  UNIQUE KEY `wit_content_uk` (`hashwit`,`fkid_vin_tab`,`idxwit`) USING BTREE,
  KEY `txwit_to_tx_fk` (`fkid_vin_tab`),
  KEY `content_idx` (`unwrapped_content`(768))
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- View structure for non_01_tags
-- ----------------------------
DROP VIEW IF EXISTS `non_01_tags`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `non_01_tags` AS select `si`.`id` AS `id`,`si`.`chain` AS `chain`,`si`.`ord_id` AS `ord_id`,`si`.`inscr_id` AS `inscr_id`,`si`.`txid` AS `txid`,`si`.`index_no` AS `index_no`,`si`.`adj_index_no` AS `adj_index_no`,`si`.`num_tags` AS `num_tags`,`si`.`tag_no` AS `tag_no`,`si`.`tag_value` AS `tag_value`,`si`.`tag_guess` AS `tag_guess`,`si`.`note` AS `note`,`si`.`inscr_format` AS `inscr_format`,`tx`.`vincount` AS `total_inputs`,`tx`.`txtimedate` AS `created_on`,`tx`.`id` AS `transaction_table_pk`,`si`.`notation_id` AS `notation_id` from ((select `inscr`.`id` AS `id`,`inscr`.`chain` AS `chain`,`inscr`.`ord_id` AS `ord_id`,`inscr`.`inscr_id` AS `inscr_id`,`inscr`.`gen_trx` AS `txid`,`inscr`.`output_no` AS `index_no`,`inscr`.`adj_output_no` AS `adj_index_no`,`inscr`.`num_tags` AS `num_tags`,`o1`.`tag_no` AS `tag_no`,`o1`.`tag_value` AS `tag_value`,`o1`.`tag_guess` AS `tag_guess`,`o1`.`note` AS `note`,`o2`.`tag_guess` AS `inscr_format`,`o1`.`notation_id` AS `notation_id` from ((`inscr` join `ord_tags` `o1`) join `ord_tags` `o2`) where `inscr`.`id` = `o1`.`inscr_tb_id` and `o2`.`tag_no` = '01' and `inscr`.`id` = `o2`.`inscr_tb_id` and `o1`.`tag_no` <> '01') `si` left join `tx` on(`si`.`txid` = `tx`.`txid`)) order by `tx`.`txtimedate`,`si`.`ord_id`;

-- ----------------------------
-- View structure for non_01_tags_summary
-- ----------------------------
DROP VIEW IF EXISTS `non_01_tags_summary`;
CREATE ALGORITHM = UNDEFINED SQL SECURITY DEFINER VIEW `non_01_tags_summary` AS select `v1`.`tag_no` AS `Tag Number`,`v1`.`notation_id` AS `Style id`,count(`v1`.`notation_id`) AS `Count`,date_format(min(`v1`.`created_on`),'%b %d %h:%i') AS `First Seen`,date_format(max(`v1`.`created_on`),'%b %d %h:%i') AS `Last Seen`,floor(count(`v1`.`ord_id`) - sum(sign(`v1`.`ord_id`) + 1) / 2) AS `Cursed`,floor(sum(sign(`v1`.`ord_id`) + 1) / 2) AS `Not Cursed` from `non_01_tags` `v1` group by 2 order by 1,3;

SET FOREIGN_KEY_CHECKS = 1;
