@echo off
setlocal EnableDelayedExpansion

echo [1] Запускаем Cloudflare Tunnel...
start "Tunnel" cmd /k cloudflared tunnel --url http://localhost:8000 > cloudflared.log

timeout /t 5 > nul

echo [2] Извлекаем URL из cloudflared.log...

set "WEBHOOK="
for /f "tokens=6" %%A in ('findstr /C:"Visit it at" cloudflared.log') do (
    set "WEBHOOK=%%A"
)

echo [3] Получен URL: !WEBHOOK!

if "!WEBHOOK!"=="" (
    echo ❌ Не удалось извлечь ссылку из cloudflared.log
    pause
    exit /b
)

echo [4] Обновляем .env...

(for /f "delims=" %%i in (.env) do (
    echo %%i | findstr /B /C:"WEBHOOK_HOST=" >nul || echo %%i
)) > .env.tmp

echo WEBHOOK_HOST=!WEBHOOK!>> .env.tmp
move /Y .env.tmp .env >nul

echo [5] Запускаем run_webhook.py...
start "" python run_webhook.py

endlocal
exit
