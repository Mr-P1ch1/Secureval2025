#!/usr/bin/env python3
# secureval.py - Punto de entrada principal para SECUREVAL
"""
SECUREVAL - Sistema de Evaluación de Seguridad
Punto de entrada principal para el sistema.

Uso:
    python3 secureval.py
    o
    python3 -m secureval

Autor: SECUREVAL Team
"""

import sys
import os

# Agregar la carpeta del proyecto al path para las importaciones
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Importar y ejecutar la aplicación principal
if __name__ == "__main__":
    try:
        from app.main import main
        main()
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("🔧 Asegúrese de que todos los módulos estén en la carpeta 'app/'")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        sys.exit(1)
