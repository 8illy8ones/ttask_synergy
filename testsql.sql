DROP DATABASE IF EXISTS test_db;
CREATE DATABASE test_db; 
USE test_db;


CREATE TABLE users (
user_id INT  AUTO_INCREMENT NOT NULL PRIMARY KEY,
email VARCHAR(50) NOT NULL,
name VARCHAR(50) NOT NULL,
phone VARCHAR(30),
cell VARCHAR(30) ,
status boolean
);

CREATE TABLE courses (
course_id INT  AUTO_INCREMENT NOT NULL PRIMARY KEY,
name varchar(50) NOT NULL,
code varchar(50) NOT NULL
);

CREATE TABLE users_courses (
id INT  AUTO_INCREMENT NOT NULL PRIMARY KEY,
user_id int NOT NULL,
course_id int NOT NULL,
FOREIGN KEY (course_id) REFERENCES courses(course_id)
);


DROP PROCEDURE IF EXISTS get_all_users;
DELIMITER //
CREATE PROCEDURE get_all_users()
BEGIN
     SELECT * FROM users;
END//
DELIMITER ;

DROP PROCEDURE IF EXISTS create_user;
DELIMITER //
CREATE PROCEDURE create_user
(
    IN
	p_email VARCHAR(30),
	p_name VARCHAR(30),
	p_phone VARCHAR(30),
	p_cell VARCHAR(30),
	p_status boolean
)
BEGIN
    INSERT INTO users VALUES (user_id, p_email, p_name, p_phone, p_cell, p_status) ;
END //
DELIMITER ;



DROP PROCEDURE IF EXISTS update_user;
DELIMITER //
CREATE PROCEDURE update_user
(
    IN
	uid int,
	p_phone VARCHAR(30),
	p_cell VARCHAR(30),
	p_status boolean
)
BEGIN
    UPDATE users SET phone = p_phone, cell = p_cell, status = p_status WHERE user_id = uid ;
END //
DELIMITER ;



DROP PROCEDURE IF EXISTS get_user;
DELIMITER //
CREATE PROCEDURE get_user  (IN uid int)
BEGIN
    SELECT * from users where user_id = uid;
END //
DELIMITER ;


DROP PROCEDURE IF EXISTS delete_user;
DELIMITER //
CREATE PROCEDURE delete_user (IN uid INT)
BEGIN
    DELETE FROM users WHERE user_id = uid;
END //
DELIMITER ;



DROP PROCEDURE IF EXISTS get_users_courses;
DELIMITER //
CREATE PROCEDURE get_users_courses(IN uid INT)
BEGIN
    SELECT * from users_courses as U join courses ;
END //
DELIMITER ;

DROP PROCEDURE IF EXISTS get_all_courses;
DELIMITER //
CREATE PROCEDURE get_all_courses()
BEGIN
    SELECT * from courses;
END //
DELIMITER ;