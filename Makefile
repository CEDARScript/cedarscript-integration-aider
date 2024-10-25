.PHONY: all version test dist clean

all: test version

version:
	python -m setuptools_scm

test:
	echo TODO pytest --cov=src/cedarscript_integration_aider tests/ --cov-report term-missing

dist: test
	scripts/check-version.sh
	rm -rf dist/
	python -m build && twine upload dist/*

clean:
	rm -f /dist/
