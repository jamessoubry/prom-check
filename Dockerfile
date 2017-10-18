FROM python:3.6

RUN pip3 install requests

# This is something I like to do as it adds the Dockerfile to the image for easy reverse engineering
ADD . /

#RUN chmod 755 /prom-check.py

ENTRYPOINT [ "python", "-u", "prom-check.py" ]