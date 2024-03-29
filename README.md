# huntflow_test
 Сервис по переносу данных из xlsx файлов в БД через API.
 
 (с) Николай Наумов
 ## Описание
 Сервис может принимать в качестве переметров командной строки:
  * папку с файлами (--folder)
  * токен (--token)
  * флаг восстановления (--restore)
 
 Настройки по умолчанию записаны в конфигурационном файле.
  
  Сервис работает по принципу разделения логики: сначала мы получаем список файлов (реализована возможность 
  обработки нескольких файлов), затем эти файлы парсятся, создаются объекты класса Candidate, после чего начинаются 
  действия с API. Дейтвия с API: сначала получаем общие данные о вакансиях и статусах, далее для каждого кандидата отправляем и парсим резюме (если нашли), обновляем объект 
  кандидата (в сервисе), далее добавляем кандидата через API уже с обновленными данными и добавляем его на вакансию.
  
  ## Сохранение состояния 
  Сервис сохраняет свое состояние, а именно данные из файлов, вакансии, статусы и прогресс отправки в API.
  Состояние сохраняется после каждого изменения. При запуске сервиса можно выбрать флаг --restore, тогда все, что
  возможно, сервис возьмет из дампа и продолжит с того момента, где остановился в прошлый раз. Реализовано через pickle, немного кривовато, но работает.
  При наличии времени можно было бы сделать лучше, как минимум проверяя сохранение дампа.
  
  ## Что можно улучшить?
  Вроде большинство крайних случаев проверяются, сильно сервис падать не должен, но проработаь с учетом
   специфики бизнес-логики конкретной базы можно (например, в голову приходить искать файлы резюме не по полному совпадению имени, а частично). Можно также попробовать переписать сервис асинхронно для ускроения обработки, добавить больше логирования. А вообще
   написано в попыхах, прошу строго не судить :)
