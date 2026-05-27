#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import urllib.request
import urllib.error

# Activación de colores ANSI en terminal Windows (CMD / PowerShell)
if os.name == 'nt':
    import ctypes
    try:
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
    except Exception:
        pass

# Determinar rutas relativas de forma dinámica
script_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(script_dir)

# Cargar UI-UX Pro Max Skill usando rutas relativas
sys.path.append(os.path.join(repo_root, ".agent", "skills", "ui-ux-pro-max", "scripts"))
try:
    from design_system import DesignSystemGenerator
    has_ui_ux_pro_max = True
except Exception:
    has_ui_ux_pro_max = False

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

def call_gemini(api_key, system_instruction, prompt, model_name="gemini-2.5-flash"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
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
    skills_dir = os.path.join(repo_root, ".agent", "skills")
    if not os.path.exists(skills_dir):
        return "No se pudo acceder al directorio de habilidades."
    
    skills = []
    for item in os.listdir(skills_dir):
        full_path = os.path.join(skills_dir, item)
        if os.path.isdir(full_path):
            skills.append(item)
    return ", ".join(skills)

def clean_code_block(text):
    text = text.strip()
    import re
    match = re.match(r'^```[a-zA-Z0-9#+\-_]*\s*(.*?)\s*```$', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text

def call_imagen_api(api_key, prompt, aspect_ratio="16:9"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:generateImages?key={api_key}"
    headers = {"Content-Type": "application/json"}
    data = {
        "prompt": prompt,
        "numberOfImages": 1,
        "outputMimeType": "image/jpeg",
        "aspectRatio": aspect_ratio
    }
    req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=35) as response:
        res_data = json.loads(response.read().decode("utf-8"))
        img_bytes_b64 = res_data["generatedImages"][0]["image"]["imageBytes"]
        import base64
        return base64.b64decode(img_bytes_b64)

def extract_json(text):
    text = text.strip()
    import re
    match = re.search(r'```json\s*(.*?)\s*```', text, re.DOTALL)
    if match:
        text = match.group(1).strip()
    else:
        match_generic = re.search(r'```\s*(.*?)\s*```', text, re.DOTALL)
        if match_generic:
            text = match_generic.group(1).strip()
    try:
        return json.loads(text)
    except Exception:
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end+1])
            except Exception:
                pass
        return None

def download_images(api_key, concept, target_dir):
    # Función legacy mantenida por compatibilidad de firma.
    pass

def create_project(api_key, system_instruction, concept, target_dir):
    print(f"\n{CYAN}=== Configuración del Proyecto Osiris ==={RESET}")
    
    # 1. Solicitar Nombre del Proyecto
    project_name = input(f"{GOLD}Nombre de la carpeta/proyecto (ej: ecommerce-cafe): {RESET}").strip()
    while not project_name:
        print(f"{RED}[!] El nombre del proyecto es obligatorio.{RESET}")
        project_name = input(f"{GOLD}Nombre del proyecto: {RESET}").strip()
        
    # 2. Solicitar Título de la Página
    page_title = input(f"{GOLD}Título/Nombre visible de la página (ej: Café Supremo): {RESET}").strip()
    while not page_title:
        print(f"{RED}[!] El título de la página es obligatorio.{RESET}")
        page_title = input(f"{GOLD}Nombre/Título de la página: {RESET}").strip()
        
    # 3. Solicitar Stack Tecnológico
    print(f"\n{GOLD}Ejemplos de Stacks comunes:{RESET}")
    print(f"  • HTML/CSS/JS (Vanilla con Express)")
    print(f"  • React con Vite y Tailwind")
    print(f"  • Next.js con Tailwind")
    tech_stack = input(f"{GOLD}Stack tecnológico a utilizar [Default: HTML/CSS/JS (Vanilla con Express)]: {RESET}").strip()
    if not tech_stack:
        tech_stack = "HTML/CSS/JS (Vanilla con Express)"
        
    # 4. Solicitar/Confirmar Concepto del proyecto
    if concept:
        print(f"{GREEN}[✓] Concepto inicial: {concept}{RESET}")
        concept_choice = input(f"{GOLD}¿Deseas modificar el concepto? (s/n) [Default: n]: {RESET}").strip().lower()
        if concept_choice == "s":
            concept = input(f"{GOLD}Describe el concepto del proyecto detalladamente: {RESET}").strip()
    else:
        concept = input(f"{GOLD}Describe el concepto del proyecto detalladamente (ej: tienda de plantas online): {RESET}").strip()
        while not concept:
            print(f"{RED}[!] El concepto del proyecto es obligatorio.{RESET}")
            concept = input(f"{GOLD}Describe el concepto del proyecto: {RESET}").strip()

    project_dir = os.path.join(target_dir, project_name)
    print(f"\n{CYAN}=== Iniciando Creación de Proyecto: {BOLD}{project_name}{RESET} ===")
    print(f"{GRAY}Directorio objetivo: {project_dir}{RESET}\n")
    os.makedirs(project_dir, exist_ok=True)
    
    # Cargar UI/UX Pro Max Design System
    ds_summary = ""
    if has_ui_ux_pro_max:
        print(f"{CYAN}[🎨 Diseñador UI/UX] Cargando especificaciones de diseño de ui-ux-pro-max...{RESET}")
        try:
            generator = DesignSystemGenerator()
            ds = generator.generate(concept)
            ds_summary = f"""
            === UI/UX PRO MAX DESIGN SYSTEM ===
            Product Category: {ds.get('category')}
            Style Recommendation: {ds.get('style', {}).get('name')} ({ds.get('style', {}).get('keywords')})
            Colors HSL/Hex:
              - Primary: {ds.get('colors', {}).get('primary')}
              - Secondary: {ds.get('colors', {}).get('secondary')}
              - CTA: {ds.get('colors', {}).get('cta')}
              - Background: {ds.get('colors', {}).get('background')}
              - Text: {ds.get('colors', {}).get('text')}
            Typography: Heading = {ds.get('typography', {}).get('heading')}, Body = {ds.get('typography', {}).get('body')}
            Key Effects: {ds.get('key_effects')}
            Anti-Patterns to Avoid: {ds.get('anti_patterns')}
            """
            print(f"{GREEN}[✓] Sistema de diseño UI/UX Pro Max generado con éxito.{RESET}")
        except Exception as e:
            print(f"{GOLD}[!] No se pudo generar el sistema de diseño automático ({e}). Usando fallbacks.{RESET}")
            
    print(f"{GOLD}[🔍 Orquestador] Planificando arquitectura del proyecto con Gemini...{RESET}")
    
    planning_prompt = f"""
    Actúa como el Orquestador y Arquitecto Principal de Osiris.
    Diseña la estructura de archivos para un nuevo proyecto web completo.
    
    Información del proyecto:
    - Nombre del proyecto: {project_name}
    - Título de la página: {page_title}
    - Stack Tecnológico: {tech_stack}
    - Concepto del proyecto: {concept}
    
    Debes definir una lista de todos los archivos necesarios para hacer esta aplicación completa (creando más archivos HTML, CSS, JS, etc. según sea necesario para que no sea solo una página simple, sino un sistema fuerte, completo, bonito y cómodo).
    También define una lista de imágenes clave (banners, productos, iconos, fondos) que deben ser generadas.
    
    Retorna ÚNICAMENTE un objeto JSON válido con la siguiente estructura:
    {{
      \"files\": [
        {{
          \"path\": \"ruta/al/archivo.ext\",
          \"type\": \"style\" | \"backend\" | \"frontend\" | \"seo\" | \"qa\",
          \"description\": \"Descripción detallada del contenido que este archivo debe tener\"
        }}
      ],
      \"images\": [
        {{
          \"path\": \"assets/nombre_imagen.jpg\",
          \"prompt\": \"Prompt descriptivo detallado en inglés para generar la imagen usando el modelo Imagen 3.0\",
          \"aspect_ratio\": \"16:9\" | \"1:1\" | \"4:3\"
        }}
      ]
    }}
    
    No agregues ninguna introducción, conclusión ni markdown fuera del bloque de código.
    """
    
    plan_text = call_gemini(api_key, "Eres un arquitecto de software de élite que planifica estructuras de proyectos en JSON.", planning_prompt, "gemini-2.5-pro")
    plan = extract_json(plan_text)
    
    if not plan or "files" not in plan:
        print(f"{RED}[!] Error al generar el plan de archivos. Usando estructura por defecto.{RESET}")
        plan = {{
            "files": [
                {{"path": "index.css", "type": "style", "description": "Estilo CSS global premium"}},
                {{"path": "server.js", "type": "backend", "description": "Servidor Express con API"}},
                {{"path": "index.html", "type": "frontend", "description": "Página principal interactiva"}},
                {{"path": "robots.txt", "type": "seo", "description": "Configuración SEO robots.txt"}},
                {{"path": "test.js", "type": "qa", "description": "Pruebas de calidad unitarias"}}
            ],
            "images": [
                {{"path": "assets/hero.jpg", "prompt": f"Premium clean banner illustration for {{concept}}", "aspect_ratio": "16:9"}},
                {{"path": "assets/feature1.jpg", "prompt": f"Feature graphic representing {{concept}}", "aspect_ratio": "1:1"}}
            ]
        }}
    
    print(f"{GREEN}[✓] Estructura planificada con éxito. Archivos a crear: {{[f['path'] for f in plan['files']]}}{RESET}\n")
    
    # 2. Generación de Imágenes usando Imagen 3.0
    print(f"{CYAN}[🎨 Diseñador de Imágenes] Iniciando generación de imágenes con el modelo Imagen...{RESET}")
    headers = {{"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}}
    for img in plan.get("images", []):
        path = img.get("path")
        prompt_img = img.get("prompt")
        aspect_ratio = img.get("aspect_ratio", "16:9")
        file_path = os.path.join(project_dir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        print(f"  {CYAN}• Generando '{{path}}' ({{aspect_ratio}}) con el modelo Imagen...{RESET}")
        try:
            img_data = call_imagen_api(api_key, prompt_img, aspect_ratio)
            with open(file_path, "wb") as f:
                f.write(img_data)
            print(f"    {GREEN}[✓] Guardado {{path}} (Imagen generada exitosamente){RESET}")
        except Exception as e:
            print(f"    {GOLD}[!] Error en Imagen API ({{e}}). Usando fallback de Unsplash...{RESET}")
            kw = prompt_img.strip().replace(" ", "+")
            unsplash_url = f"https://images.unsplash.com/featured/?{{kw}}"
            try:
                req = urllib.request.Request(unsplash_url, headers=headers)
                with urllib.request.urlopen(req, timeout=12) as response:
                    with open(file_path, "wb") as f:
                        f.write(response.read())
                print(f"      {GREEN}[✓] Guardado {{path}} (Fallback Unsplash exitoso){RESET}")
            except Exception as e2:
                print(f"      {GOLD}[!] Error en fallback ({{e2}}). Se usará CSS/SVG inline en la app.{RESET}")
                
    # 3. Generación secuencial de archivos en equipo
    print(f"\n{GOLD}[💻 Equipo de Agentes] Iniciando codificación full-stack del proyecto...{RESET}")
    generated_contents = {{}}
    
    type_priority = {{"style": 0, "backend": 1, "frontend": 2, "seo": 3, "qa": 4}}
    sorted_files = sorted(plan["files"], key=lambda x: type_priority.get(x["type"], 5))
    
    for file_info in sorted_files:
        path = file_info["path"]
        ftype = file_info["type"]
        description = file_info["description"]
        file_path = os.path.join(project_dir, path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        print(f"  {CYAN}• Agente [{{ftype.upper()}}] escribiendo '{{path}}'...{RESET}")
        
        style_context = ""
        backend_context = ""
        other_files_context = f"Archivos ya planificados/creados en este proyecto: {{', '.join(generated_contents.keys())}}"
        
        for p, content in generated_contents.items():
            if p.endswith(".css"):
                style_context += f"\nEstilo ({{p}}):\n{{content[:1000]}}\n"
            elif p.endswith(".js") or p.endswith(".py"):
                backend_context += f"\nBackend ({{p}}):\n{{content[:1000]}}\n"
                
        if ftype == "style":
            prompt = f"""
            Actúa como el Diseñador UI/UX de Osiris.
            Genera el archivo de estilos '{{path}}' para el proyecto '{{project_name}}' (Título: '{{page_title}}').
            Concepto: '{{concept}}'. Stack: '{{tech_stack}}'.
            Propósito del archivo: '{{description}}'.
            
            Usa las directrices de diseño de ui-ux-pro-max:
            {{ds_summary}}
            Debe incluir:
            - Colores HSL premium y variables consistentes.
            - Tipografía moderna (Google Fonts) y escala responsiva.
            - Bento Grid o layout asimétrico moderno.
            - Transiciones fluidas, hovers animados y efectos premium (glassmorphism/gradientes).
            
            Retorna únicamente el código CSS puro, sin explicaciones ni markdown.
            """
            system_ins = "Eres un Diseñador UI/UX senior experto en CSS premium, animaciones fluidas y layouts responsivos."
            model_to_use = "gemini-2.5-flash"
            
        elif ftype == "backend":
            prompt = f"""
            Actúa como el Desarrollador Backend de Osiris.
            Genera el archivo backend '{{path}}' para el proyecto '{{project_name}}'.
            Concepto: '{{concept}}'. Stack: '{{tech_stack}}'.
            Propósito del archivo: '{{description}}'.
            {{other_files_context}}
            
            Debe seguir las directrices de arquitecto-software y desarrollador-backend:
            - Estructura limpia SOLID y Separation of Concerns (SoC).
            - Funcionalidad real completa del backend para responder a las llamadas de la app.
            - Validación de datos estricta y manejo de excepciones.
            - Si usa base de datos local (ej: SQLite), inicialízala y escribe queries completas.
            
            Retorna únicamente el código de programación backend puro, sin explicaciones ni markdown.
            """
            system_ins = "Eres un desarrollador backend senior experto en APIs seguras, base de datos y lógica de negocio sólida."
            model_to_use = "gemini-2.5-pro"
            
        elif ftype == "frontend":
            prompt = f"""
            Actúa como el Desarrollador Frontend de Osiris.
            Genera la página frontend '{{path}}' para el proyecto '{{project_name}}'.
            Concepto: '{{concept}}'. Título: '{{page_title}}'. Stack: '{{tech_stack}}'.
            Propósito del archivo: '{{description}}'.
            
            Debe seguir las directrices de frontend-developer y analista-seo:
            - HTML5 semántico (un solo <h1> por página, jerarquía correcta).
            - Estructura premium Bento Grid y responsiva.
            - Consumo dinámico de la API/Backend del proyecto.
            - Estados visuales de carga (loaders) y manejo de errores visible.
            - IDs únicos para cada botón/formulario y ARIA tags para accesibilidad.
            - Enlace correcto con otros archivos del proyecto: {{', '.join(generated_contents.keys())}}
            - Vincula estas imágenes locales generadas si corresponde:
              {{', '.join([img['path'] for img in plan.get('images', [])])}}
              
            Contexto de estilos y backend previos:
            {{style_context}}
            {{backend_context}}
            
            Retorna únicamente el código frontend completo y funcional, sin explicaciones ni markdown.
            """
            system_ins = "Eres un desarrollador frontend senior especializado en interfaces hermosas, accesibles y dinámicas."
            model_to_use = "gemini-2.5-flash"
            
        elif ftype == "seo":
            prompt = f"""
            Actúa como el Analista SEO y Copywriter de Osiris.
            Genera el archivo SEO '{{path}}' para el proyecto '{{project_name}}'.
            Concepto: '{{concept}}'. Propósito: '{{description}}'.
            
            Retorna únicamente el contenido del archivo de texto puro, sin explicaciones ni markdown.
            """
            system_ins = "Eres un consultor SEO y copywriter técnico especialista en sitemaps, marcado semántico y indexabilidad."
            model_to_use = "gemini-2.5-flash"
            
        else: # qa
            prompt = f"""
            Actúa como el Especialista QA de Osiris.
            Genera el archivo de pruebas '{{path}}' para el proyecto '{{project_name}}'.
            Concepto: '{{concept}}'. Stack: '{{tech_stack}}'.
            Propósito: '{{description}}'.
            
            Escribe pruebas unitarias o de integración simples para verificar el comportamiento de los endpoints o el frontend del proyecto.
            
            Retorna únicamente el código de prueba puro, sin explicaciones ni markdown.
            """
            system_ins = "Eres un especialista QA senior experto en automatización de pruebas, Jest, Mocha y manejo de errores."
            model_to_use = "gemini-2.5-pro"
            
        content_res = call_gemini(api_key, system_ins, prompt, model_to_use)
        content_res = clean_code_block(content_res)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content_res)
        generated_contents[path] = content_res
        print(f"    {GREEN}[✓] Escrito: {{path}}{RESET}")

    # 4. Fase de Calidad, Verificación y Refinamiento Visual
    print(f"\n{GOLD}=== Fase de Calidad, Verificación y Refinamiento Visual ==={RESET}")
    print(f"{CYAN}[🧪 QA & 🎨 Diseñador] Auditando y mejorando visualmente el código de los archivos del proyecto...{RESET}")
    
    for path, content_res in list(generated_contents.items()):
        if not (path.endswith(".html") or path.endswith(".css") or path.endswith(".js") or path.endswith(".py")):
            continue
            
        print(f"  {CYAN}• Examinando errores y optimizando diseño visual en '{{path}}'...{RESET}")
        audit_prompt = f"""
        Actúa como el Auditor de Diseño Visual y Desarrollador Senior de Osiris.
        Revisa y optimiza el siguiente código del archivo '{{path}}' del proyecto '{{project_name}}' (Stack: {{tech_stack}}):
        
        ```
        {{content_res}}
        ```
        
        Tu objetivo es:
        1. Identificar y corregir errores de código, dependencias faltantes o enlaces rotos con los otros archivos del proyecto: {{', '.join(generated_contents.keys())}}.
        2. Analizar y refinar visualmente la página: mejorar contrastes de color, centrado, Bento grids, márgenes, tipografías, hover effects, transiciones y suavidad general.
        3. Elevar el diseño para que se sienta 100% premium, cómodo, moderno y espectacular.
        
        Retorna únicamente el código FINAL corregido, completo y refinado. No añadas explicaciones ni markdown.
        """
        refined_content = call_gemini(api_key, "Eres un diseñador visual y QA de élite dedicado a perfeccionar el diseño visual y la robustez del código.", audit_prompt, "gemini-2.5-pro")
        refined_content = clean_code_block(refined_content)
        
        if refined_content and len(refined_content) > 50:
            generated_contents[path] = refined_content
            with open(os.path.join(project_dir, path), "w", encoding="utf-8") as f:
                f.write(refined_content)
            print(f"    {GREEN}[✓] '{{path}}' optimizado y mejorado con éxito.{RESET}")
        else:
            print(f"    {GRAY}[-] No se requirieron cambios en '{{path}}'.{RESET}")

    # 5. Generar README.md de instalación
    print(f"\n{CYAN}[📝 Redactor] Generando README.md de instalación...{RESET}")
    readme_prompt = f"""
    Actúa como el Redactor de Contenido y Desarrollador de Onboarding de Osiris.
    Genera un archivo 'README.md' premium para el proyecto '{{project_name}}'.
    Concepto: '{{concept}}'. Título: '{{page_title}}'. Stack: '{{tech_stack}}'.
    
    Archivos creados en el proyecto:
    {{', '.join(generated_contents.keys())}}
    
    El README debe contener:
    - Un banner visual hermoso en la parte superior.
    - Explicación del concepto del proyecto y arquitectura de componentes.
    - Requisitos previos necesarios.
    - Pasos detallados e instrucciones de instalación de dependencias específicas para el stack '{{tech_stack}}'.
    - Instrucciones paso a paso de ejecución en local.
    - Instrucciones sobre cómo ejecutar los tests.
    - Co-Authored-By: Antigravity Developer Agent <antigravity@google.com>
    
    Retorna únicamente el código Markdown puro para README.md.
    """
    readme_content = call_gemini(api_key, "Eres un redactor técnico experto que escribe documentación clara y atractiva.", readme_prompt, "gemini-2.5-flash")
    readme_content = clean_code_block(readme_content)
    
    with open(os.path.join(project_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content)
    print(f"{GREEN}[✓] Escrito: README.md{{RESET}}")
    
    print(f"\n{GREEN}[✓] ¡Proyecto Osiris '{{project_name}}' creado con éxito en: {{project_dir}}!{{RESET}}")
    print(f"{{GOLD}}Habilidades cooperando: ui-ux-pro-max, disenador, arquitecto-software, desarrollador-backend, desarrollador-frontend, analista-seo, redactor-contenido, pruebas-calidad y el modelo Imagen 3.0 para diseño gráfico.{{RESET}}")
def handle_agent_proposals(response, target_dir):
    import re
    import subprocess
    
    # 1. Parse file writes: [WRITE_FILE: path/to/file.ext] followed by a code block
    write_pattern = r'\[WRITE_FILE:\s*([^\n\]]+)\]\s*\n*```[a-zA-Z0-9#+\-_]*\n(.*?)\n*```'
    write_matches = re.findall(write_pattern, response, re.DOTALL)
    
    for file_path, file_content in write_matches:
        file_path = file_path.strip()
        full_path = os.path.join(target_dir, file_path)
        print(f"\n{GOLD}[🤖 Propuesta de Archivo] Osiris sugiere escribir en '{file_path}'.{RESET}")
        confirm = input(f"{CYAN}¿Deseas crear/modificar este archivo? (s/n) [Default: n]: {RESET}").strip().lower()
        if confirm == 's':
            try:
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(file_content.strip() + "\n")
                print(f"{GREEN}[✓] Archivo escrito con éxito en {file_path}{RESET}")
            except Exception as e:
                print(f"{RED}[!] Error al escribir el archivo: {e}{RESET}")
                
    # 2. Parse command executions: [RUN_COMMAND: command]
    cmd_pattern = r'\[RUN_COMMAND:\s*([^\n\]]+)\]'
    cmd_matches = re.findall(cmd_pattern, response)
    
    for cmd in cmd_matches:
        cmd = cmd.strip()
        print(f"\n{GOLD}[🤖 Propuesta de Comando] Osiris sugiere ejecutar: {BOLD}{cmd}{RESET}")
        confirm = input(f"{CYAN}¿Deseas ejecutar este comando? (s/n) [Default: n]: {RESET}").strip().lower()
        if confirm == 's':
            try:
                print(f"{GRAY}Ejecutando: {cmd}...{RESET}")
                res = subprocess.run(cmd, shell=True, cwd=target_dir, text=True)
                if res.returncode == 0:
                    print(f"{GREEN}[✓] Comando ejecutado con éxito (código de salida: 0).{RESET}")
                else:
                    print(f"{RED}[!] El comando falló con código de salida: {res.returncode}{RESET}")
            except Exception as e:
                print(f"{RED}[!] Error al ejecutar el comando: {e}{RESET}")

def main():
    print(LOGO)
    print(f"{GRAY}Cargando contexto del workspace...{RESET}")
    
    skills_list = get_skills_summary()
    print(f"{GREEN}[✓] {len(skills_list.split(', '))} Habilidades core mapeadas.{RESET}")
    
    # Preguntar por el directorio de trabajo del proyecto
    workspace_root = repo_root
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
    
    CAPACIDAD DE EJECUCIÓN DE AGENTE:
    Si tu respuesta requiere la creación o modificación de un archivo para el usuario, debes incluir una sección con el siguiente formato exacto:
    [WRITE_FILE: nombre_archivo.ext]
    ```idioma
    contenido del archivo
    ```
    
    Si tu respuesta requiere ejecutar un comando de terminal/consola en el sistema del usuario (como instalar paquetes, correr servidores, etc.), debes incluir el comando en el siguiente formato exacto:
    [RUN_COMMAND: comando a ejecutar]
    
    Puedes proponer múltiples acciones de tipo WRITE_FILE y RUN_COMMAND en una sola respuesta si la tarea lo requiere.
    """
    
    print(f"\n{GREEN}Osiris Online.{RESET} Directorio activo: {CYAN}{target_dir}{RESET}")
    print(f"\n{BOLD}Capacidades de Osiris:{RESET}")
    print(f"  • {CYAN}/create <nombre>{RESET} - Orquesta 6 agentes en equipo para autogenerar tu app completa.")
    print(f"  • {CYAN}/chat <pregunta>{RESET}  - Analiza tu código, depura errores y genera creativos visuales con IA.")
    print(f"  • {CYAN}/match <solicitud>{RESET} - Mapea y selecciona habilidades óptimas de tu catálogo para cualquier tarea.")
    print(f"  • {CYAN}/optimize <prompt>{RESET}- Reescribe prompts para evitar autocompletados del IDE y estructurar código.")
    print(f"\nEscribe {CYAN}/help{RESET} para ver la lista completa de comandos.")
    
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
                    
                    import subprocess
                    scan_script = os.path.join(repo_root, ".agent", "skills", "agent-orchestrator", "scripts", "scan_registry.py")
                    match_script = os.path.join(repo_root, ".agent", "skills", "agent-orchestrator", "scripts", "match_skills.py")
                    
                    print(f"{GRAY}Sincronizando registro de habilidades locales...{RESET}")
                    subprocess.run([sys.executable, scan_script], capture_output=True, text=True)
                    
                    print(f"{GRAY}Calculando relevancia y entrelazado de habilidades (Cerebro Osiris)...{RESET}")
                    res = subprocess.run([sys.executable, match_script, args], capture_output=True, text=True)
                    
                    matched_data = {}
                    if res.returncode == 0:
                        try:
                            matched_data = json.loads(res.stdout)
                        except Exception:
                            pass
                    
                    skills_matched_info = ""
                    if matched_data and "skills" in matched_data and matched_data["skills"]:
                        for s in matched_data["skills"]:
                            skills_matched_info += f"- Habilidad: {s['name']}\n  Descripción: {s['description']}\n  Capacidades: {', '.join(s['capabilities'])}\n\n"
                    else:
                        skills_matched_info = "- Ninguna habilidad local superó el umbral de relevancia directa.\n"
                    
                    prompt = f"""
                    Como el Cerebro Orquestador de Osiris, diseña un mapa cognitivo para entrelazar las habilidades y resolver la tarea: "{args}".
                    
                    Aquí están las habilidades más relevantes que he detectado localmente en mi registro para esta tarea:
                    {skills_matched_info}
                    
                    Por favor, actúa como el cerebro humano y diseña un flujo de trabajo secuencial detallado. Describe paso a paso cómo se comunican y complementan estas habilidades entre sí (p. ej., de qué forma la Habilidad A prepara los datos que la Habilidad B necesita para ejecutar la acción). Usa una estructura visual clara (p. ej., diagramas ASCII o formato de fases con emojis).
                    """
                    
                    response = call_gemini(api_key, system_instruction, prompt)
                    print(f"\n{GOLD}🧠 Mapa de Entrelazado Cognitivo (Cerebro Osiris):{RESET}\n{response}")
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
                    handle_agent_proposals(response, target_dir)
                else:
                    print(f"{RED}[!] Comando desconocido. Escribe /help para ver la lista.{RESET}")
            else:
                print(f"{GRAY}Consultando con Osiris...{RESET}")
                response = call_gemini(api_key, system_instruction, user_input)
                print(f"\n{response}")
                handle_agent_proposals(response, target_dir)
                
        except KeyboardInterrupt:
            print(f"\n{GOLD}Apagando Osiris. Hasta pronto.{RESET}")
            break
        except Exception as e:
            print(f"\n{RED}[!] Error: {e}{RESET}")

if __name__ == "__main__":
    main()

