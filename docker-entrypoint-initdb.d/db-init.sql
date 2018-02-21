create database rds;
use rds;

CREATE TABLE `humans` (
  `id` varchar(8) NOT NULL,
  `name` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

INSERT INTO humans VALUES ('00000001', 'ichiro'), ('00000002', 'jiro');
