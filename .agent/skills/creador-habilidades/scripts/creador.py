#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import re

def clean_slug(name):
    # Convert to lowercase, replace spaces and special characters with hyphens
    name = name.lower()
    name = re.sub(r'[^a-z0-9\-_]', '-', name)
    name = re.sub(r'-+', '-', name)
    return name.strip('-')

def create_skill(args):
    name = clean_slug(args.nombre)
    description = args.descripcion.strip()
    title = args.titulo.strip() if args.titulo else name.replace('-', ' ').title()
    cuando = args.cuando.strip() if args.cuando else "Describe cuándo se debe utilizar esta habilidad."
    como = args.como.strip() if args.como else "Instrucciones paso a paso sobre cómo utilizar esta habilidad."

    if args.is_global:
        # Global path: ~/.gemini/antigravity/skills/<name>
        home_dir = os.path.expanduser('~')
        target_dir = os.path.join(home_dir, '.gemini', 'antigravity', 'skills', name)
    else:
        # Workspace path: .agents/skills/<name>
        # Let's find workspace root or default to current working directory
        cwd = os.getcwd()
        # We look for .agents or .agent directory to verify
        target_dir = os.path.join(cwd, '.agents', 'skills', name)

    print(f"Creando habilidad '{name}' en: {target_dir}")

    # Create directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    skill_md_path = os.path.join(target_dir, 'SKILL.md')
    
    content = f"""---
name: {name}
description: {description}
---

# {title}

## Cuándo usar esta habilidad

{cuando}

## Cómo usarla

{como}
"""

    with open(skill_md_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"¡Habilidad creada con éxito!")
    print(f"Archivo: {skill_md_path}")
    print("\nContenido generado:")
    print("-" * 40)
    print(content)
    print("-" * 40)

def main():
    parser = argparse.ArgumentParser(description="Creador de habilidades de Antigravity en Español")
    parser.add_argument('-n', '--nombre', help="Nombre de la habilidad (ej. validador-codigo)")
    parser.add_argument('-d', '--descripcion', help="Descripción breve para el frontmatter")
    parser.add_argument('-t', '--titulo', help="Título de la habilidad en el documento")
    parser.add_argument('-c', '--cuando', help="Sección: Cuándo usar esta habilidad")
    parser.add_argument('-m', '--como', help="Sección: Cómo usarla")
    parser.add_argument('-g', '--global', dest='is_global', action='store_true', help="Crear la habilidad de forma global en ~/.gemini/antigravity/skills/")

    args = parser.parse_args()

    # Interactive mode if arguments are missing
    if not args.nombre or not args.descripcion:
        print("=== Creador Interactivo de Habilidades Antigravity ===")
        if not args.nombre:
            args.nombre = input("Nombre de la habilidad (slug, ej. mi-habilidad): ").strip()
            while not args.nombre:
                args.nombre = input("El nombre es requerido. Ingrese el nombre: ").strip()
        
        if not args.descripcion:
            args.descripcion = input("Descripción breve (aparece en la selección del agente): ").strip()
            while not args.descripcion:
                args.descripcion = input("La descripción es requerida. Ingrese la descripción: ").strip()

        if not args.titulo:
            args.titulo = input(f"Título de la habilidad [por defecto: {args.nombre.replace('-', ' ').title()}]: ").strip()

        if not args.cuando:
            print("Ingrese cuándo usar esta habilidad (Presione Enter en línea vacía para terminar):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            args.cuando = "\n".join(lines)

        if not args.como:
            print("Ingrese cómo usar esta habilidad (pasos/instrucciones, Enter en línea vacía para terminar):")
            lines = []
            while True:
                line = input()
                if line == "":
                    break
                lines.append(line)
            args.como = "\n".join(lines)

    create_skill(args)

if __name__ == '__main__':
    main()
