@echo off
REM Указание пути, чтобы модули при импортировании могли найти нужные им модули/пакеты
REM . -- текущая папка
set PYTHONPATH=.
set PYTHON=C:\ProgramData\Anaconda3\python.exe

start %PYTHON% main.py
REM start %PYTHON% commands\coordinator.py
REM start %PYTHON% commands\command__damn\server.py
REM start %PYTHON% commands\command__fun\server.py
REM start %PYTHON% commands\command__weather_in_city\server.py