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

init-db: ## Initialize DB
	@echo Start $@
	docker run \
	    --name rds-mysql \
	    -p 3306:3306 \
	    -v `pwd`/docker-entrypoint-initdb.d:/docker-entrypoint-initdb.d \
	    -e MYSQL_ROOT_PASSWORD=password \
	    -d mysql:5.6 \
	    --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci 
	@echo End $@

clean-db: ## Delete DB
	@echo Start $@
	docker rm -f `docker ps -aq --filter name=rds-mysql`
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

build: ## Build application
	@echo Start $@
	mkdir -p dist
	cp app.py dist/
	@echo End $@

build-with-install: _install build ## Install packages and build application

dev: ## Run locally
	@echo Start $@
	sam local invoke -e event.json TestFunction
	@echo End $@

