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

# Estilos de consola
COLOR_GREEN = "\033[92m"
COLOR_BLUE = "\033[94m"
COLOR_YELLOW = "\033[93m"
COLOR_RED = "\033[91m"
COLOR_BOLD = "\033[1m"
COLOR_RESET = "\033[0m"

def print_banner():
    print(f"{COLOR_BLUE}{COLOR_BOLD}")
    print(" ========================================================")
    print("       IMPORTADOR DE HABILIDADES ANTIGRAVITY AWESOME     ")
    print(" ========================================================")
    print(f"{COLOR_RESET}")
    print(f"Workspace Destino: {COLOR_BOLD}{TARGET_SKILLS_DIR}{COLOR_RESET}\n")

def fetch_index():
    print(f"{COLOR_BLUE}[*]{COLOR_RESET} Descargando índice de habilidades desde GitHub...")
    try:
        with urllib.request.urlopen(INDEX_URL) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"{COLOR_RED}[!] Error al descargar el índice: {e}{COLOR_RESET}")
        sys.exit(1)

def get_available_categories(skills):
    categories = set()
    for s in skills:
        cat = s.get("category", "uncategorized")
        if cat:
            categories.add(cat)
    return sorted(list(categories))

def get_bundles():
    return {
        "Essentials": ["bash-linux", "bash-scripting", "brainstorming", "claude-code-guide", "error-handling-patterns", "testing-patterns", "prompt-engineering", "uncle-bob-craft"],
        "Web Wizard": ["angular", "angular-state-management", "browser-extension-builder", "frontend-dev-guidelines", "radix-ui-design-system", "tailwind-design-system", "tailwind-patterns", "react-best-practices", "react-ui-patterns"],
        "Full-Stack Developer": ["backend-dev-guidelines", "database-design", "database-architect", "graphql", "nextjs-best-practices", "nestjs-expert", "prisma-expert", "drizzle-orm-expert", "postgres-best-practices"],
        "QA & Testing": ["e2e-testing-patterns", "mock-hunter", "awt-e2e-testing", "browser-automation"],
        "Security Developer": ["active-directory-attacks", "constant-time-analysis", "agentic-actions-auditor", "007"],
        "DevOps & Cloud": ["cloudformation-best-practices", "github-actions-templates", "monorepo-architect", "nx-workspace-patterns"],
        "Observability & Monitoring": ["error-detective", "agenttrace-session-audit", "monte-carlo-push-ingestion", "monte-carlo-validation-notebook"]
    }

def download_and_extract_skills(selected_skills):
    if not selected_skills:
        print(f"{COLOR_YELLOW}[!] No se seleccionó ninguna habilidad para instalar.{COLOR_RESET}")
        return

    print(f"\n{COLOR_BLUE}[*]{COLOR_RESET} Descargando repositorio completo (~15MB ZIP)...")
    
    # Crear directorio temporal
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "repo.zip")
        
        # Descargar el ZIP con indicador de progreso simple
        try:
            urllib.request.urlretrieve(REPO_ZIP_URL, zip_path)
            print(f"{COLOR_GREEN}[✓]{COLOR_RESET} Repositorio descargado correctamente.")
        except Exception as e:
            print(f"{COLOR_RED}[!] Error al descargar el ZIP: {e}{COLOR_RESET}")
            return

        print(f"{COLOR_BLUE}[*]{COLOR_RESET} Procesando y extrayendo habilidades seleccionadas...")
        
        # Abrir el ZIP
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Obtener la lista de archivos en el zip
                namelist = zip_ref.namelist()
                root_folder = namelist[0].split('/')[0] # usualmente "antigravity-awesome-skills-main"
                
                os.makedirs(TARGET_SKILLS_DIR, exist_ok=True)
                
                success_count = 0
                for i, skill in enumerate(selected_skills):
                    skill_id = skill["id"]
                    skill_rel_path = skill["path"]
                    
                    # El prefijo de la carpeta del skill en el ZIP
                    zip_prefix = f"{root_folder}/{skill_rel_path}/"
                    
                    # Encontrar todos los archivos que pertenecen a este skill
                    skill_members = [m for m in namelist if m.startswith(zip_prefix)]
                    
                    if not skill_members:
                        # Re-intentar buscando directamente en skills/
                        zip_prefix_alt = f"{root_folder}/skills/{skill_id}/"
                        skill_members = [m for m in namelist if m.startswith(zip_prefix_alt)]
                        
                    if skill_members:
                        # Crear el directorio destino del skill
                        dest_skill_dir = os.path.join(TARGET_SKILLS_DIR, skill_id)
                        os.makedirs(dest_skill_dir, exist_ok=True)
                        
                        # Extraer archivos individualmente mapeando las rutas
                        for member in skill_members:
                            # Ignorar directorios en la lista de namelist
                            if member.endswith('/'):
                                continue
                            
                            # Obtener la ruta relativa del archivo dentro del skill
                            if member.startswith(zip_prefix):
                                rel_file_path = member[len(zip_prefix):]
                            else:
                                rel_file_path = member[len(zip_prefix_alt):]
                                
                            dest_file_path = os.path.join(dest_skill_dir, rel_file_path)
                            os.makedirs(os.path.dirname(dest_file_path), exist_ok=True)
                            
                            # Leer y escribir el archivo
                            with zip_ref.open(member) as source_file:
                                with open(dest_file_path, 'wb') as dest_file:
                                    shutil.copyfileobj(source_file, dest_file)
                        
                        success_count += 1
                        print(f" [{i+1}/{len(selected_skills)}] {COLOR_GREEN}✓{COLOR_RESET} Instalado: {COLOR_BOLD}{skill_id}{COLOR_RESET}")
                    else:
                        print(f" [{i+1}/{len(selected_skills)}] {COLOR_RED}✗{COLOR_RESET} No se encontró en el ZIP: {skill_id} (ruta esperada: {skill_rel_path})")

                print(f"\n{COLOR_GREEN}[✓] ¡Proceso completado! Se instalaron {success_count} de {len(selected_skills)} habilidades con éxito.{COLOR_RESET}")
                print(f"Todas las habilidades se encuentran listas en: {COLOR_BOLD}{TARGET_SKILLS_DIR}{COLOR_RESET}")
        
        except Exception as e:
            print(f"{COLOR_RED}[!] Error al procesar el archivo ZIP: {e}{COLOR_RESET}")

def main():
    print_banner()
    skills = fetch_index()
    total_skills = len(skills)
    print(f"{COLOR_GREEN}[✓]{COLOR_RESET} Se encontraron {COLOR_BOLD}{total_skills}{COLOR_RESET} habilidades disponibles.\n")

    while True:
        print("Seleccione una opción de instalación:")
        print(f" {COLOR_GREEN}1.{COLOR_RESET} Instalar TODO ({total_skills} habilidades - ¡Atención: puede saturar el contexto del agente!)")
        print(f" {COLOR_GREEN}2.{COLOR_RESET} Instalar un Rol / Bundle (Curados y optimizados)")
        print(f" {COLOR_GREEN}3.{COLOR_RESET} Instalar por Categorías (security, ai-ml, backend, etc.)")
        print(f" {COLOR_GREEN}4.{COLOR_RESET} Instalar habilidades específicas por nombre")
        print(f" {COLOR_GREEN}5.{COLOR_RESET} Salir")
        
        try:
            choice = input(f"\n{COLOR_BOLD}Opción > {COLOR_RESET}").strip()
        except KeyboardInterrupt:
            print("\nSaliendo...")
            sys.exit(0)

        if choice == '1':
            confirm = input(f"{COLOR_RED}[!] ¿Está seguro de que desea instalar las {total_skills} habilidades? (s/n): {COLOR_RESET}").strip().lower()
            if confirm == 's':
                download_and_extract_skills(skills)
                break
        elif choice == '2':
            bundles = get_bundles()
            print("\nRoles / Bundles disponibles:")
            for idx, (name, skill_list) in enumerate(bundles.items(), 1):
                print(f" {COLOR_BLUE}{idx}.{COLOR_RESET} {COLOR_BOLD}{name}{COLOR_RESET} ({len(skill_list)} habilidades)")
                print(f"    Muestra: {', '.join(skill_list[:4])}...")
            
            b_choice = input(f"\nSeleccione un Rol (1-{len(bundles)}) o enter para regresar: ").strip()
            if b_choice.isdigit() and 1 <= int(b_choice) <= len(bundles):
                selected_bundle_name = list(bundles.keys())[int(b_choice) - 1]
                target_ids = bundles[selected_bundle_name]
                selected_skills = [s for s in skills if s["id"] in target_ids]
                print(f"\n{COLOR_BLUE}[*]{COLOR_RESET} Preparando instalación para el Rol: {COLOR_BOLD}{selected_bundle_name}{COLOR_RESET}")
                download_and_extract_skills(selected_skills)
                break
        elif choice == '3':
            categories = get_available_categories(skills)
            print("\nCategorías disponibles:")
            # Mostrar categorías en columnas
            for idx, cat in enumerate(categories, 1):
                cat_count = len([s for s in skills if s.get("category") == cat])
                print(f" {COLOR_BLUE}{idx:2d}.{COLOR_RESET} {cat:<28s} ({cat_count} habilidades)")
                
            cat_choice = input(f"\nSeleccione una Categoría (1-{len(categories)}) o enter para regresar: ").strip()
            if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(categories):
                selected_cat = categories[int(cat_choice) - 1]
                selected_skills = [s for s in skills if s.get("category") == selected_cat]
                print(f"\n{COLOR_BLUE}[*]{COLOR_RESET} Instalando habilidades de la categoría: {COLOR_BOLD}{selected_cat}{COLOR_RESET}")
                download_and_extract_skills(selected_skills)
                break
        elif choice == '4':
            names_input = input("\nIngrese los nombres (IDs) de las habilidades separados por coma (ej. bash-linux, 007): ").strip()
            if names_input:
                target_ids = [n.strip() for n in names_input.split(',')]
                selected_skills = [s for s in skills if s["id"] in target_ids]
                
                found_ids = [s["id"] for s in selected_skills]
                missing_ids = [tid for tid in target_ids if tid not in found_ids]
                
                if missing_ids:
                    print(f"{COLOR_YELLOW}[!] Advertencia: Las siguientes habilidades no se encontraron en el catálogo y serán ignoradas: {', '.join(missing_ids)}{COLOR_RESET}")
                
                if selected_skills:
                    download_and_extract_skills(selected_skills)
                    break
        elif choice == '5':
            print("¡Hasta luego!")
            break
        else:
            print(f"{COLOR_RED}[!] Opción no válida. Intente de nuevo.{COLOR_RESET}\n")

if __name__ == "__main__":
    main()
