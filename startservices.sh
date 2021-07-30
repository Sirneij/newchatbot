cd app/
# Start rasa server with nlu model
rasa run -m models --enable-api --cors "*" --debug -p $PORT
rasa run actions -p $PORT
