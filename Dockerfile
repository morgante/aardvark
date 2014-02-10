# DOCKER-VERSION 0.8.0
FROM	shykes/pybuilder

# Add source
ADD 	. /src

# Pip installer
RUN 	cd /src; pip install -r requirements.txt

# Expose port
EXPOSE 	5000

# Run it
WORKDIR	/src

CMD		["python", "server.py"]