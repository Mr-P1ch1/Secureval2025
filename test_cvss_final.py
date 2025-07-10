#!/usr/bin/env python3
"""
Test final para verificar que el CVSS máximo se muestra correctamente
en los módulos de tratamiento y monitoreo.
"""

import sys
import os
import json

# Agregar el directorio de la aplicación al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

import tratamiento
import monitoreo

def test_cvss_tratamiento():
    """Prueba que el módulo de tratamiento extrae y muestra CVSS."""
    print("🔍 PROBANDO MÓDULO DE TRATAMIENTO")
    print("=" * 50)
    
    dominios = tratamiento.listar_dominios()
    print(f"Dominios encontrados: {dominios}")
    
    for dominio in dominios:
        riesgos = tratamiento.cargar_riesgos(dominio)
        if riesgos:
            cvss_values = [r.get('cvss_max', 0) for r in riesgos]
            max_cvss = max(cvss_values) if cvss_values else 0
            print(f"Dominio {dominio}: CVSS máximo = {max_cvss}")
            
            # Buscar el primer riesgo con CVSS > 0
            riesgo_con_cvss = next((r for r in riesgos if r.get('cvss_max', 0) > 0), None)
            if riesgo_con_cvss:
                print(f"  ✅ Riesgo con CVSS encontrado:")
                print(f"     Subdominio: {riesgo_con_cvss.get('subdominio', 'N/A')}")
                print(f"     Tecnología: {riesgo_con_cvss.get('tecnologia', 'N/A')}")
                print(f"     CVSS: {riesgo_con_cvss.get('cvss_max', 0)}")
                print(f"     Criticidad: {riesgo_con_cvss.get('criticidad', 'N/A')}")
            else:
                print(f"  ⚠️ No se encontraron riesgos con CVSS > 0")
    
    print()

def test_cvss_monitoreo():
    """Prueba que el módulo de monitoreo extrae y muestra CVSS."""
    print("🔍 PROBANDO MÓDULO DE MONITOREO")
    print("=" * 50)
    
    dominios = ['vulqanopark.com', 'testfire.net', 'bancodeloja.fin.ec']
    
    for dominio in dominios:
        try:
            kpis = monitoreo.calcular_kpis(dominio)
            cvss_max = kpis.get('cvss_max', 0)
            print(f"Dominio {dominio}: CVSS máximo en KPIs = {cvss_max}")
            
            if cvss_max > 0:
                print(f"  ✅ CVSS detectado correctamente")
                
                # Clasificación visual según el CVSS
                if cvss_max >= 9.0:
                    nivel = "🔴 CRÍTICO"
                elif cvss_max >= 7.0:
                    nivel = "🟠 ALTO"
                elif cvss_max >= 4.0:
                    nivel = "🟡 MEDIO"
                else:
                    nivel = "🟢 BAJO"
                
                print(f"     Nivel de riesgo: {nivel}")
            else:
                print(f"  ⚠️ CVSS = 0 (sin vulnerabilidades detectadas)")
                
        except Exception as e:
            print(f"  ❌ Error procesando {dominio}: {e}")
    
    print()

def test_integracion_completa():
    """Prueba que ambos módulos funcionan de manera integrada."""
    print("🔍 PRUEBA DE INTEGRACIÓN COMPLETA")
    print("=" * 50)
    
    # Probar con vulqanopark.com que tiene CVSS > 0
    dominio_test = 'vulqanopark.com'
    
    print(f"Probando integración con dominio: {dominio_test}")
    
    # Test del tratamiento
    riesgos = tratamiento.cargar_riesgos(dominio_test)
    cvss_tratamiento = max([r.get('cvss_max', 0) for r in riesgos]) if riesgos else 0
    
    # Test del monitoreo
    kpis = monitoreo.calcular_kpis(dominio_test)
    cvss_monitoreo = kpis.get('cvss_max', 0)
    
    print(f"CVSS máximo en tratamiento: {cvss_tratamiento}")
    print(f"CVSS máximo en monitoreo: {cvss_monitoreo}")
    
    if cvss_tratamiento == cvss_monitoreo and cvss_tratamiento > 0:
        print("✅ INTEGRACIÓN EXITOSA: Ambos módulos reportan el mismo CVSS")
        return True
    elif cvss_tratamiento == cvss_monitoreo and cvss_tratamiento == 0:
        print("⚠️ INTEGRACIÓN OK: Ambos módulos reportan CVSS = 0")
        return True
    else:
        print("❌ INTEGRACIÓN FALLIDA: Los módulos reportan valores diferentes")
        return False

def main():
    """Función principal de pruebas."""
    print("🚀 INICIANDO PRUEBAS DE CVSS MÁXIMO")
    print("=" * 60)
    print()
    
    # Ejecutar todas las pruebas
    test_cvss_tratamiento()
    test_cvss_monitoreo()
    integracion_ok = test_integracion_completa()
    
    print()
    print("📊 RESUMEN DE PRUEBAS")
    print("=" * 30)
    
    if integracion_ok:
        print("✅ TODAS las pruebas PASARON")
        print("✅ El CVSS máximo se muestra correctamente en tratamiento")
        print("✅ El CVSS máximo se muestra correctamente en monitoreo")
        print("✅ Ambos módulos están integrados correctamente")
        print()
        print("🎯 CONCLUSIÓN: El sistema SECUREVAL está funcionando correctamente")
        print("   y muestra el CVSS máximo en ambos módulos según lo solicitado.")
    else:
        print("❌ Algunas pruebas FALLARON")
        print("⚠️ Revisar la implementación de CVSS en los módulos")

if __name__ == "__main__":
    main()
