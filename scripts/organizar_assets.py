#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil

# Configuración de rutas
SOURCE_BANNER = "/home/andres/.gemini/antigravity/brain/dc0561a6-4855-42ca-86c6-68c07a3a6e08/project_osiris_banner_1779901890042.png"
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_ASSETS_DIR = os.path.join(WORKSPACE_ROOT, "assets")
TARGET_BANNER = os.path.join(TARGET_ASSETS_DIR, "project_osiris_banner.png")

def main():
    print("=== Organizando Assets del Proyecto Osiris ===")
    
    # Crear directorio assets si no existe
    if not os.path.exists(TARGET_ASSETS_DIR):
        os.makedirs(TARGET_ASSETS_DIR)
        print(f"[+] Carpeta de assets creada en: {TARGET_ASSETS_DIR}")
        
    # Copiar el banner generado
    if os.path.exists(SOURCE_BANNER):
        try:
            shutil.copy(SOURCE_BANNER, TARGET_BANNER)
            print(f"[✓] Banner copiado exitosamente a: {TARGET_BANNER}")
        except Exception as e:
            print(f"[!] Error al copiar el banner: {e}")
    else:
        print(f"[!] Archivo origen no encontrado en: {SOURCE_BANNER}")
        print("Asegúrate de que la ruta del banner generado en la sesión es correcta.")

if __name__ == "__main__":
    main()
