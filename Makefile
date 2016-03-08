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

deploy:
	$(APPCFG) -e $(EMAIL) update ttupdater

update:
	$(APPCFG) -e $(EMAIL) update ttupdater

rollback:
	$(APPCFG) -e $(EMAIL) rollback ttupdater

serve:
	$(PYTHON) $(APPENGINE)/dev_appserver.py \
	--host $(SERVE_ADDRESS) --port $(PORT) \
	--admin_host $(SERVE_ADDRESS) --admin_port $(ADMIN_PORT) \
	--datastore_path=$(DATASTORE_PATH) \
	ttupdater

console:
	@$(PYTHON) $(APPENGINE)/remote_api_shell.py -s $(APP_ID).appspot.com

update-indexes:
	$(APPCFG) update_indexes ttupdater

vacuum-indexes:
	$(APPCFG) vacuum_indexes ttupdater

download-data:
ifndef filename
	@echo "Invalid usage. Try 'make help' for more details."
else
	$(APPCFG) download_data \
	--application=$(APP_ID) \
	--email=$(EMAIL) \
	--url=http://$(APP_ID).appspot.com/_ah/remote_api \
	--filename=$(filename)
endif
