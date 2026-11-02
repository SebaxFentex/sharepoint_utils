@echo off
cd /d "%~dp0.."
if exist ".env" (
    uv run --env-file .env python -m sharepoint_utils
) else (
    uv run python -m sharepoint_utils
)
if errorlevel 1 pause
