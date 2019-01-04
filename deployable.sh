#!/bin/sh
export HOST_PORT="8000"
if [ $1 ]
then
    HOST_PORT=$1
fi
export CONT_NM="nyuscheduler"
export HOME_DIR="/home/Scheduler"

docker rm $CONT_NM 2> /dev/null || true 
docker run -it -p $HOST_PORT:8000 $CONT_NM $HOME_DIR/runserver.sh
