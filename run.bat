@echo off
REM Указание пути, чтобы модули при импортировании могли найти нужные им модули/пакеты
REM . -- текущая папка
set PYTHONPATH=.;

start C:\ProgramData\Anaconda3\python.exe main.py
start C:\ProgramData\Anaconda3\python.exe commands\coordinator.py
start C:\ProgramData\Anaconda3\python.exe commands\command__damn\damn_server.py
start C:\ProgramData\Anaconda3\python.exe commands\command__fun\fun_server.py
start C:\ProgramData\Anaconda3\python.exe commands\command__weather_in_city\weather_server.py