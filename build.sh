#!/usr/bin/env bash
mkdir "queue-bot"
mv bot Procfile requirements.txt "queue-bot"
cd queue-bot
heroku create queue-bot
git init && echo "git inited"
heroku git:remote -a queue-bot
git add . && git commit -am "init" && git push heroku master && echo "run.."
heroku ps:scale bot=1
#heroku logs -t