-- MySQL Script generated by MySQL Workbench
-- Thứ ba, 18 Tháng 6 Năm 2019 15:27:31 +07
-- Model: New Model    Version: 1.0
-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema kindness_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema kindness_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `kindness_db` DEFAULT CHARACTER SET utf8 ;
USE `kindness_db` ;

-- -----------------------------------------------------
-- Table `kindness_db`.`category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kindness_db`.`category` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `icon` VARCHAR(245) NULL,
  `description` VARCHAR(4500) NULL,
  `ordinal` INT NOT NULL DEFAULT 0,
  `parent_id` INT NULL,
  `status` INT NULL,
  `used_for_search` INT NULL,
  `used_for_filter` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kindness_db`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kindness_db`.`user` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `full_name` VARCHAR(64) NOT NULL,
  `email` VARCHAR(64) NULL,
  `phone` VARCHAR(32) NULL,
  `gender` INT NULL,
  `avatar` VARCHAR(245) NULL,
  `created_time` BIGINT NULL,
  `updated_time` BIGINT NULL,
  `push_token` VARCHAR(4500) NULL,
  `device_id` VARCHAR(64) NULL,
  `facebook_id` VARCHAR(64) NULL,
  `google_id` VARCHAR(64) NULL,
  `apple_id` VARCHAR(64) NULL,
  `birthday` DATE NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4;


-- -----------------------------------------------------
-- Table `kindness_db`.`following`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kindness_db`.`following` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT NOT NULL,
  `following_user_id` BIGINT NOT NULL,
  `inserted_time` BIGINT NULL,
  `status` INT NULL,
  `updated_time` BIGINT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idx_unique_following` (`user_id` ASC, `following_user_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kindness_db`.`user_story`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kindness_db`.`user_story` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT NOT NULL,
  `title` VARCHAR(450) NOT NULL,
  `content` LONGTEXT NOT NULL,
  `status` INT NULL,
  `created_time` BIGINT NULL,
  `number_of_like` INT NOT NULL DEFAULT 0,
  `numer_of_dislike` INT NOT NULL DEFAULT 0,
  `number_of_comment` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kindness_db`.`image`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kindness_db`.`image` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NULL,
  `description` VARCHAR(4500) NULL,
  `image_link` VARCHAR(255) NOT NULL,
  `status` INT NOT NULL DEFAULT 0,
  `created_time` BIGINT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kindness_db`.`story_image`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kindness_db`.`story_image` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `story_id` BIGINT NULL,
  `image_id` BIGINT NULL,
  `inserted_time` BIGINT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idx_unique_image` (`story_id` ASC, `image_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kindness_db`.`kindness_action`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kindness_db`.`kindness_action` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(1000) NULL,
  `content` LONGTEXT NULL,
  `status` INT NULL,
  `created_time` BIGINT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kindness_db`.`kindness_action_image`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kindness_db`.`kindness_action_image` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `kindness_action_id` BIGINT NOT NULL,
  `image_id` BIGINT NOT NULL,
  `created_time` BIGINT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idx_unique_image` (`kindness_action_id` ASC, `image_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kindness_db`.`story_action`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kindness_db`.`story_action` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `story_id` BIGINT NOT NULL,
  `action_id` BIGINT NOT NULL,
  `created_time` BIGINT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idx_unique_story_action` (`story_id` ASC, `action_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kindness_db`.`action_category`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kindness_db`.`action_category` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `action_id` BIGINT NOT NULL,
  `category_id` INT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unique_action_category` (`action_id` ASC, `category_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kindness_db`.`story_reaction`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kindness_db`.`story_reaction` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `story_id` BIGINT NOT NULL,
  `user_id` BIGINT NOT NULL,
  `reaction_id` VARCHAR(45) NOT NULL,
  `reaction_time` BIGINT NULL,
  `status` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idx_unique_user_story` (`story_id` ASC, `user_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kindness_db`.`story_comment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kindness_db`.`story_comment` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `story_id` BIGINT NOT NULL,
  `user_id` BIGINT NOT NULL,
  `content` LONGTEXT NULL,
  `commented_time` BIGINT NULL,
  `status` INT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kindness_db`.`comment_image`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kindness_db`.`comment_image` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `comment_id` BIGINT NOT NULL,
  `image_id` BIGINT NOT NULL,
  `created_time` BIGINT NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `idx_unique_comment_image` (`comment_id` ASC, `image_id` ASC))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `kindness_db`.`suggest_kindness_action`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `kindness_db`.`suggest_kindness_action` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `user_id` BIGINT NOT NULL,
  `action_id` BIGINT NOT NULL,
  `inserted_time` BIGINT NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
