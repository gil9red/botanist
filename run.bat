@echo off
REM Указание пути, чтобы модули при импортировании могли найти нужные им модули/пакеты
set PYTHON=C:\Users\ipetrash\AppData\Local\Continuum\Anaconda3\python.exe

start %PYTHON% main_vk_bot.py
start %PYTHON% commands\coordinator.py
start %PYTHON% commands\command__calc\server.py
start %PYTHON% commands\command__damn\server.py
start %PYTHON% commands\command__duckduckgo\server.py
start %PYTHON% commands\command__exchange_rate\server.py
start %PYTHON% commands\command__fun\server.py
start %PYTHON% commands\command__get_image_info\server.py
start %PYTHON% commands\command__gif\server.py
start %PYTHON% commands\command__qrcode\server.py
start %PYTHON% commands\command__test_get_attachment\server.py
start %PYTHON% commands\command__text_converter\server.py
start %PYTHON% commands\command__weather_in_city\server.py
start %PYTHON% commands\command__wikipedia\server.py