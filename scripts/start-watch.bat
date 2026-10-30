@echo off
rem Start the auto-commit watcher in a minimized window.
rem Double-click this file, or put a shortcut in shell:startup to run at logon.
setlocal enabledelayedexpansion
cd /d "%~dp0.."
set "ROOT=%CD%"
set "ROOT=!ROOT:\=/!"

set "BASH="
for %%B in (
  "%ProgramFiles%\Git\bin\bash.exe"
  "%ProgramFiles%\Git\usr\bin\bash.exe"
  "%LOCALAPPDATA%\Programs\Git\bin\bash.exe"
  "%ProgramFiles(x86)%\Git\bin\bash.exe"
) do (
  if exist %%B if not defined BASH set "BASH=%%B"
)
if not defined BASH (
  for /f "delims=" %%P in ('where bash 2^>nul') do if not defined BASH set "BASH=%%P"
)
if not defined BASH (
  echo [start-watch] bash.exe not found. Please run: bash scripts/watch-commit.sh
  pause
  exit /b 1
)

start "wx-mp autocommit" /min "%BASH%" -c "cd '%ROOT%' && bash scripts/watch-commit.sh"
echo [start-watch] watcher started with: %BASH%
timeout /t 2 >nul
exit /b 0
