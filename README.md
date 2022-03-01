# Выполнение тестововых заданий

1. Сканер портов 

##  Формулировка задачи

Для проверки безопасности сетей, а также для сбора информации о работающих сетевых сервисах применяется процесс, называемый сканированием сети. Данное консольное приложение принимает на вход диапазон ip-адресов (например 192.168.1.0/24) и список портов (например 80, 443, 22, 21, 25). Результатом выполнения является список открытых портов с указанием удаленного хоста.

Также, как правило, порты 80и443слушают веб-сервер. В некоторых случаях в заголовке ответа в поле Server передается название службы. Реализована логика определения ПО сервера, слушающего порты 80 и 443.

#### Задача реализвована в скрипте с названием ```scanner_ports.py```

2. Подбор похожих доменов

## Формулировка задачи

Для оперативного поиска фишинговых ресурсов может применяться следующая
логика:

- составляется первичный набор ключевых слов, ассоциирующихся с целевой
  компанией

- при помощи набора *стратегий* (например, одна из них — подстановка схожих
  по написанию символов) формируется расширенный набор ключевых слов

- полученное на предыдущем шаге множество перемножается на некоторое
  множество доменных зон (`ru, com, net, org, biz` и т. п.)

- отправляются dns-запросы с целью получить IP-адрес по каждому из
  элементов списка

- домены, по которым удалось определить ip, попадают в отчет

Разработано консольное приложение, решающее описанную выше задачу.

***Входные данные*** — набор ключевых слов

***Результат*** — список доменов с ip-адресом.

Стратегии формирования набора ключевых слов описаны в таблице 1 ниже.

| Стратегия                                                  | Входное слово | Выходные слова                                                |
| ---------------------------------------------------------- | ------------- | ------------------------------------------------------------- |
| Добавление одного символа в<br>конец строки                | group-ib      | group-iba<br>group-ibb<br>group-ibc<br>...                    |
| Подстановка символа, схожего<br>по написанию (`homoglyph`) | group-ib      | gr0up-ib<br>group-1b<br>gr0up-1b                              |
| Выделение поддомена, т. е.<br>добавление точки             | group-ib      | group-i.b<br>grou.p-ib<br>gro.up-ib<br>gr.oup-ib<br>g.roup-ib |
| Удаление одного символа                                    | group-ib      | group-i<br>group-b<br>groupib<br>grou-ib                      |

Таблица 1 — Стратегии формирования ключевых слов.

Список доменных зон для подстановки: `com, ru, net, org, info, cn, es, top, au, pl, it, uk, tk, ml, ga, cf, us, xyz, top, site, win, bid` DNS-запросы должны отправляются параллельно.

#### Задача реализвована в скрипте с названием ```fishing_domains.py```


3. Парсер магазина приложений Google Play


## Формулировка задачи

В целях защиты бренда часто возникает задача найти мобильные приложения, содержащие определенное ключевое слово. Как правило, магазины не предоставляют API для этих целей, вследствие чего приходится парсить сайт.

Для Google Play можно получить список приложений по ключевому слову «сбербанк» на следующей [странице](https://play.google.com/store/search?q=%D1%81%D0%B1%D0%B5%D1%80%D0%B1%D0%B0%D0%BD%D0%BA&c=apps).

Разработано консольное приложение, которое осуществляет поиск по заданному ключевому слову и возвращает информацию о найденных приложениях в виде объекта `json`.

Для каждого найденного приложения возвращена следующая информация:

- название (`name`)

- автор (`author`)

- средняя оценка (`average_rating`)

- url страницы приложения (`link`)

- описание (`description`)

- категория (`category`)

- количество оценок (`number_of_ratings`)

- последнее обновление (`last_update`)

Пример конечного `json`  файла по ключевому слову (`сбербанк`) приведет в директории `/google_play_parser/data`  .

- Рассматривается весь результат поиска (все приложения).

- У некоторых приложений искомое ключевое слово не присутствует ни в
  названии, ни в описании, поэтому такие приложения не включаются в итоговый файл.

- Обработка сайтов происходит параллельно.

#### Задача реализвована в скрипте с названием ```google_play_parser.py```
