#
# Makefile

defaut: help

install: wandbox/*.py ## install self
	python setup.py install

install-test-deps: ## install test dependencies
	pip install -e.[test]

test: install ## commands test
	make -C samples/command

pytest: ## python test
	python setup.py test

tox: install-test-deps ## run tox
	tox .

flake8: install-test-deps ## run tox flake8 only
	tox -e flake8 .

help: ## Display this help screen
	@grep -E '^[a-zA-Z][a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sed -e 's/^GNUmakefile://' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

docker-build: ## build development docker image
	docker build -t wandbox-api-dev .

docker-run: ## run development docker container
	docker run -it --rm -v ${PWD}:/work -w /work wandbox-api-dev bash
	
docker-alpine: ## run python alpine container
	docker run -it --rm -v ${PWD}:/work -w /work python:3.8-alpine sh
	# apk add make

pyenv-versions:
	pyenv versions | grep -v system | grep -o "3\.5\.[0-9a-z]*" | tail -1 >  .python-version
	pyenv versions | grep -v system | grep -o "3\.6\.[0-9a-z]*" | tail -1 >> .python-version
	pyenv versions | grep -v system | grep -o "3\.7\.[0-9a-z]*" | tail -1 >> .python-version
	pyenv versions | grep -v system | grep -o "3\.8\.[0-9a-z]*" | tail -1 >> .python-version
	pyenv versions | grep -v system | grep -o "3\.9\.[0-9a-z]*" | tail -1 >> .python-version

clean: ## clean workspace
	rm -rf .python-version
