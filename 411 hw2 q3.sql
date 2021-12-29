CREATE TABLE User (
user_id         VARCHAR(20),
name            VARCHAR(20),
email           VARCHAR(20),
PRIMARY KEY (user_id)
);

CREATE TABLE Alubum (
photo_name      VARCHAR(20),
photo_data      VARCHAR(max),
PRIMARY KEY (photo_name,user_id),
FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE
);

CREATE TABLE Article (
aid             VARCHAR(20),
timestamp       VARCHAR(20),
title           VARCHAR(20),
content         VARCHAR(max),
PRIMARY KEY (aid)
);


CREATE TABLE Comment (
cid             VARCHAR(20),
create_time     VARCHAR(20),
text            VARCHAR(max),
PRIMARY KEY (cid)
);