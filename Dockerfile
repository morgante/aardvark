# DOCKER-VERSION 0.8.0
FROM		shykes/pybuilder

# LXML nonsense
RUN 		apt-get install -y libxml2-dev libxslt1-dev python-dev
RUN 		easy_install lxml

# Add requirements
ADD 		./requirements.txt /requirements.txt

# Install requirements
RUN 		pip install -r /requirements.txt

# Add source
ADD 		. /src

# Expose port
EXPOSE 		5000

# Run it
WORKDIR		/src

ENTRYPOINT ["python"]
CMD ["server.py"]