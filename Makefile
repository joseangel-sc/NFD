test:
	pytest -s -vvv

build_dev:
	docker build -t nfd .

dev_env:
	docker run -it -v $$(pwd):/NFD --entrypoint=/bin/bash nfd

lint:
	autoflake --in-place --remove-unused-variables --remove-all-unused-imports --recursive .
	black .
	isort --atomic --profile black .
