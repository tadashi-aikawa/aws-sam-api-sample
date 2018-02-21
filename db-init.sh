#!/bin/bash

docker run \
    --name rds-mysql \
    -p 3306:3306 \
    -v `pwd`/docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d \
    -e MYSQL_ROOT_PASSWORD=password \
    -d mysql:5.6 \
    --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci 
    
