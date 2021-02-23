#
# Makefile

defaut: help

install: wandbox/*.py ## install self
	python setup.py install

test: install ## commands test
	make -C samples/command

pytest: ## python test
	python setup.py test	

help: ## Display this help screen
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

docker:
	docker run -it --rm -v ${PWD}:/work -w /work python:3.8-alpine sh
	# apk add make
