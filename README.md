# Scheduler
Project to schedule lectures in classrooms.

## Run

### Local

Install the development requirements:

```text
pip install -r docker/requirement-dev.txt
``` 

Use shell script to start the server:

```text
./runserver.sh 
``` 

### Docker

Build the docker image:

```text
make dev_container
```

Enter the docker:
```text
./dev_cont.st
```

Use shell script to start the server

```text
./runserver.sh 
```

## Test

```text
make tests
```