# Windows Powershell Script for DevOps Docker Container
docker rm scheduler | true
docker run -it -p 8000:8000 -v ${PWD}:/home/Scheduler scheduler bash
