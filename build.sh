#!/usr/bin/env bash
#git reset --hard 21501dbf8a0655865ac85d6adec5fd7175f1149d
#git pull

# run tests
pytest tests -v
if [[ $? != 0 ]]
    then
        echo "Test isn't completed!!!"
        exit
fi

docker stop nrs
docker rm nrs
docker rmi nrs

docker build -t nrs .

docker run --rm --name nrs \
    -p 8080:8080 \
    -e TELEGRAM_ACCES_TOKEN=431094155:AAGou_c16lpH96_dgQ8xq1gP2ZQSJEAZPuo \
    -e TELEGRAM_CHAT_ID=410942470\
    -e NOTIFICATION_ENGINE=true \
    nrs
