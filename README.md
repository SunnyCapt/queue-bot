queue-bot
=========
Telegram queue bot.

FИCK/FAQ/А_КАК
-------------
* -С чего начать?
        <br> Написать [@BotFather](https://telegram.me/BotFather) (не забудь добавить команды /next и /get у своего бота)
        
        git clone https://github.com/SunnyCapt/queue-bot.git
    Создать файл bot/local_config.py и задать все переменные, которые в bot/config.py равны None 
* -Как запустить?
    * На своем компе:
         <br> Придется искать надежный прокси и прописать его в \_\_main__.py 
         в конце, где закомментированная строка
          
            sudo apt-get install virtualenv
            virtualenv venv --no-site-packages --python=python3 
            source venv/bin/activate
            pipp install -r requirements.txt
            python bot
    * На серваке:
        
        Установить heroku cli, а потом:
           
            ./build.sh


---
Tg: [@SunnyCapt](https://telegram.me/SunnyCapt)

Email: sunny.capt@tuta.io 

