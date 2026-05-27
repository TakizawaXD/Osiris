#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import shutil
import tempfile
import urllib.request
import zipfile

# Configuración de rutas
WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TARGET_SKILLS_DIR = os.path.join(WORKSPACE_ROOT, ".agent", "skills")

# URLs del repositorio
REPO_ZIP_URL = "https://github.com/sickn33/antigravity-awesome-skills/archive/refs/heads/main.zip"
INDEX_URL = "https://raw.githubusercontent.com/sickn33/antigravity-awesome-skills/main/data/skills_index.json"

COLOR_GREEN = "\033[92m"
COLOR_BLUE = "\033[94m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"

def print_banner():
    print(f"{COLOR_BLUE}{COLOR_BOLD}")
    print(" ========================================================")
    print("       INSTALADOR AUTOMÁTICO DE TODAS LAS HABILIDADES     ")
    print(" ========================================================")
    print(f"{COLOR_RESET}")
    print(f"Directorio Destino: {COLOR_BOLD}{TARGET_SKILLS_DIR}{COLOR_RESET}\n")

def main():
    print_banner()
    
    print(f"{COLOR_BLUE}[*]{COLOR_RESET} Descargando índice de habilidades...")
    try:
        with urllib.request.urlopen(INDEX_URL) as response:
            skills = json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"{COLOR_RED}[!] Error al descargar el índice: {e}{COLOR_RESET}")
        sys.exit(1)

    total_skills = len(skills)
    print(f"{COLOR_GREEN}[✓]{COLOR_RESET} Se detectaron {COLOR_BOLD}{total_skills}{COLOR_RESET} habilidades en el repositorio.")
    
    print(f"\n{COLOR_BLUE}[*]{COLOR_RESET} Descargando archivo ZIP completo (~15MB)...")
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "repo.zip")
        try:
            urllib.request.urlretrieve(REPO_ZIP_URL, zip_path)
            print(f"{COLOR_GREEN}[✓]{COLOR_RESET} Repositorio descargado.")
        except Exception as e:
            print(f"{COLOR_RED}[!] Error al descargar el archivo ZIP: {e}{COLOR_RESET}")
            sys.exit(1)

        print(f"{COLOR_BLUE}[*]{COLOR_RESET} Extrayendo todas las habilidades a {TARGET_SKILLS_DIR}...")
        
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                namelist = zip_ref.namelist()
                root_folder = namelist[0].split('/')[0] # antigravity-awesome-skills-main
                
                os.makedirs(TARGET_SKILLS_DIR, exist_ok=True)
                
                installed_count = 0
                for i, skill in enumerate(skills):
                    skill_id = skill["id"]
                    skill_rel_path = skill["path"]
                    
                    zip_prefix = f"{root_folder}/{skill_rel_path}/"
                    skill_members = [m for m in namelist if m.startswith(zip_prefix)]
                    
                    # Ruta alternativa si el path cambió
                    if not skill_members:
                        zip_prefix_alt = f"{root_folder}/skills/{skill_id}/"
                        skill_members = [m for m in namelist if m.startswith(zip_prefix_alt)]
                    
                    if skill_members:
                        dest_skill_dir = os.path.join(TARGET_SKILLS_DIR, skill_id)
                        os.makedirs(dest_skill_dir, exist_ok=True)
                        
                        for member in skill_members:
                            if member.endswith('/'):
                                continue
                            
                            # Obtener ruta de archivo relativa
                            if member.startswith(zip_prefix):
                                rel_path = member[len(zip_prefix):]
                            else:
                                rel_path = member[len(zip_prefix_alt):]
                                
                            dest_file_path = os.path.join(dest_skill_dir, rel_path)
                            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                            
                            with zip_ref.open(member) as source_file:
                                with open(dest_file_path, 'wb') as dest_file:
                                    shutil.copyfileobj(source_file, dest_file)
                        
                        installed_count += 1
                        if installed_count % 50 == 0 or installed_count == total_skills:
                            print(f" [*] Progreso: {installed_count}/{total_skills} habilidades instaladas...")
                
                print(f"\n{COLOR_GREEN}[✓] ¡Éxito! Se instalaron {installed_count} habilidades en total.{COLOR_RESET}")
                print(f"Las habilidades están listas para ser usadas por el agente en la carpeta .agent/skills/")
                
        except Exception as e:
            print(f"{COLOR_RED}[!] Error durante la extracción: {e}{COLOR_RESET}")
            sys.exit(1)

if __name__ == "__main__":
    main()
