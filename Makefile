PYTHON          = python
APPENGINE       = /home/ubuntu/google-cloud-sdk/platform/google_appengine
APPCFG          = $(PYTHON) /home/ubuntu/google-cloud-sdk/platform/google_appengine/appcfg.py
APP_ID          = ttupdater
EMAIL           = notapresent@gmail.com
PORT      		?= 8080
ADMIN_PORT      = 8081
SERVE_ADDRESS   = 0.0.0.0
DATASTORE_PATH  = ../datastore.sqlite3

test:
	cd ttupdater && $(PYTHON) testrunner.py $(APPENGINE) .

deploy:
	$(APPCFG) -e $(EMAIL) update .

update:
	$(APPCFG) -e $(EMAIL) update .

rollback:
	$(APPCFG) -e $(EMAIL) rollback .

serve:
	$(PYTHON) $(APPENGINE)/dev_appserver.py \
	--host $(SERVE_ADDRESS) --port $(PORT) \
	--admin_host $(SERVE_ADDRESS) --admin_port $(ADMIN_PORT) \
	--datastore_path=$(DATASTORE_PATH) \
	.

console:
	@$(PYTHON) $(APPENGINE)/remote_api_shell.py -s $(APP_ID).appspot.com

update-indexes:
	$(APPCFG) update_indexes .

vacuum-indexes:
	$(APPCFG) vacuum_indexes .

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
