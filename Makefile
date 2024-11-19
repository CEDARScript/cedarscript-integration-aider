.PHONY: all dist d clean c version v install i test t build b

ci: clean install test
all: ci build version

dist d: all
	scripts/check-version.sh
	twine upload dist/*

clean c:
	rm -rfv out dist build/bdist.*

version v:
	git describe --tags ||:
	python -m setuptools_scm

install i:
	pip install --upgrade --force-reinstall -e . \
	&& pip show cedarscript-integration-aider

test t:
	echo TODO pytest --cov=src/cedarscript_integration_aider tests/ --cov-report term-missing

build b:
	# SETUPTOOLS_SCM_PRETEND_VERSION=0.0.1
	python -m build
