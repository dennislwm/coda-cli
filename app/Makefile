.PHONY: default ci_build ci_freeze docker_build docker_clean docker_run install_freeze install_new install_pipfile install_test run shell shell_clean test test_verbose

default: run

ci_build: ci_freeze
	DOCKER_BUILDKIT=1 docker build -t coda-cli .

ci_freeze:
  pip3 install pipreqs
	pipreqs --ignore tests . --force
	echo "prospector==1.6.0" >> ./requirements.txt
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
	pipenv install --dev pytest=6.2.4

install_pipfile:
	pipenv install --dev

run:
  python coda.py

shell:
	pipenv shell

shell_clean:
	pipenv --rm

test: 
	PYTHONPATH=.:../ pytest

test_verbose: 
	PYTHONPATH=.:../ pytest -v -s