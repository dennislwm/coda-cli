.PHONY: default install_freeze install_new install_pipfile run shell shell_clean

default: run

install_freeze:
  pip3 install pipreqs
	pipreqs --ignore tests . --force
	echo "click==8.1.3" >> ./requirements.txt
	echo "codaio==0.6.10" >> ./requirements.txt
	pip3 uninstall -y pipreqs

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