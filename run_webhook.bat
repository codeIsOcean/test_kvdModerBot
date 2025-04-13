@echo off
setlocal

:: Определим свободный порт: сначала пробуем 8000
set PORT=8000
netstat -ano | find ":8000" >nul
if %errorlevel%==0 (
    echo 🔁 Порт 8000 занят, переключаемся на 8080
    set PORT=8080
) else (
    echo ✅ Порт 8000 свободен
)

:: Запуск Cloudflare Tunnel
start "Cloudflare Tunnel" cmd /k "D:\cloudflared\cloudflared.exe tunnel --url http://localhost:%PORT%"

:: Ждём пару секунд
timeout /t 3 >nul

:: Запуск run_webhook.py с нужным Python
start "Webhook Bot" cmd /k "D:\test_kvdModerBot\.venv\Scripts\python.exe run_webhook.py"

endlocal

