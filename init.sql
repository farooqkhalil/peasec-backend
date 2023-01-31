CREATE DATABASE restapi;
USE restapi;
CREATE TABLE user_creds (user_id INT(11) NOT NULL AUTO_INCREMENT, username VARCHAR(30), password BINARY(60), fullname VARCHAR(30), PRIMARY KEY (user_id));
CREATE TABLE reports (report_id INT(11) NOT NULL AUTO_INCREMENT, title VARCHAR(20), details VARCHAR(255), lat DOUBLE DEFAULT 0, lng DOUBLE DEFAULT 0, country VARCHAR(30), image1 TEXT, image2 TEXT, image3 TEXT, PRIMARY KEY (report_id));
