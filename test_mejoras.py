#!/usr/bin/env python3
# Test mejorado del analyzer con las nuevas funciones

import sys
import os
sys.path.append('app')

from analyzer import escanear_puertos_nmap

def test_mejoras_escaneo():
    """Prueba las mejoras en el escaneo de puertos"""
    print("🔬 TESTING MEJORAS DEL ANALYZER")
    print("=" * 50)
    
    # Test casos que deberían funcionar
    hosts_test = [
        "google.com",        # Debería tener puertos
        "github.com",        # Debería tener puertos  
        "noestadominio.fake", # DNS no debería resolver
        "vulqanopark.com"    # Dependiendo de configuración
    ]
    
    for host in hosts_test:
        print(f"\n🎯 Probando: {host}")
        resultado = escanear_puertos_nmap(host)
        print(f"📊 Resultado ({len(resultado)} elementos):")
        for i, r in enumerate(resultado[:3], 1):  # Solo mostrar primeros 3
            print(f"   {i}. {r}")
        if len(resultado) > 3:
            print(f"   ... y {len(resultado)-3} más")

if __name__ == "__main__":
    test_mejoras_escaneo()
    print("\n🏁 Test completado")
