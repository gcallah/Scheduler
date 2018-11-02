# Need to export as ENV var
export TEMPLATE_DIR = templates
export QUIZ_DIR = templates
export TEST_DIR = tests
export TEST_DATA = test_data

PTML_DIR = html_src
UDIR = utils
INCS = $(TEMPLATE_DIR)/head.txt 
DJANGO_DIR = scheduler
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

# build the static website describing the project:
website: $(INCS) $(HTML_FILES) 
	-git commit -a 
	git pull origin master
	git push origin master

# the rest of these targets may need to be tweaked for this project:
container:
	docker build -t scheduler docker


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
