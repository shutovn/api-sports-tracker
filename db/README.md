### Схема БД workout


# Таблица workout.activity
Содержит информацию о id и названиях тренировок. (На данном этапе заполняется в ручную)
- **id_activity** - id записи в таблицы activity
- **activityid** - id активности на ресурсе [Sports Tracker](https://www.sports-tracker.com)
- **name_activity** - наименование тренировки
- **description** - перевод на русский язык наименования

# Таблица workout.workouts
Содержит информацию о тренировках.
- **id_workout** - id записи в таблицы workouts
- **date_create** - Timestamp, формата ГГГГ-ММ-ДД ЧЧ:ММ:СС, создание записи.
- **date_update** - Timestamp, обновления записи.
- **name** - Имя тренировки (На сайте это дата и время начала тренровки).
- **starttime** - Время в формате Milliseconds since Unix Epoch ( начало тренировки ).
- **stoptime** - Время в формате Milliseconds since Unix Epoch ( конец тренировки ).
- **totaltime** - Время длительности тренировки в секундах.
- **activityid** - id активности на ресурсе [Sports Tracker](https://www.sports-tracker.com)
- **totaldistance** - Дистанция тренировки в метрах.
- **avgspeed** - Средняя скорость в формате м/с.
- **workoutkey** - Уникальный идентификатор/ключ тренировки.
- **recoverytime** - Время восстановления в формате в секундах.
- **energy** - Потраченные kcal за тренировку.
- **export** - **0** - тренировка не экспортирована в файл GPX. **1** - тренировка экспортирована в файл GPX.
- **description** - Описание тренировки.

# Таблица workout.workouts_gpx
Содержит информацию о экспорте тренировок.
- **id_gpx** - id записи в таблицы workouts_gpx
- **date_create** - Timestamp, формата ГГГГ-ММ-ДД ЧЧ:ММ:СС, экспорта тренировки в файл формата GPX.
- **id_workout** - id тренировки из таблицы workouts
- **path_gpx** - путь и имя файла записаного при экспорте в формате < директория хранения файлов >/< workoutkey >.gpx
