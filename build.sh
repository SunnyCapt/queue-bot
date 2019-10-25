#!/usr/bin/env bash

mkdir queue-bot
mv `ls -a | egrep -v '^(\.|queue-bot|\.\.)$'` queue-bot
cd queue-bot
read bot_name
heroku create $bot_name
git init && echo 'git inited'
heroku git:remote -a $bot_name
git add . && git commit -am "init" && git push heroku master && echo "run.."
heroku ps:scale bot=1
#heroku logs -t
