# Результаты сканирования сайтов

| URL сайта | Время обработки | Кол-во найденных ссылок | Имя файла с результатом |
| --- | --- | --- | --- |
| http://crawler-test.com/ | 00:00:43 | 634 | crawler-test.xml |
| http://google.com/ | 10:49:58 | 371 437 | google.xml |
| https://stackoverflow.com | 28:41:28 | 2 128 676 | stackoverflow.html |
| https://vk.com | 11:25:41 | 413 271 | vk.xml |
| https://dzen.ru | 00:00:00 | - | - |

Парсинг всех сайтов кроме crawler-test.com был вручную остановлен, т.к. ссылок для обработки слишком много и парсить может бесконечно.

https://dzen.ru не распарсил, потому что там требуется обработка JavaScript'а, и я не нашел способ сделать это стандартными средствами Python.