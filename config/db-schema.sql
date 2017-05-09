CREATE DATABASE IF NOT EXISTS django CHARACTER SET utf8 COLLATE utf8_bin;
CREATE DATABASE IF NOT EXISTS fluidintegrates;

USE fluidintegrates;

CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT,
    username varchar(255) DEFAULT NULL,
    registered char(1) DEFAULT 'N',
    last_name varchar(255) DEFAULT NULL,
    first_name varchar(255) DEFAULT NULL,
    email varchar(255) NOT NULL,
    company varchar(255) NOT NULL,
    PRIMARY KEY (id)
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS roles (
    user_id INT NOT NULL,
    role varchar(255) NOT NULL
) ENGINE=INNODB;

CREATE TABLE IF NOT EXISTS projects (
    user_id INT NOT NULL,
    project varchar(255) NOT NULL
) ENGINE=INNODB;
