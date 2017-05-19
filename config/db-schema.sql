CREATE DATABASE IF NOT EXISTS django CHARACTER SET utf8 COLLATE utf8_bin;
CREATE DATABASE IF NOT EXISTS fluidintegrates CHARACTER SET utf8 COLLATE utf8_bin;

USE fluidintegrates;

CREATE TABLE IF NOT EXISTS users (
    id INT NOT NULL AUTO_INCREMENT,
    username varchar(64) COLLATE utf8_bin DEFAULT NULL,
    password varchar(254) NOT NULL,
    registered tinyint(1) NOT NULL DEFAULT 0,
    last_name varchar(64) COLLATE utf8_bin DEFAULT NULL,
    first_name varchar(64) COLLATE utf8_bin DEFAULT NULL,
    email varchar(254) COLLATE utf8_bin NOT NULL,
    company varchar(254),
    role varchar(32) NOT NULL,
    last_login datetime(6) DEFAULT NULL,
    date_joined datetime(6) DEFAULT NULL,
    PRIMARY KEY (id, email)
) ENGINE=INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE IF NOT EXISTS projects (
    user_id INT NOT NULL,
    project varchar(64) COLLATE utf8_bin NOT NULL
) ENGINE=INNODB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

INSERT INTO users(email,password,role) VALUES("customer@bancolombia.com.co","$6$rounds=656000$qpzYYYHV.VRPyOF7$.xqzwOkgMGHnSNaFI/RxSMk5f4xBOk3GEiAzsc8U5cr9Qj3cs6PjmHITL5GyQHOuOERDynDGmDEXKMpWT.onz.","customer")
