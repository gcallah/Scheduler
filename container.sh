#!/bin/sh
docker rm scheduler 2> /dev/null || true 
docker run -it -p 8000:8000 -v $PWD:/home/Scheduler scheduler bash
