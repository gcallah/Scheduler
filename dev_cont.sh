#!/bin/sh
export HOST_PORT="8000"
export CONT_NAME="scheduler"
if [ $1 ]
then
    HOST_PORT=$1
fi

docker rm $CONT_NAME 2> /dev/null || true 
docker run -it -p $HOST_PORT:8000 -v $PWD:/home/Scheduler $CONT_NAME bash
