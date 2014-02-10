# DOCKER-VERSION 0.8.0
FROM		shykes/pybuilder

# LXML nonsense
RUN 		apt-get install -y libxml2-dev libxslt1-dev python-dev
RUN 		easy_install lxml

# Add source
ADD 		. /src

# Pip installer
RUN 		cd /src; pip install -r requirements.txt

# Expose port
EXPOSE 		5000

# Run it
WORKDIR		/src

ENTRYPOINT ["python", "server.py"]