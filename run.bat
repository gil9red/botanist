@echo off
REM Указание пути, чтобы модули при импортировании могли найти нужные им модули/пакеты
set PYTHON=C:\ProgramData\Anaconda3\python.exe

start %PYTHON% main.py
start %PYTHON% commands\coordinator.py
start %PYTHON% commands\command__calc\server.py
start %PYTHON% commands\command__damn\server.py
start %PYTHON% commands\command__duckduckgo\server.py
start %PYTHON% commands\command__exchange_rate\server.py
start %PYTHON% commands\command__fun\server.py
start %PYTHON% commands\command__test_get_attachment\server.py
start %PYTHON% commands\command__text_converter\server.py
start %PYTHON% commands\command__weather_in_city\server.py