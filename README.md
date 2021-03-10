Telegram бот для ведения дневника тренировок.

Для запуска своего бота необходимо создать в директории проекта файл .env, в котором следует указать свой Токен, 
полученный от BotFather (пример .env(example)):
```
API_TOKEN_TELEGRAM=xxxx:XXXXXXXXXXXXXXX
```
Файл .env необходим также и при работе через docker!
Для сборки образа контейнера необходимо выполнить.
```
cd telegram_TrainingDiary
docker build -t tg_workout_diary ./
```
В следующей команде запуска контейнера необходимо заменить `<../telegram_TrainingDiary>` на абсолютный путь к проекту:
```
docker run -d --name tgwd -v <../telegram_TrainingDiary>:/home tg_workout_diary
```
Чтобы войти в bash работающего контейнера:
```
docker exec -ti tgwd bash
```
Чтобы выключить и удалить контейнер:
```
docker stop tgwd
docker rm tgwd
```
Чтобы удалить образ:
```
docker rmi tg_workout_diary
```