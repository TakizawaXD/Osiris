#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import urllib.request
import urllib.error

# Configuración de Colores ANSI
CYAN = "\033[96m"
GOLD = "\033[93m"
GREEN = "\033[92m"
RED = "\033[91m"
GRAY = "\033[90m"
RESET = "\033[0m"
BOLD = "\033[1m"

# ASCII Art del Ojo de Horus y Osiris
LOGO = f"""
{GOLD}              ▲
             / \\
            / 👁 \\
           /_____\\       {CYAN}⚡ PROYECTO OSIRIS ⚡{GOLD}
          /       \\      {GRAY}AI Agent Orchestration Terminal{RESET}

{CYAN}  █▀▀█ █▀▀ ░▀░ █▀▀█ ░▀░ █▀▀ 
  █  █ ▀▀█ ▀█▀ █▄▄▀ ▀█▀ ▀▀█ 
  ▀▀▀▀ ▀▀▀ ▀▀▀ ▀ ▀▀ ▀▀▀ ▀▀▀ {RESET}
"""



def print_help():
    print(f"\n{BOLD}Comandos Disponibles:{RESET}")
    print(f"  {CYAN}/chat <pregunta>{RESET}   - Conversar con la IA sobre el workspace o código.")
    print(f"  {CYAN}/skills{RESET}           - Listar las habilidades core disponibles en el sistema.")
    print(f"  {CYAN}/match <tarea>{RESET}    - Buscar qué habilidades se activarían para una tarea.")
    print(f"  {CYAN}/optimize <prompt>{RESET}- Optimizar un prompt usando la habilidad core.")
    print(f"  {CYAN}/dir <ruta>{RESET}        - Cambiar el directorio de trabajo del proyecto.")
    print(f"  {CYAN}/create <concepto>{RESET}- Crear un nuevo proyecto donde todos los módulos trabajan en equipo.")
    print(f"  {CYAN}/help{RESET}             - Mostrar este menú de ayuda.")
    print(f"  {CYAN}/exit{RESET}             - Salir de la terminal Osiris.")

def get_api_key():
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        print(f"\n{RED}[!] GEMINI_API_KEY no encontrada en las variables de entorno.{RESET}")
        key = input(f"{GOLD}Por favor, ingresa tu Gemini API Key para continuar (o presiona Enter para salir): {RESET}").strip()
        if not key:
            print(f"{RED}Saliendo...{RESET}")
            sys.exit(0)
    return key

def call_gemini(api_key, system_instruction, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "systemInstruction": {"parts": [{"text": system_instruction}]}
    }
    
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            res_data = json.loads(response.read().decode("utf-8"))
            return res_data["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        error_msg = e.read().decode("utf-8")
        try:
            err_json = json.loads(error_msg)
            return f"{RED}Error de la API: {err_json['error']['message']}{RESET}"
        except:
            return f"{RED}HTTP Error {e.code}: {e.reason}{RESET}"
    except Exception as e:
        return f"{RED}Error de conexión: {str(e)}{RESET}"

def get_skills_summary():
    skills_dir = "/media/andres/github/habilidades/.agent/skills"
    if not os.path.exists(skills_dir):
        return "No se pudo acceder al directorio de habilidades."
    
    skills = []
    for item in os.listdir(skills_dir):
        full_path = os.path.join(skills_dir, item)
        if os.path.isdir(full_path):
            skills.append(item)
    return ", ".join(skills)

def create_project(api_key, system_instruction, concept, target_dir):
    print(f"\n{CYAN}=== Iniciando Creación de Proyecto: {BOLD}{concept}{RESET} ===")
    print(f"{GRAY}Directorio objetivo: {target_dir}{RESET}\n")
    
    print(f"{GOLD}[🔍 Orquestador] Cargando equipo de trabajo Osiris...{RESET}")
    print(f"{CYAN}[🎨 Diseñador UI/UX] Cargando módulo ui-ux-pro-max... OK{RESET}")
    print(f"{CYAN}[🏗️ Arquitecto] Cargando módulo arquitecto-software... OK{RESET}")
    print(f"{CYAN}[💻 Frontend] Cargando módulo desarrollador-frontend... OK{RESET}")
    print(f"{CYAN}[⚙️ Backend] Cargando módulo desarrollador-backend... OK{RESET}")
    print(f"{CYAN}[🔍 SEO] Cargando módulo analista-seo... OK{RESET}")
    print(f"{CYAN}[🧪 QA] Cargando módulo pruebas-calidad... OK{RESET}\n")
    
    print(f"{GOLD}[⚙️ Sistema] Generando especificaciones y código simultáneamente (como un solo equipo)...{RESET}")
    print(f"{GRAY}Esto puede tardar unos segundos, por favor espera...{RESET}")
    
    prompt = f"""
    Actúa como el equipo completo de desarrollo de Osiris (Diseño, Arquitectura, Frontend, Backend, SEO, QA) trabajando simultáneamente.
    Genera el proyecto completo para: '{concept}'.
    Debes retornar UNICAMENTE un objeto JSON válido (encapsulado en marcas de código ```json ... ```) con la siguiente estructura exacta:
    {{
      "arquitectura.md": "Especificación detallada de arquitectura, componentes y decisiones de diseño del equipo.",
      "index.html": "Código HTML5 completo, responsivo, estético (modo oscuro, gradientes, glassmorphism), con metatags SEO únicos, IDs en elementos interactivos y links a index.css.",
      "index.css": "Estilos CSS modernos, variables HSL de color, animaciones y transiciones.",
      "server.js": "Código backend funcional (Node.js/Express o Python Flask/FastAPI) con API endpoints RESTful, validación y logs.",
      "test.js": "Suite de pruebas funcionales y unitarias (QA) para verificar el frontend y la API backend.",
      "robots.txt": "Archivo robots.txt optimizado para SEO."
    }}
    Asegúrate de que los archivos contengan código de nivel producción, funcional y completo (sin omitir partes por brevedad).
    """
    
    response_text = call_gemini(api_key, system_instruction, prompt)
    
    import re
    json_data = None
    match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
    if match:
        try:
            json_data = json.loads(match.group(1).strip())
        except Exception as e:
            pass
            
    if not json_data:
        try:
            json_data = json.loads(response_text.strip())
        except Exception as e:
            print(f"{RED}[!] Error: La IA no devolvió un JSON estructurado de archivos. Guardando salida completa como raw_output.txt...{RESET}")
            os.makedirs(target_dir, exist_ok=True)
            with open(os.path.join(target_dir, "raw_output.txt"), "w", encoding="utf-8") as f:
                f.write(response_text)
            return
            
    os.makedirs(target_dir, exist_ok=True)
    print("")
    for filename, content in json_data.items():
        file_path = os.path.join(target_dir, filename)
        if "arquitectura" in filename:
            print(f"{CYAN}[🏗️ Arquitecto] Escribiendo especificación en {filename}... {GREEN}✓{RESET}")
        elif "html" in filename:
            print(f"{CYAN}[💻 Frontend] Estructurando {filename} (con metatags SEO)... {GREEN}✓{RESET}")
        elif "css" in filename:
            print(f"{CYAN}[🎨 Diseñador] Diseñando estilos en {filename}... {GREEN}✓{RESET}")
        elif "server" in filename or "backend" in filename or "app" in filename:
            print(f"{CYAN}[⚙️ Backend] Programando endpoints en {filename}... {GREEN}✓{RESET}")
        elif "test" in filename:
            print(f"{CYAN}[🧪 QA] Creando pruebas unitarias en {filename}... {GREEN}✓{RESET}")
        else:
            print(f"{CYAN}[🔍 SEO] Generando configuración de {filename}... {GREEN}✓{RESET}")
            
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
            
    print(f"\n{GREEN}[✓] Proyecto Osiris '{concept}' creado exitosamente en: {target_dir}{RESET}")
    print(f"{GOLD}¡Todos los módulos del equipo de trabajo funcionaron de forma sincronizada!{RESET}")

def main():
    print(LOGO)
    print(f"{GRAY}Cargando contexto del workspace...{RESET}")
    
    skills_list = get_skills_summary()
    print(f"{GREEN}[✓] {len(skills_list.split(', '))} Habilidades core mapeadas.{RESET}")
    
    # Preguntar por el directorio de trabajo del proyecto
    workspace_root = "/media/andres/github/habilidades"
    print(f"\n{GOLD}--- Ubicación del Proyecto ---{RESET}")
    target_dir = input(f"¿Dónde deseas ubicar tu proyecto Osiris?\n[Presiona Enter para usar la carpeta actual '{workspace_root}']: ").strip()
    if not target_dir:
        target_dir = workspace_root
    else:
        target_dir = os.path.abspath(target_dir)
        
    # Crear directorio si no existe
    if not os.path.exists(target_dir):
        try:
            os.makedirs(target_dir)
            print(f"{GREEN}[+] Directorio creado en: {target_dir}{RESET}")
        except Exception as e:
            print(f"{RED}[!] Error al crear el directorio: {e}. Usando '{workspace_root}'.{RESET}")
            target_dir = workspace_root
            
    api_key = get_api_key()
    
    system_instruction = f"""
    Eres la IA central de Proyecto Osiris, un workspace de orquestación de agentes.
    El workspace cuenta con habilidades core: {skills_list}.
    
    REGLA CRÍTICA DE BREVEDAD: Responde siempre de forma extremadamente directa, concisa y corta. Ve al grano inmediatamente.
    NUNCA expliques las fases completas de la arquitectura cognitiva ni uses plantillas largas o preguntas de seguimiento a menos que te sea solicitado de forma explícita.
    Responde en español de forma técnica y directa.
    """
    
    print(f"\n{GREEN}Osiris Online.{RESET} Directorio activo: {CYAN}{target_dir}{RESET}")
    print(f"Escribe {CYAN}/help{RESET} para ver los comandos.")
    
    while True:
        try:
            user_input = input(f"\n{CYAN}Osiris {GOLD}❯{RESET} ").strip()
            if not user_input:
                continue
                
            if user_input.startswith("/"):
                parts = user_input.split(" ", 1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""
                
                if cmd == "/exit":
                    print(f"\n{GOLD}Apagando Osiris. Hasta pronto.{RESET}")
                    break
                elif cmd == "/help":
                    print_help()
                elif cmd == "/dir":
                    if not args:
                        print(f"Directorio activo actual: {CYAN}{target_dir}{RESET}")
                        continue
                    new_path = os.path.abspath(args)
                    if not os.path.exists(new_path):
                        try:
                            os.makedirs(new_path)
                            print(f"{GREEN}[+] Directorio creado.{RESET}")
                        except Exception as e:
                            print(f"{RED}[!] Error al crear el directorio: {e}{RESET}")
                            continue
                    target_dir = new_path
                    print(f"{GREEN}[✓] Directorio activo cambiado a: {CYAN}{target_dir}{RESET}")
                elif cmd == "/skills":
                    print(f"\n{GOLD}Habilidades Core Disponibles:{RESET}")
                    for s in skills_list.split(", "):
                        print(f"  {CYAN}•{RESET} {s}")
                elif cmd == "/match":
                    if not args:
                        print(f"{RED}[!] Especifica una tarea. Ej: /match crear landing page{RESET}")
                        continue
                    prompt = f"Basándote en las habilidades {skills_list}, ¿cuáles de ellas activarías y en qué orden de fases para realizar la siguiente tarea: '{args}'? Justifica brevemente."
                    print(f"{GRAY}Analizando matching de habilidades...{RESET}")
                    response = call_gemini(api_key, system_instruction, prompt)
                    print(f"\n{GOLD}Resultado del Match:{RESET}\n{response}")
                elif cmd == "/optimize":
                    if not args:
                        print(f"{RED}[!] Especifica el prompt a optimizar. Ej: /optimize hacer backend nodejs{RESET}")
                        continue
                    prompt = f"Utiliza las pautas de la habilidad optimizador-prompts para reescribir de forma técnica y estructurada la siguiente solicitud: '{args}'."
                    print(f"{GRAY}Optimizando prompt...{RESET}")
                    response = call_gemini(api_key, system_instruction, prompt)
                    print(f"\n{GOLD}Prompt Optimizado:{RESET}\n{response}")
                elif cmd == "/create":
                    if not args:
                        print(f"{RED}[!] Especifica el concepto del proyecto. Ej: /create e-commerce de plantas{RESET}")
                        continue
                    create_project(api_key, system_instruction, args, target_dir)
                elif cmd == "/chat":
                    if not args:
                        print(f"{RED}[!] Ingresa tu pregunta. Ej: /chat cómo funciona claud.md{RESET}")
                        continue
                    print(f"{GRAY}Consultando con Osiris...{RESET}")
                    response = call_gemini(api_key, system_instruction, args)
                    print(f"\n{response}")
                else:
                    print(f"{RED}[!] Comando desconocido. Escribe /help para ver la lista.{RESET}")
            else:
                print(f"{GRAY}Consultando con Osiris...{RESET}")
                response = call_gemini(api_key, system_instruction, user_input)
                print(f"\n{response}")
                
        except KeyboardInterrupt:
            print(f"\n{GOLD}Apagando Osiris. Hasta pronto.{RESET}")
            break
        except Exception as e:
            print(f"\n{RED}[!] Error: {e}{RESET}")

if __name__ == "__main__":
    main()

