cd app/
rasa run -m models --endpoints endpoints.yml --credentials credentials.yml  --cors "*" --enable-api  --debug --port $PORT || 5005