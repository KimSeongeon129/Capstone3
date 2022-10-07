-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------


-- -----------------------------------------------------
-- Table `mydb`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `user` (
  `user_id` VARCHAR(20) NOT NULL,
  `user_pw` VARCHAR(20) NOT NULL,
  `name` VARCHAR(20) NOT NULL,
  `number` VARCHAR(50) NOT NULL,
  `user_admin` VARCHAR(20) NOT NULL,
  `user_line` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`user_id`))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `mydb`.`admin`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `admin` (
  `admin_id` VARCHAR(20) NOT NULL,
  `admin_pw` VARCHAR(20) NOT NULL,
  `number` VARCHAR(50) NOT NULL,
  `name` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`admin_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `mydb`.`image`
-- -----------------------------------------------------
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


-- -----------------------------------------------------
-- Table `mydb`.`result`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `result` (
  `part_id` VARCHAR(45) NOT NULL,
  `date` DATETIME(6) NOT NULL,
  `part_name` VARCHAR(45) NOT NULL,
  `part_category` VARCHAR(45) NOT NULL,
  `part_judge` VARCHAR(45) NOT NULL,
  `user_id` VARCHAR(20) NOT NULL,
  `inspection_number` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`inspection_number`),
  INDEX `fk_result_user1_idx` (`user_id` ASC) VISIBLE,
  INDEX `fk_result_image1_idx` (`inspection_number` ASC) VISIBLE,
  CONSTRAINT `fk_result_user1`
    FOREIGN KEY (`user_id`)
    REFERENCES `user` (`user_id`)
    ON DELETE cascade
    ON UPDATE cascade,
  CONSTRAINT `fk_result_image1`
    FOREIGN KEY (`inspection_number`)
    REFERENCES `image` (`inspection_number`)
    ON DELETE cascade
    ON UPDATE cascade)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
