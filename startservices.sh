cd app/
rasa run -m models --enable-api --cors "*" --debug -p $PORT
rasa run actions -p $PORT
