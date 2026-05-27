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

:: 1. Configurar rutas conocidas del repositorio
set "REPO_PATH=/media/andres/github/habilidades"
set "ALT_PATH=D:\github\habilidades"

:: Intentar acceder a las rutas en orden de prioridad
cd /d "%REPO_PATH%" 2>nul
if %errorlevel% neq 0 (
    cd /d "%ALT_PATH%" 2>nul
    if %errorlevel% neq 0 (
        cd /d "%~dp0" 2>nul
    )
)

:: 2. Si no se encuentra el script, solicitar ruta manualmente
if not exist "scripts\osiris_cli.py" (
    color 0C
    echo [AVISO] No se encontro 'scripts\osiris_cli.py' en la ruta automatica.
    echo.
    echo Introduce la ruta completa de la carpeta de tu repositorio:
    set /p "USER_PATH=Ruta: "
    if not "%USER_PATH%"=="" (
        cd /d "%USER_PATH%" 2>nul
    )
)

:: 3. Validar existencia final
if not exist "scripts\osiris_cli.py" (
    color 0C
    echo [ERROR CRITICO] Ruta invalida. No se puede iniciar Osiris CLI.
    goto end
)

:: 4. Verificar que Python este instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo [ERROR] Python no esta en el PATH del sistema o no esta instalado.
    echo Instala Python 3 para poder iniciar Osiris CLI.
    goto end
)

:: 5. Iniciar la Consola Interactiva
color 0F
python scripts/osiris_cli.py

:end
echo.
echo Presiona cualquier tecla para salir...
pause >nul
