#!/usr/bin/env bash
echo "Iniciando Proyecto Osiris..."
cd "$(dirname "$0")"
python3 scripts/osiris_cli.py
if [ $? -ne 0 ]; then
    echo ""
    echo "Ocurrió un error al iniciar Osiris CLI."
    read -p "Presiona Enter para continuar..."
fi
