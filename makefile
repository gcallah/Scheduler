# Need to export as ENV var
export TEMPLATE_DIR = templates
export QUIZ_DIR = templates

PTML_DIR = html_src
UDIR = utils
INCS = $(TEMPLATE_DIR)/head.txt 
SCHED_DIR = scheduler/scheduler

HTML_FILES = $(shell ls $(PTML_DIR)/*.ptml | sed -e 's/.ptml/.html/' | sed -e 's/html_src\///')

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

# the rest of these targets must be tweaked for this project:
container:
	docker build -t scheduler docker


dblocal:
	python3 manage.py makemigrations
	python3 manage.py migrate

db:
	python3 manage.py makemigrations
	python3 manage.py migrate
	git add $(SCHED_DIR)/migrations/*.py
	-git commit $(SCHED_DIR)/migrations/*.py
	git push origin master

prod: $(SRCS) $(OBJ)
	./all_tests.sh
	git push origin master
# what to do here?
#	ssh gcallah@ssh.pythonanywhere.com 'cd /home/gcallah/Emu86; /home/gcallah/Emu86/myutils/prod.sh'
