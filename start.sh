#!/bin/sh

# Запуск первого модуля
python3 main.py &

# Запуск второго модуля
python3 sockets_server.py &

# Ожидание завершения всех фонов процессов
wait
