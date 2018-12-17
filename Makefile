
all: process.venv

process.venv:
	virtualenv -p python3 process.venv && \
	. process.venv/bin/activate && \
	./process.venv/bin/pip install -r requirements.txt

clean:
	rm -rf process.venv *.pyc

test: process.venv
	. process.venv/bin/activate && \
	./func_test.py
