DROP TABLE IF EXISTS rule;
DROP TABLE IF EXISTS endpoint;
DROP TABLE IF EXISTS alert_history;
DROP TABLE IF EXISTS alert;

CREATE TABLE endpoint (
id INT NOT NULL AUTO_INCREMENT,
uid VARCHAR(32) NOT NULL,
CONSTRAINT pk_endpoint PRIMARY KEY (id),
CONSTRAINT u_uid UNIQUE (uid)
);

CREATE TABLE alert (
id INT NOT NULL AUTO_INCREMENT,
endpoint_id INT NOT NULL, 
insert_date DATETIME NOT NULL,
effective_date DATETIME NOT NULL,
category VARCHAR(254) NOT NULL, 
impact INT,
priority INT, 
severity INT, 
status INT, 
name VARCHAR(254),
body TEXT,
CONSTRAINT pk_alert PRIMARY KEY (id),
CONSTRAINT FOREIGN KEY (endpoint_id) REFERENCES endpoint (id)
);

CREATE TABLE alert_history(
id INT NOT NULL AUTO_INCREMENT,
alert_id INT, 
effective_date DATETIME, 
summary VARCHAR(1000),
CONSTRAINT pk_alert_history PRIMARY KEY (id),
CONSTRAINT fk_alert_id FOREIGN KEY (alert_id) REFERENCES alert (id)
);

CREATE TABLE rule (
id INT NOT NULL AUTO_INCREMENT,
type VARCHAR(32), 
endpoint_id INT,
logic VARCHAR(1000),
CONSTRAINT pk_rule PRIMARY KEY (id),
CONSTRAINT FOREIGN KEY (endpoint_id) REFERENCES endpoint (id)
);


