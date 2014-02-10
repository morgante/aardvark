aardvark
========

Clarifies acronyms

# Docker
This project is containerized with [Docker](http://docker.io). With docker installed, from the project directory:

# Rebuild the docker image with every requirement change: ```docker build -t morgante/aardvark .```
# Run the docker image, with a mount for development: ```docker run -P -v /var/code/COREI-24J/aardvark/:/src -d -t morgante/aardvark``` where ```/var/code/COREI-24J/aardvark/``` is the porject directory on the host machine.
# For production, the mounting is unnecessary: ```docker run -P -d -t morgante/aardvark```