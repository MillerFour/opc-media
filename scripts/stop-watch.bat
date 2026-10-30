@echo off
rem Stop the auto-commit watcher.
setlocal
cd /d "%~dp0.."
if not exist "scripts\.watch.pid" (
  echo [stop-watch] no pid file, watcher not running.
  exit /b 0
)
set /p PID=<scripts\.watch.pid
taskkill /PID %PID% /F >nul 2>&1
if errorlevel 1 (
  echo [stop-watch] pid %PID% not running.
) else (
  echo [stop-watch] killed pid %PID%.
)
del /q "scripts\.watch.pid" >nul 2>&1
exit /b 0
