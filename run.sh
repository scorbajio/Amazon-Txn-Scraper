!#/usr/bin/bash

docker run --name=firefox-standalone -d -p 4444:4444 -p 7900:7900 --shm-size="2g" selenium/standalone-firefox:4.1.0-20211123
python3 -m venv env
source env/bin/activate
python3 -m pip install -r requirements.txt
python3 main.py
docker stop firefox-standalone
docker container rm firefox-standalone
deactivate