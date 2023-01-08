## API для работы со спорт трекером [Sports Tracker](https://www.sports-tracker.com).
Данный инструмент разработан для возможности автоматизации пользовательского взаимодействия со спорт трекером.
Основная цель создания **api-sports-tracker** - бекап всех тренировок записаных в Sports Tracker с возможность восстановления своих спортивных достижений на любом другом спортивном ресурсе, поддерживающего загрузку треков тренировок в формате GPX.  
Цель достигается в результате сохранения необходимой информации о тренеровках в локальной базе данных MySQL (БД) и экспорте треков в формате <key_workout>.gpx на локальный жесткий диск.   

### Подготовка к использованию инструмента.
Данный проект предназначен для пользователей приложения Sports Tracker. И для того, что бы использовать API необходимы предварительные шаги для настройки.
Потребуются следующие данные:
- Учётная запись на сайте [Sports Tracker](https://www.sports-tracker.com) (Логин / Пароль).
- Токен авторизации (STTAuthorization) учетной записи [Sports Tracker](https://www.sports-tracker.com). Получить токен можно с помощью браузера используя Инструменты веб-разработчика. При авторизации пользователя смотреть в инструменте веб-разработчика, Вкладка - "Сеть", выбрать сроку со значением "user" в столбце "файл" и в правом окошке раздел "Заголовки" скопировать и сохранить значение из STTAuthorization.  
- Клонировать проект api-sports-tracker `` git clone https://github.com/shutovn/api-sports-tracker.git ``
- Создать и заполнить файл .env (Использовать в качестве примера example_env.). Скопировать файл example_env в файл .env и в файле .env отредактировать желаемые значения переменных, а так же заполнить корректные учетные данные для приложения Sports Tracker. Для быстрого старта и корректной работы достаточно указать следующие переменные:  
`` MYSQLROOT = <password>  ``  
`` MYSQLPASS = <password>  ``  
`` LOGIN_SPORTS_TRACKER = <user_name>  ``  
`` PASS_SPORTS_TRACKER = <user_password>  ``  
`` TOKEN_SPORTS_TRACKER = <user_authorization_token>  `` 

### Запуск проекта.
Если все предварительные шаги для настройки проекта выполнены, то для того, что бы запустить проект и начать его использовать, необходимо использовать Docker:
- Для запуска проекта необходим Docker и Docker-compose.
- Переходим в директорию проекта `` cd <Path>/api-sports-tracker ``
- Запускаем контейнеры `` docker-compose up -d ``
- Проверяем все ли контейнеры в статусе UP `` docker-compose ps ``

### Тест api-sports-tracker.
После успешного запуска проекта api-sports-tracker должны быть доступны два контейнера:
- db_workout, БД, к которой можно подключиться с помощью команды `` mysql -u workout -h 127.0.0.1 -P 3307 -D workout -p ``
- python_app_workout, приложение написаное на Python ( фреймворк Flask ) доступное на порту 5001, http://127.0.0.1:5001/route

Тест приложения:
`` curl http://127.0.0.1:5001/hello ``   
Возвращает строку с приветствием и текущим timestamp.

`` curl http://127.0.0.1:5001/test_mysql ``   
Вернет либо пустой массив, если данных в БД еще нет, либо массив данных JSON из таблицы workouts.

### Как использовать api-sports-tracker
`` curl http://127.0.0.1:5001/workouts_json ``   
Возвращает JSON с последними 10-тью тренировками. Ничего никуда не записывает.

`` curl http://127.0.0.1:5001/workout_last ``   
Запрашивает JSON с последними 50-тью тренировками. И записывает их в БД. запись прекращается, как только значение key workout встречается в БД. При первом запуске данного route необходимо указать в коде значение count = вашему ко-ву тренировок (можно больше). После первого запуска и записи всех тренировок в БД, можно сократить кол-во до 15-20 тренировок. Записываться в БД будут только новые тренировки из запрошенных (15-20), но тогда и "забирать" тренировки нужно чаще, чем вы фиксируете 15-20 своих занятий.

`` curl http://127.0.0.1:5001/export_workout ``   
Экспортирует файл трека тренировки если в БД значение поле export=0 и устанвливает поле export=1.

`` curl http://127.0.0.1:5001/update_workout_description ``   
Обновление записи поля description в БД если оно различается с описанием тренировки на сайте [Sports Tracker](https://www.sports-tracker.com).
