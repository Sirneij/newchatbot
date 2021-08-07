FROM ubuntu:18.04

RUN apt-get update && apt-get install -y python3 python3-pip
RUN python3 -m pip install --upgrade pip
RUN pip3 install rasa==2.8

ADD * /actions/

RUN chmod +x /actions/*

ENTRYPOINT []
CMD ./actions/start_actions.sh