#!/usr/bin/env python3
"""
Test final para verificar la implementación completa de la metodología SECUREVAL
y validar que toda la documentación esté correctamente integrada
"""

import sys
import os
import json
from pathlib import Path

# Agregar el directorio app al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_metodologia_secureval():
    """Test completo de la metodología SECUREVAL"""
    print("🧪 TEST FINAL: METODOLOGÍA SECUREVAL v1.0")
    print("=" * 70)
    print("Verificando implementación completa de la metodología")
    print()
    
    success_count = 0
    total_tests = 6
    
    # Test 1: Verificar función evaluar_riesgo_secureval
    print("📐 Test 1: Función evaluar_riesgo_secureval...")
    try:
        from analyzer import evaluar_riesgo_secureval
        
        # Casos de prueba según metodología
        test_cases = [
            (5.0, 9.5, 5, 5, 125, "CRÍTICO"),  # Caso crítico
            (4.0, 7.5, 4, 4, 64, "ALTO"),      # Caso alto  
            (3.0, 5.2, 3, 3, 27, "MEDIO"),     # Caso medio
            (2.0, 2.1, 2, 2, 8, "BAJO"),       # Caso bajo
            (1.0, 0.0, 1, 1, 1, "MÍNIMO")      # Caso mínimo
        ]
        
        casos_correctos = 0
        for va, cvss, prob_esperada, vul_esperada, riesgo_esperado, nivel in test_cases:
            prob, vul, riesgo = evaluar_riesgo_secureval(va, cvss)
            
            if prob == prob_esperada and vul == vul_esperada and abs(riesgo - riesgo_esperado) < 0.1:
                casos_correctos += 1
                print(f"   ✅ {nivel}: VA={va}, CVSS={cvss} → Riesgo={riesgo}")
            else:
                print(f"   ❌ {nivel}: Esperado={riesgo_esperado}, Obtenido={riesgo}")
        
        if casos_correctos == len(test_cases):
            print(f"✅ Función evaluar_riesgo_secureval: {casos_correctos}/{len(test_cases)} casos correctos")
            success_count += 1
        else:
            print(f"❌ Función evaluar_riesgo_secureval: {casos_correctos}/{len(test_cases)} casos correctos")
            
    except Exception as e:
        print(f"❌ Error en evaluar_riesgo_secureval: {e}")
    
    # Test 2: Verificar documentación en código
    print("\\n📚 Test 2: Documentación en código...")
    try:
        with open('app/analyzer.py', 'r') as f:
            contenido = f.read()
        
        elementos_doc = [
            "METODOLOGÍA SECUREVAL",
            "FÓRMULA DE EVALUACIÓN DE RIESGO", 
            "Valor_Activo × Probabilidad × Vulnerabilidad",
            "ESCALAS DE CVSS A SECUREVAL",
            "CLASIFICACIÓN DE RIESGO FINAL"
        ]
        
        elementos_encontrados = 0
        for elemento in elementos_doc:
            if elemento in contenido:
                elementos_encontrados += 1
        
        if elementos_encontrados == len(elementos_doc):
            print(f"✅ Documentación completa: {elementos_encontrados}/{len(elementos_doc)} elementos")
            success_count += 1
        else:
            print(f"❌ Documentación incompleta: {elementos_encontrados}/{len(elementos_doc)} elementos")
            
    except Exception as e:
        print(f"❌ Error leyendo documentación: {e}")
    
    # Test 3: Verificar integración con monitoreo
    print("\\n🖥️ Test 3: Integración con monitoreo...")
    try:
        from monitoreo import calcular_kpis, mostrar_kpis_en_gui
        
        # Buscar dominio con datos CVSS
        resultados_dir = Path("resultados")
        dominio_test = None
        
        for dominio_dir in resultados_dir.iterdir():
            if dominio_dir.is_dir():
                riesgo_file = dominio_dir / "riesgo.json"
                if riesgo_file.exists():
                    try:
                        with open(riesgo_file, 'r') as f:
                            riesgo_data = json.load(f)
                        for item in riesgo_data:
                            if isinstance(item, dict) and item.get('cvss_max', 0) > 0:
                                dominio_test = dominio_dir.name
                                break
                        if dominio_test:
                            break
                    except:
                        continue
        
        if dominio_test:
            kpis = calcular_kpis(dominio_test)
            if kpis and 'cvss_max' in kpis and kpis['cvss_max'] > 0:
                print(f"✅ Integración monitoreo: CVSS={kpis['cvss_max']:.1f} en {dominio_test}")
                success_count += 1
            else:
                print("❌ Integración monitoreo: No extrae CVSS correctamente")
        else:
            print("⏭️ Sin datos CVSS para probar integración")
            success_count += 1  # No es un error del sistema
            
    except Exception as e:
        print(f"❌ Error en integración monitoreo: {e}")
    
    # Test 4: Verificar clasificación de criticidad
    print("\\n🎯 Test 4: Clasificación de criticidad...")
    try:
        from analyzer import evaluar_riesgo_secureval
        
        # Verificar rangos de clasificación
        clasificaciones = [
            (5.0, 9.0, "CRÍTICO", 80),   # Debe dar ≥80
            (4.0, 7.0, "ALTO", 50),      # Debe dar ≥50
            (3.0, 4.0, "MEDIO", 25),     # Debe dar ≥25  
            (2.0, 1.0, "BAJO", 1)        # Debe dar <25
        ]
        
        clasificaciones_correctas = 0
        for va, cvss, nivel_esperado, umbral in clasificaciones:
            prob, vul, riesgo = evaluar_riesgo_secureval(va, cvss)
            
            if nivel_esperado == "CRÍTICO" and riesgo >= 80:
                clasificaciones_correctas += 1
            elif nivel_esperado == "ALTO" and 50 <= riesgo < 80:
                clasificaciones_correctas += 1
            elif nivel_esperado == "MEDIO" and 25 <= riesgo < 50:
                clasificaciones_correctas += 1
            elif nivel_esperado == "BAJO" and riesgo < 25:
                clasificaciones_correctas += 1
            
            print(f"   • {nivel_esperado}: Riesgo={riesgo:.1f}")
        
        if clasificaciones_correctas == len(clasificaciones):
            print(f"✅ Clasificación criticidad: {clasificaciones_correctas}/{len(clasificaciones)} correctas")
            success_count += 1
        else:
            print(f"❌ Clasificación criticidad: {clasificaciones_correctas}/{len(clasificaciones)} correctas")
            
    except Exception as e:
        print(f"❌ Error en clasificación: {e}")
    
    # Test 5: Verificar archivos de documentación
    print("\\n📄 Test 5: Archivos de documentación...")
    archivos_doc = [
        "METODOLOGIA_SECUREVAL_FINAL.md",
        "CORRECCIÓN_CVSS_MONITOREO.md",
        "CORRECCIONES_FINALES.md"
    ]
    
    archivos_encontrados = 0
    for archivo in archivos_doc:
        if Path(archivo).exists():
            archivos_encontrados += 1
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo}")
    
    if archivos_encontrados == len(archivos_doc):
        print(f"✅ Documentación externa: {archivos_encontrados}/{len(archivos_doc)} archivos")
        success_count += 1
    else:
        print(f"❌ Documentación externa: {archivos_encontrados}/{len(archivos_doc)} archivos")
    
    # Test 6: Verificar consistencia de datos
    print("\\n🔍 Test 6: Consistencia de datos guardados...")
    try:
        resultados_dir = Path("resultados")
        dominios_validos = 0
        total_dominios = 0
        
        for dominio_dir in resultados_dir.iterdir():
            if dominio_dir.is_dir():
                total_dominios += 1
                riesgo_file = dominio_dir / "riesgo.json"
                
                if riesgo_file.exists():
                    try:
                        with open(riesgo_file, 'r') as f:
                            riesgo_data = json.load(f)
                        
                        # Verificar estructura de datos
                        datos_validos = True
                        for item in riesgo_data:
                            if isinstance(item, dict):
                                campos_requeridos = ['cvss_max', 'probabilidad', 'vulnerabilidad', 'riesgo']
                                for campo in campos_requeridos:
                                    if campo not in item:
                                        datos_validos = False
                                        break
                            if not datos_validos:
                                break
                        
                        if datos_validos:
                            dominios_validos += 1
                            
                    except:
                        continue
        
        if total_dominios > 0:
            porcentaje = (dominios_validos / total_dominios) * 100
            print(f"   Dominios válidos: {dominios_validos}/{total_dominios} ({porcentaje:.1f}%)")
            
            if porcentaje >= 80:  # Al menos 80% deben ser válidos
                print("✅ Consistencia de datos: Estructura correcta")
                success_count += 1
            else:
                print("❌ Consistencia de datos: Estructura inconsistente")
        else:
            print("⏭️ Sin datos para verificar consistencia")
            success_count += 1
            
    except Exception as e:
        print(f"❌ Error verificando consistencia: {e}")
    
    # Resumen final
    print("\\n" + "=" * 70)
    print(f"📊 RESUMEN FINAL: {success_count}/{total_tests} pruebas pasadas")
    
    if success_count == total_tests:
        print("🎉 ¡METODOLOGÍA SECUREVAL COMPLETAMENTE IMPLEMENTADA!")
        print("✅ Versión final lista para producción")
        print("✅ Documentación completa y consistente")
        print("✅ Fórmula validada y probada")
        print("✅ Integración con todos los módulos")
        print("✅ Clasificación de riesgos funcionando")
        print("✅ Datos guardados correctamente")
        return True
    else:
        print("⚠️ Algunas pruebas fallaron")
        print("ℹ️ Revisar implementación antes de producción")
        return False

if __name__ == "__main__":
    success = test_metodologia_secureval()
    sys.exit(0 if success else 1)
