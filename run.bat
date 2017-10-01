@echo off
REM Указание пути, чтобы модули при импортировании могли найти нужные им модули/пакеты
REM . -- текущая папка
set PYTHONPATH=.
set PYTHON=C:\ProgramData\Anaconda3\python.exe

start %PYTHON% main.py
start %PYTHON% commands\coordinator.py
start %PYTHON% commands\command__damn\damn_server.py
start %PYTHON% commands\command__fun\fun_server.py
start %PYTHON% commands\command__weather_in_city\weather_server.py