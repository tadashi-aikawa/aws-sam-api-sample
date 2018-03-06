create database rds;
use rds;

CREATE TABLE `members` (
  `id` varchar(4) NOT NULL,
  `name` varchar(30) NOT NULL,
  `age` integer NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE `projects` (
  `id` varchar(4) NOT NULL,
  `name` varchar(30) NOT NULL,
  `launch_at` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO members VALUES
  ('0001', 'イチロー', 40),
  ('0002', 'ジロー', 30),
  ('0003', 'サブロー', 20)

