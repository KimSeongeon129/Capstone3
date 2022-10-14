-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';


CREATE DATABASE IF not exists myDB;


CREATE TABLE IF NOT EXISTS `user` (
  `user_id` VARCHAR(100) NOT NULL,
  `nickname` VARCHAR(100) NOT NULL,
  `user_admin` VARCHAR(100) ,
  `user_line` VARCHAR(100) ,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;


CREATE TABLE IF NOT EXISTS `admin` (
  `admin_id` VARCHAR(100) NOT NULL,
  `admin_pw` VARCHAR(100) NOT NULL,
  `number` VARCHAR(100) NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`admin_id`))
ENGINE = InnoDB;



CREATE TABLE IF NOT EXISTS `image` (
  `inspection_number` VARCHAR(50) NOT NULL,
  `img_id` VARCHAR(45) NOT NULL,
  `bbox_x1` DOUBLE NOT NULL,
  `bbox_x2` DOUBLE NOT NULL,
  `bbox_y1` DOUBLE NOT NULL,
  `bbox_y2` DOUBLE NOT NULL,
  `image` MEDIUMBLOB NOT NULL,
  PRIMARY KEY (`inspection_number`))
ENGINE = InnoDB;



CREATE TABLE IF NOT EXISTS `result` (
  `part_id` VARCHAR(45) NOT NULL,
  `date` DATETIME(6) NOT NULL,
  `part_name` VARCHAR(45) NOT NULL,
  `part_category` VARCHAR(45) NOT NULL,
  `part_judge` VARCHAR(45) NOT NULL,
  `user_id` VARCHAR(100) NOT NULL,
  `inspection_number` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`inspection_number`),
  FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE cascade ON UPDATE cascade,
  FOREIGN KEY (`inspection_number`) REFERENCES `image` (`inspection_number`) ON DELETE cascade ON UPDATE cascade)
ENGINE = InnoDB;

select * from admin;


select * from user;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

