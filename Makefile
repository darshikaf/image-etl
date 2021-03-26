DOCKER_IMAGE := build-python:latest
TERM := docker run --rm -it -v $(shell pwd):/etl -w /etl -e PYTTHONPATH=. darshika/${DOCKER_IMAGE}
TESTENV	:= docker run --rm -v $(shell pwd):/etl -w /etl -e PYTTHONPATH=. darshika/${DOCKER_IMAGE}

clean:
	$(TESTENV) rm -rf __pycache__ etl/__pycache__ tests/__pycache__ .pytest_cache .coverage
	$(TESTENV) rm -rf __pycache__ etl/grid/__pycache__ etl/agent/__pycache__ etl/commands/__pycache__
	$(TESTENV) rm -rf .mypy_cache/
	$(TESTENV) rm -rf .eggs *.egg-info dist/*

test: clean
	$(TESTENV) coverage run setup.py test --pytest-args="--junit-xml=tests/results.xml"
	$(TESTENV) coverage report

test-specific: clean
	$(TESTENV) python setup.py test --pytest-args="-k $(TEST)|-s|-v"

test-verbose: clean
	$(TESTENV) python setup.py test --pytest-args="-s"

test-missing: clean
	$(TESTENV) python setup.py test --pytest-args="--cov-report=term-missing|--cov=etl"

bash:
	$(TERM) bash

python:
	$(TERM) python

local-dist:
	python setup.py sdist bdist_wheel
	pip install dist/image_etl-*.whl

release:
	$(TERM) python setup.py sdist bdist_wheel; twine upload --repository testpypi dist/*

test-python-lint:
	$(TESTENV) black -l 79 --check .

test-python-types:
	$(TESTENV) mypy --ignore-missing-imports etl

.PHONY: test bash clean python