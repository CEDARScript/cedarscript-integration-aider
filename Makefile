.PHONY: all version v test t dist d clean c

all: test version

version v:
	git describe --tags
	python -m setuptools_scm

test t:
	echo TODO pytest --cov=src/cedarscript_integration_aider tests/ --cov-report term-missing

dist d: test
	scripts/check-version.sh
	rm -rf dist/
	python -m build && twine upload dist/*

clean c:
	rm -rfv dist/
