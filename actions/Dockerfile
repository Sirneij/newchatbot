
FROM rasa/rasa-sdk:2.8.1

COPY . /app/actions/
COPY ./startup.sh /startup.sh

EXPOSE 5005
ENV PORT 5005

STOPSIGNAL SIGINT

USER root
RUN chmod a+rx /startup.sh
ENTRYPOINT "/startup.sh"