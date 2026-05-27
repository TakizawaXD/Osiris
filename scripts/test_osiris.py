#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

# Agregar la raíz del repositorio al path para poder importar scripts
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    import scripts.osiris_cli as osiris
    print("[✓] Importación de osiris_cli.py exitosa.")
except Exception as e:
    print(f"[X] Fallo al importar osiris_cli.py: {e}")
    sys.exit(1)

def run_tests():
    print("\n--- Iniciando Pruebas de Calidad (Osiris QA) ---")
    
    # Test 1: Verificar existencia de variables de color
    try:
        assert hasattr(osiris, 'CYAN')
        assert hasattr(osiris, 'GOLD')
        assert hasattr(osiris, 'RESET')
        print("[✓] Test 1: Configuración de colores ANSI y constantes de diseño listos.")
    except AssertionError:
        print("[X] Test 1: Faltan constantes de colores ANSI.")
        return False
        
    # Test 2: Mapeo de Habilidades
    try:
        skills = osiris.get_skills_summary()
        assert len(skills) > 0
        print(f"[✓] Test 2: Mapeo de habilidades core exitoso ({len(skills.split(', '))} detectadas).")
    except Exception as e:
        print(f"[X] Test 2: Error al mapear habilidades: {e}")
        return False

    # Test 3: Verificar Clave de API de Gemini
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("[!] Test 3: Advertencia - GEMINI_API_KEY no configurada en las variables de entorno.")
        print("    (El test de conectividad con Gemini se omitirá).")
    else:
        print("[✓] Test 3: GEMINI_API_KEY detectada en el entorno.")
        # Test 4: Conectividad con la API de Gemini
        try:
            print("[...] Test 4: Probando conectividad con Gemini API...")
            system_instruction = "Eres un asistente de pruebas breves."
            response = osiris.call_gemini(api_key, system_instruction, "Dile 'Ok' al usuario.")
            if "Error" in response or "HTTP Error" in response:
                print(f"[X] Test 4: Fallo en conexión a la API: {response}")
                return False
            else:
                print(f"[✓] Test 4: Conectividad y respuesta de Gemini verificada: '{response.strip()}'")
        except Exception as e:
            print(f"[X] Test 4: Error durante la llamada de prueba: {e}")
            return False

    print("\n[✓] ¡Todos los tests locales pasaron exitosamente! El sistema está listo para operar.")
    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
