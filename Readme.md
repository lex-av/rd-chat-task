##  Websockets chat

Данный репозиторий содержит пакеты сервера и клиента, реализующие асинхронный
чат через websockets.

### Функционал сервера:

- на TCP порт принимает запросы от клиентов;
- поддерживает минимум 2-х клиентов единовременно;
- доставляет сообщение адресату;
- об успехе или неуспехе сообщает отправителю *;
- логирует сообщения клиентов в syslog.

### Функционал клиентов:

- получают сообщения от сервера;
- отправляют сообщения;
- получают подтверждение о доставке*.

### Требования к разработке

- ОС: Oracle Linux;
- ЯП: Python 3.9+ с учётом более новых версий;
- использование сторонних библиотек;
- хорошая читабельность кода;
- сборка и установка проекта через setuptools.

### Сборка и установка пакета

Для данной задачи было решено использовать инструмент setuptools. Поэтому для сборки и установки
пакета нужно использовать следующие команды в директории проекта (рекомендуется предварительно установить venv):

построение пакета:

    python setup.py sdist

Утановка сформированного пакета:

    pip install dist/websockets-chat-0.1.tar.gz

### Запуск и использование утилит

Пример команды для запуска сервера:

    server --ip=localhost --port=6078

Пример команды для запуска сервера:

    client --ip=localhost --port=6078

После запуска сервер переходит в режим ожидания клиентов. Для начала работы необходимо подключение двух клиентов.
Для клиента предусмотрены следующие стадии общения с сервером:
1. Регистрация - ввод и отправка уникального ника на сервер
2. Объединение в пару со вторым пользователем - отправка на сервер ника собеседника
3. Обмен сообщениями - отправка сообщений между клиентами
4. Выход с сервера с помощью отправки сообщения :quit:

Для объединения пользователей в пару оба пользователя должны быть зарегистрированы (то есть должны отправить свои
ники на сервер и получить подтверждение).
После окончания обмена сообщениями пользователи могут выйти из чата командой :quit: или с помощью сочетания
клавиш ctrl-c

### Примечания*

Из требуемого функционала не удалось реализовать лишь один пункт - отправку сообщения клиенту с
подтверждением доставки его сообщения. Тем не менее, для пользователя реализовано оповещение
об отправке его сообщения с сервера адресату и оповещение выхода адресата из чата
