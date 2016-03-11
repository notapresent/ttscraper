PYTHON          = $(shell which python2)
DEV_APPSERVER	= $(shell which dev_appserver.py)
PORT      		?= 8080
ADMIN_PORT      = 8081
SERVE_ADDRESS   = 0.0.0.0
DATASTORE_PATH  = $(realpath ../datastore.sqlite3)
ifeq ($(findstring /bin/dev_appserver.py,$(DEV_APPSERVER)),/bin/dev_appserver.py)
APPENGINE = $(realpath $(dir $(DEV_APPSERVER))..)/platform/google_appengine
else
APPENGINE = $(patsubst %/,%,$(dir $(DEV_APPSERVER)))
endif

init:
	pip install -r requirements.txt
	rm -rf ttupdater/lib/*
	pip install -r requirements-prod.txt -t ttupdater/lib

test:
	cd ttupdater && $(PYTHON) testrunner.py $(APPENGINE) .
