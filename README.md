Telegram бот для ведения дневника тренировок.

Для запуска своего бота необходимо создать в директории проекта файл .env, в котором следует указать свой Токен, полученный от BotFather:
```
API_TOKEN_TELEGRAM=xxxx:XXXXXXXXXXXXXXX
```
Файл .env необходим также и при работе через docker!
Для сборки образа контейнера необходимо выполнить.
```
docker build -t tg_workout_diary ./
```
В следующей команде запуска контейнера необходимо заменить `local_project_path` на локальный путь проекта:
```
docker run -d --name tgwd -v /local_project_name/docker_db:/home/docker_db tg_workout_diary
```
Чтобы войти в bash работающего контейнера:
```
docker exec -ti tgwd bash
```
