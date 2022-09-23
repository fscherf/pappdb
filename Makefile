SHELL=/bin/bash
PYTHON=python3

PYTHON_ENV_ROOT=envs
PYTHON_DEVELOPMENT_ENV=$(PYTHON_ENV_ROOT)/$(PYTHON)-dev
PYTHON_PACKAGING_ENV=$(PYTHON_ENV_ROOT)/$(PYTHON)-packaging
PYTHON_TESTING_ENV=$(PYTHON_ENV_ROOT)/$(PYTHON)-testing

.PHONY: clean doc sdist shell freeze

# environments ################################################################
$(PYTHON_DEVELOPMENT_ENV): REQUIREMENTS.development.txt setup.py
	rm -rf $(PYTHON_DEVELOPMENT_ENV) && \
	$(PYTHON) -m venv $(PYTHON_DEVELOPMENT_ENV) && \
	. $(PYTHON_DEVELOPMENT_ENV)/bin/activate && \
	pip install pip --upgrade && \
	pip install -r ./REQUIREMENTS.development.txt

$(PYTHON_PACKAGING_ENV): REQUIREMENTS.packaging.txt
	rm -rf $(PYTHON_PACKAGING_ENV) && \
	$(PYTHON) -m venv $(PYTHON_PACKAGING_ENV) && \
	. $(PYTHON_PACKAGING_ENV)/bin/activate && \
	pip install --upgrade pip && \
	pip install -r REQUIREMENTS.packaging.txt

$(PYTHON_TESTING_ENV): REQUIREMENTS.testing.txt
	rm -rf $(PYTHON_TESTING_ENV) && \
	$(PYTHON) -m venv $(PYTHON_TESTING_ENV) && \
	. $(PYTHON_TESTING_ENV)/bin/activate && \
	pip install --upgrade pip && \
	pip install -r REQUIREMENTS.testing.txt
	date > $(PYTHON_TESTING_ENV)/.created

# environment helper ##########################################################
clean:
	rm -rf $(PYTHON_ENV_ROOT)
	rm -rf .tox

shell: | $(PYTHON_DEVELOPMENT_ENV)
	. $(PYTHON_DEVELOPMENT_ENV)/bin/activate && \
	$(PYTHON) test.py

freeze: | $(PYTHON_DEVELOPMENT_ENV)
	. $(PYTHON_DEVELOPMENT_ENV)/bin/activate && \
	pip freeze

# packaging ###################################################################
sdist: $(PYTHON_PACKAGING_ENV)
	. $(PYTHON_PACKAGING_ENV)/bin/activate && \
	rm -rf dist *.egg-info && \
	./setup.py sdist

_release: sdist
	. $(PYTHON_PACKAGING_ENV)/bin/activate && \
	twine upload --config-file ~/.pypirc.fscherf dist/*

# tests #######################################################################
test: | $(PYTHON_TESTING_ENV)
	. $(PYTHON_TESTING_ENV)/bin/activate && \
	time tox $(args)

ci-test: | $(PYTHON_TESTING_ENV)
	. $(PYTHON_TESTING_ENV)/bin/activate && \
	time JENKINS_URL=1 tox $(args)

lint: | $(PYTHON_TESTING_ENV)
	. $(PYTHON_TESTING_ENV)/bin/activate && \
	time tox -e lint $(args)
