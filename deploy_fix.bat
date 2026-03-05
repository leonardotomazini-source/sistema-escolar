@echo off
REM matarPython processes
taskkill /IM python.exe /F 2>nul
timeout /t 1

REM Go to project directory
cd /d c:\Users\Professor\sistema_escolar

REM Git commands
git status
git add .
git commit -m "Fix: usar caminhos absolutos para database e melhorar estrutura"
git push origin main

echo.
echo COMMIT E PUSH CONCLUIDOS!
echo Aguarde 2-3 minutos para o Render fazer o re-deploy.
echo Depois visite: https://sistema-escolar-2q3l.onrender.com
pause
