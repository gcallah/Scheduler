# Need to export as ENV var
export TEMPLATE_DIR = templates
export TEST_DIR = tests
export TEST_DATA = test_data

UDIR = utils
INCS = $(TEMPLATE_DIR)/head.txt 
DJANGO_DIR = scheduler
DOCKER_DIR = docker
PYTHONFILES = $(shell ls $(DJANGO_DIR)/*.py)

FORCE:

tests: FORCE

lint: $(patsubst %.py,%.pylint,$(PYTHONFILES))

%.pylint:
	flake8 $*.py

# rule for making html files from ptml files:
%.html: $(PTML_DIR)/%.ptml $(INCS)
	python3 $(UDIR)/html_checker.py $<
	$(UDIR)/html_include.awk <$< >$@
	git add $@

local: $(HTML_FILES) 

dev_container:
	docker build -t scheduler $(DOCKER_DIR)

prod_container:
	docker build -t gcallah/nyusched --no-cache -f $(DOCKER_DIR)/Deployable $(DOCKER_DIR)

deploy_container:
	docker push gcallah/nyusched

prod: $(SRCS) $(OBJ) local lint tests
	-git commit -a 
	git push origin master
	# now Travis should take over and deploy!
