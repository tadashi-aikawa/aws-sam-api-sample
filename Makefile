MAKEFLAGS += --warn-undefined-variables
SHELL := /bin/bash
ARGS :=
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

.PHONY: $(shell egrep -oh ^[a-zA-Z0-9][a-zA-Z0-9_-]+: $(MAKEFILE_LIST) | sed 's/://')

help: ## Print this help
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z0-9][a-zA-Z0-9_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

#------

NETWORK_NAME := br0
RDS_IP := 192.168.100.100
EVENT :=
FUNCTION :=

init: ## Initialize for develop
	@echo Start $@
	pipenv install -d
	@echo End $@

init-db: ## Initialize DB
	@echo Start $@
	docker network create --subnet=192.168.100.0/24 $(NETWORK_NAME)
	docker run \
	    --name rds-mysql \
	    -p 3306:3306 \
	    --net $(NETWORK_NAME) \
	    --ip $(RDS_IP) \
	    -v `pwd`/conf.d:/etc/mysql/conf.d \
	    -v `pwd`/docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d \
	    -e MYSQL_ROOT_PASSWORD=password \
	    -d mysql:5.6 \
	    --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
	@echo End $@

clean-db: ## Delete DB
	@echo Start $@
	-docker rm -f `docker ps -aq --filter name=rds-mysql`
	-docker network remove $(NETWORK_NAME)
	@echo End $@

db: ## Access DB
	@echo Start $@
	docker run -it --link rds-mysql:mysql --net $(NETWORK_NAME) --rm mysql sh -c 'exec mysql -h"$(RDS_IP)" -P3306 -uroot -ppassword'
	@echo End $@

_install:
	@echo Start $@
	rm -rf dist
	rm -f requirements.txt

	mkdir dist
	pipenv lock -r | cut -d' ' -f1 > requirements.txt
	pip install -r requirements.txt -t dist/
	rm -f requirements.txt
	@echo End $@

build:
	@echo Start $@
	mkdir -p dist
	cp -r aws_sam_sample dist/
	@echo End $@

build-with-install: _install build ## Install packages and build application

dev: build ## Run locally (ex. make dev EVENT=find_ichiro.json FUNCTION=MemberFunction)
	@echo Start $@
	sam local invoke \
		-e events/$(EVENT) \
		--env-vars envs/dev.json \
		--docker-network $(NETWORK_NAME) \
		$(FUNCTION)
	@echo End $@

api: build ## Run as API
	@echo Start $@
	sam local start-api \
		--env-vars envs/dev.json \
		--docker-network $(NETWORK_NAME)
	@echo End $@

deploy: ## Deploy
	@echo Start $@
	aws cloudformation package \
	  --template-file template.yaml \
  	--output-template-file output-template.yaml \
  	--s3-bucket mamansoft-aws-sam-sample
	aws cloudformation deploy \
  	--template-file output-template.yaml \
  	--stack-name test \
	  --capabilities CAPABILITY_IAM
	rm output-template.yaml
	@echo End $@

test: ## Test
	@echo Start $@
	pipenv run pytest tests
	@echo End $@

