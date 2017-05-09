CREATE DATABASE if not exists fluidintegrates;

USE fluidintegrates;

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT,
    username varchar(255) DEFAULT NULL,
    last_name varchar(255) DEFAULT NULL,
    first_name varchar(255) DEFAULT NULL,
    email varchar(255) NOT NULL,
    company varchar(255) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=INNODB;

CREATE TABLE roles (
    user_id INT NOT NULL,
    role varchar(255) NOT NULL,
) ENGINE=INNODB;

CREATE TABLE projects (
    user_id INT NOT NULL,
    project varchar(255) NOT NULL,
) ENGINE=INNODB;

