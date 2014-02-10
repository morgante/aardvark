aardvark
========

Clarifies acronyms

# Docker
This project is containerized with [Docker](http://docker.io). With docker installed, from the project directory:

1. Rebuild the docker image with every requirement change: ```docker build -t morgante/aardvark .```
2. Run the docker image, with a mount for development: ```docker run -P -v /var/code/COREI-24J/aardvark/:/src -d -t morgante/aardvark``` where ```/var/code/COREI-24J/aardvark/``` is the porject directory on the host machine.
3. The docker container should automatically be exposed on a port in your host machine. To find the port, just type ```docker ps```.

For production, the mounting is unnecessary: ```docker run -P -d -t morgante/aardvark```.
