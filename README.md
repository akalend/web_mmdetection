# web_mmdetection
Deep Learning School  graduftion project:  Web site detection images based on mmdetection 

## Описание

Проект реализован на база проекта mmdetection https://github.com/open-mmlab/mmdetection/ с предустановочной сетью RCNN R-50 натренированной на картинках датасета COCO (Common Objects in Context) https://cocodataset.org/


Детекция детекция происходит в модуле mmdetectionl.py


## Структура проекта

Проект реализованан в трех частях:

1. WEB Клиентская часть: Js скрипт, который выполняется в WEB браузере index.html
2. Серверная часть, обработки HTTP запросов. Скрит web.py.
3. Скрипт детекции объектов: mmdetectionl.py


## Алгоритм работы

Алгоритм избражет на рис 1. 
![Процесс детекции](/wb_detection.jpeg)

1. Пользователь через AJAX загружает картинку
2. WEB скрипт принимает картинку, преобразует её в png формат и сохраняет её, присвоив ей уникальное имя. 
Уникальное имя состоим из уникального идентификатора и типа файла. Пример: sid = 123, уникальное имя 123.png
3. WEB скрипт возвращает клиентскому приложению (Js скрипту) уникальнный идентификатор sid, который будет необходим для опроса шаг 7 и запускает таймер опроса.
4. Далее WEB скрипт запускает скрипт определения предметов на картинке: mmdetectionl.py и передает ему в качестве параметров уникальный идентификатор и точность выбора.
5. Скрипт детекции по уникальному идентификатору sid определяет имя файла и осуществляет на нем детекцию.
6. Результаты детекции mmdetectionl.py сохраняет в виде файла: [sid].out.png: например  123.out.png.
7. После загрузки файла, клиентский Js скрипт через AJAX по таймеру порверяет наличие файла [sid].out.png. 
8. Если файл [sid].out.png существует, то Js скрипт показывает его.

## Почему так сложно?

Дело в том, что процесс детекции осуществляется отностительно долгое время и некоторые сервера обрывают соединения, по этому сделана такая асинхронность. Такая реализация - более надежна.

