#!/usr/bin/env python3
# Test script para verificar el escaneo de puertos

import sys
import os
sys.path.append('app')

from analyzer import escanear_puertos_nmap, analizar_dominio

def test_escaneo_directo():
    """Prueba directa de la función de escaneo"""
    print("=" * 50)
    print("🔬 TEST DIRECTO DE ESCANEO DE PUERTOS")
    print("=" * 50)
    
    # Test con diferentes tipos de URLs
    urls_test = [
        "google.com",
        "https://google.com",
        "http://google.com/path",
        "google.com:80",
        "vulqanopark.com"
    ]
    
    for url in urls_test:
        print(f"\n🎯 Probando URL: {url}")
        resultado = escanear_puertos_nmap(url)
        print(f"📊 Resultado: {resultado}")

def test_analisis_con_opciones():
    """Prueba el análisis completo con opciones controladas"""
    print("\n" + "=" * 50)
    print("🔬 TEST DE ANÁLISIS CON OPCIONES")
    print("=" * 50)
    
    # Test con puertos habilitados
    print("\n🟢 TEST 1: Con escaneo de puertos HABILITADO")
    opciones_con_puertos = {
        'subdominios': False,  # Deshabilitar para acelerar test
        'tecnologias': False, 
        'puertos': True,      # ✅ HABILITADO
        'tls': False,
        'cves': False
    }
    
    # Test con puertos deshabilitados  
    print("\n🔴 TEST 2: Con escaneo de puertos DESHABILITADO")
    opciones_sin_puertos = {
        'subdominios': False,  # Deshabilitar para acelerar test
        'tecnologias': False,
        'puertos': False,     # ❌ DESHABILITADO
        'tls': False,
        'cves': False
    }
    
    dominio_test = "google.com"
    
    print(f"\nAnalizando {dominio_test} con opciones limitadas...")
    
    try:
        print("\n--- Con puertos habilitados ---")
        resultado1 = analizar_dominio(dominio_test, opciones_con_puertos)
        
        print("\n--- Con puertos deshabilitados ---") 
        resultado2 = analizar_dominio(dominio_test, opciones_sin_puertos)
        
        print(f"\n✅ Ambas pruebas completadas")
        
    except Exception as e:
        print(f"❌ Error en el test: {e}")

if __name__ == "__main__":
    print("🚀 Iniciando tests del sistema de escaneo de puertos")
    
    # Test 1: Escaneo directo
    test_escaneo_directo()
    
    # Test 2: Análisis con opciones
    test_analisis_con_opciones()
    
    print("\n🏁 Tests completados")
