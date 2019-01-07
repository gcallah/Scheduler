# Need to export as ENV var
export TEMPLATE_DIR = templates
export QUIZ_DIR = templates
export TEST_DIR = tests
export TEST_DATA = test_data

PTML_DIR = html_src
UDIR = utils
INCS = $(TEMPLATE_DIR)/head.txt 
DJANGO_DIR = scheduler
DOCKER_DIR = docker
PYTHONFILES = $(shell ls $(DJANGO_DIR)/*.py)

HTML_FILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\///')

FORCE:

tests: FORCE
	$(TEST_DIR)/all_tests.sh

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

deploy_container:
	docker system prune
	docker build -t gcallah/nyusched --no-cache -f $(DOCKER_DIR)/Deployable $(DOCKER_DIR)

ship_container:
	docker push gcallah/nyusched

dblocal:
	python3 manage.py makemigrations
	python3 manage.py migrate

db:
	python3 manage.py makemigrations
	python3 manage.py migrate
	git add $(DJANGO_DIR)/migrations/*.py
	-git commit $(DJANGO_DIR)/migrations/*.py
	git push origin master

prod: $(SRCS) $(OBJ)
	$(TEST_DIR)/all_tests.sh
	-git commit -a 
	git push origin master
# what to do here?
#	ssh gcallah@ssh.pythonanywhere.com 'cd /home/gcallah/Emu86; /home/gcallah/Emu86/myutils/prod.sh'
