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
S3_IP := 192.168.100.101
PACKAGE_NAME := aws_sam_sample
EVENT :=
FUNCTION :=

#----------------------------
# Develop and Test
#----------------------------
init: ## Initialize for develop
	@echo Start $@
	pipenv install -d
	@echo End $@

test: ## Test
	@echo Start $@
	pipenv run pytest tests $(ARGS)
	@echo End $@


#----------------------------
# Run locally
#----------------------------
init-aws-local: ## Initialize AWS local environments
	@echo Start $@
	docker network create --subnet=192.168.100.0/24 $(NETWORK_NAME)
	docker run \
	    --name rds-mysql \
	    -p 3306:3306 \
	    --net $(NETWORK_NAME) \
	    --ip $(RDS_IP) \
	    -v `pwd`/docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d \
	    -v `pwd`/conf.d:/etc/mysql/conf.d \
	    -e MYSQL_ROOT_PASSWORD=password \
	    -d mysql:5.6
	docker run \
	    --name s3server \
	    --net $(NETWORK_NAME) \
	    --ip $(S3_IP) \
	    -p 8000:8000 \
	    -e SCALITY_ACCESS_KEY_ID=accessKey1 \
	    -e SCALITY_SECRET_ACCESS_KEY=verySecretKey1 \
	    -e S3BACKEND=mem \
	    -d scality/s3server
	@echo 'Wait 10 minutes for initialize DB & S3'
	@sleep 10s
	pipenv run python s3-local-init.py
	@echo End $@

build: ## Build
	mkdir -p dist/$(PACKAGE_NAME)
	rsync -av --delete $(PACKAGE_NAME)/ dist/$(PACKAGE_NAME)/

install-packages: ## Install packages to dist according to Pipfile
	@echo Start $@
	rm -rf dist
	make build
	rm -f requirements.txt

	mkdir -p dist
	pipenv lock -r | cut -d' ' -f1 > requirements.txt
	pip install -r requirements.txt -t dist/
	rm -f requirements.txt
	@echo End $@

run-as-lambda: build ## Run lambda locally (ex. make dev EVENT=find_ichiro.json FUNCTION=MemberFunction)
	@echo Start $@
	sam local invoke \
		-e events/$(EVENT) \
		--env-vars envs/dev.json \
		--docker-network $(NETWORK_NAME) \
		$(FUNCTION)
	@echo End $@

run-as-api: build ## Run as API
	@echo Start $@
	sam local start-api \
		--env-vars envs/dev.json \
		--docker-network $(NETWORK_NAME)
	@echo End $@

clean-aws-local: ## Clean AWS local environments
	@echo Start $@
	-docker rm -f `docker ps -aq --filter name=rds-mysql`
	-docker rm -f `docker ps -aq --filter name=s3server`
	-docker network remove $(NETWORK_NAME)
	@echo End $@

db-client: ## Access DB by using client
	@echo Start $@
	docker run -it \
	    --link rds-mysql:mysql \
	    --net $(NETWORK_NAME) \
	    -e LANG=C.UTF-8 \
	    --rm \
	    mysql sh -c 'exec mysql -h"$(RDS_IP)" -P3306 -uroot -ppassword'
	@echo End $@


#----------------------------
# Deploy to staging or...
#----------------------------
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

