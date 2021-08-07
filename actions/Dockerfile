FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3 python3-pip && python3 -m pip install --no-cache --upgrade pip && pip3 install --no-cache rasa==2.8

ADD * /actions/

RUN chmod +x /actions/*

ENTRYPOINT []
CMD ./actions/start_actions.sh