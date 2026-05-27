@echo off
:: ==========================================
::   PROYECTO OSIRIS - CLIENTE DE TERMINAL
:: ==========================================
:: Este archivo permite iniciar la consola de Osiris
:: directamente desde tu Escritorio en Windows.

title Proyecto Osiris CLI Launcher
color 0B
cls

echo ==================================================
echo   Iniciando Terminal de Proyecto Osiris...
echo ==================================================
echo.

:: 1. Cambiar al directorio del script
cd /d "%~dp0"

:: 2. Validar existencia final de osiris_cli.py
if not exist "scripts\osiris_cli.py" (
    color 0C
    echo [ERROR CRITICO] No se encontro 'scripts\osiris_cli.py' en la carpeta actual.
    echo Asegurate de ejecutar este archivo .bat desde la raiz del repositorio Osiris.
    goto end
)

:: 3. Verificar que Python este instalado (intentar 'python' y 'py')
set PYTHON_CMD=
python --version >nul 2>&1
if %errorlevel% equ 0 (
    set PYTHON_CMD=python
) else (
    py --version >nul 2>&1
    if %errorlevel% equ 0 (
        set PYTHON_CMD=py
    )
)

if "%PYTHON_CMD%"=="" (
    color 0C
    echo [ERROR] Python no esta instalado o no se encuentra en el PATH del sistema.
    echo Instala Python 3 para poder iniciar Osiris CLI.
    goto end
)

:: 4. Iniciar la Consola Interactiva
color 0F
%PYTHON_CMD% scripts/osiris_cli.py

:end
echo.
echo Presiona cualquier tecla para salir...
pause >nul
