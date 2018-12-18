
all: bump-version-yaml.venv

bump-version-yaml.venv:
	virtualenv -p python3 bump-version-yaml.venv && \
	. bump-version-yaml.venv/bin/activate && \
	./bump-version-yaml.venv/bin/pip install -r requirements.txt

clean:
	rm -rf bump-version-yaml.venv *.pyc

test: bump-version-yaml.venv
	. bump-version-yaml.venv/bin/activate && \
	./func_test.py
