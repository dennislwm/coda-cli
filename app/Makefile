.PHONY: default ci_build ci_freeze ci_test_build ci_test_freeze docker_build docker_clean docker_run install_freeze install_new run shell shell_clean test test_verbose help list-docs list-controls list-folders list-formulas list-sections list-tables list-views list-columns list-rows get-doc get-section get-column export-table export-template import-template register-template list-templates remove-template

default: run

ci_build: ci_freeze
	DOCKER_BUILDKIT=1 docker build -t coda-cli .

ci_freeze:
	pip3 install pipreqs
	pipreqs --ignore tests . --force
	pip3 uninstall -y pipreqs

ci_test_build: ci_test_freeze
	DOCKER_BUILDKIT=1 docker build -t coda-cli .

ci_test_freeze:
	pip3 install pipreqs
	pipreqs --ignore tests . --force
	echo "prospector==1.6.0" >> ./requirements.txt
	echo "pytest==6.2.4" >> ./requirements.txt
	pip3 uninstall -y pipreqs

docker_build: install_freeze
	DOCKER_BUILDKIT=1 docker build -t coda-cli .

docker_clean:
	docker image prune -f

docker_run: docker_build docker_clean
	docker run --rm --env-file .env --name=objCoda coda-cli --version

install_freeze:
	pipreqs --ignore tests . --force

install_new:
	pipenv install click==8.1.3 codaio==0.6.10
	pipenv install --dev pytest==6.2.4

run:
	python coda.py

shell:
	pipenv shell

shell_clean:
	pipenv --rm

test:
	PYTHONPATH=. pytest

test_verbose:
	PYTHONPATH=. pytest -v -s

# CLI command targets (require valid CODA_API_KEY and parameters)
help:
	pipenv run python coda.py --help

list-docs:
	pipenv run python coda.py list-docs | jq

list-controls:
	@echo "Usage: make list-controls DOC=<doc_id>"
	@if [ -n "$(DOC)" ]; then pipenv run python coda.py list-controls --doc $(DOC) | jq; fi

list-folders:
	@echo "Usage: make list-folders DOC=<doc_id>"
	@if [ -n "$(DOC)" ]; then pipenv run python coda.py list-folders --doc $(DOC) | jq; fi

list-formulas:
	@echo "Usage: make list-formulas DOC=<doc_id>"
	@if [ -n "$(DOC)" ]; then pipenv run python coda.py list-formulas --doc $(DOC) | jq; fi

list-sections:
	@echo "Usage: make list-sections DOC=<doc_id>"
	@if [ -n "$(DOC)" ]; then pipenv run python coda.py list-sections --doc $(DOC) | jq; fi

list-tables:
	@echo "Usage: make list-tables DOC=<doc_id>"
	@if [ -n "$(DOC)" ]; then pipenv run python coda.py list-tables --doc $(DOC) | jq; fi

list-views:
	@echo "Usage: make list-views DOC=<doc_id>"
	@if [ -n "$(DOC)" ]; then pipenv run python coda.py list-views --doc $(DOC) | jq; fi

list-columns:
	@echo "Usage: make list-columns DOC=<doc_id> TABLE=<table_id>"
	@if [ -n "$(DOC)" ] && [ -n "$(TABLE)" ]; then pipenv run python coda.py list-columns --doc $(DOC) --table $(TABLE) | jq; fi

list-rows:
	@echo "Usage: make list-rows DOC=<doc_id> TABLE=<table_id>"
	@if [ -n "$(DOC)" ] && [ -n "$(TABLE)" ]; then pipenv run python coda.py list-rows --doc $(DOC) --table $(TABLE) | jq; fi

get-doc:
	@echo "Usage: make get-doc DOC=<doc_id>"
	@if [ -n "$(DOC)" ]; then pipenv run python coda.py get-doc --doc $(DOC) | jq; fi

get-section:
	@echo "Usage: make get-section DOC=<doc_id> SECTION=<section_id>"
	@if [ -n "$(DOC)" ] && [ -n "$(SECTION)" ]; then pipenv run python coda.py get-section --doc $(DOC) --section $(SECTION) | jq; fi

get-column:
	@echo "Usage: make get-column DOC=<doc_id> TABLE=<table_id> COLUMN=<column_id>"
	@if [ -n "$(DOC)" ] && [ -n "$(TABLE)" ] && [ -n "$(COLUMN)" ]; then pipenv run python coda.py get-column --doc $(DOC) --table $(TABLE) --column $(COLUMN) | jq; fi

export-table:
	@echo "Usage: make export-table DOC=<doc_id> TABLE=<table_id> [OUTPUT=<file.csv>]"
	@if [ -n "$(DOC)" ] && [ -n "$(TABLE)" ]; then \
		if [ -n "$(OUTPUT)" ]; then \
			pipenv run python coda.py export-table --doc $(DOC) --table $(TABLE) --output $(OUTPUT); \
		else \
			pipenv run python coda.py export-table --doc $(DOC) --table $(TABLE); \
		fi \
	fi

export-template:
	@echo "Usage: make export-template DOC=<doc_id> [OUTPUT=<file.yml>]"
	@if [ -n "$(DOC)" ]; then \
		if [ -n "$(OUTPUT)" ]; then \
			pipenv run python coda.py export-template --doc $(DOC) --output $(OUTPUT); \
		else \
			pipenv run python coda.py export-template --doc $(DOC); \
		fi \
	fi

import-template:
	@echo "Usage: make import-template FILE=<template.yml> [VARIABLES='VAR1=value1 VAR2=value2']"
	@if [ -n "$(FILE)" ]; then \
		if [ -n "$(VARIABLES)" ]; then \
			pipenv run python coda.py import-template --file $(FILE) --variables "$(VARIABLES)"; \
		else \
			pipenv run python coda.py import-template --file $(FILE); \
		fi \
	fi

register-template:
	@echo "Usage: make register-template NAME=<template_name> DOC=<doc_id> [DESCRIPTION='<description>']"
	@if [ -n "$(NAME)" ] && [ -n "$(DOC)" ]; then \
		if [ -n "$(DESCRIPTION)" ]; then \
			pipenv run python coda.py register-template --name $(NAME) --doc $(DOC) --description "$(DESCRIPTION)"; \
		else \
			pipenv run python coda.py register-template --name $(NAME) --doc $(DOC); \
		fi \
	fi

list-templates:
	@echo "Usage: make list-templates"
	pipenv run python coda.py list-templates

remove-template:
	@echo "Usage: make remove-template NAME=<template_name>"
	@if [ -n "$(NAME)" ]; then \
		pipenv run python coda.py remove-template --name $(NAME); \
	fi