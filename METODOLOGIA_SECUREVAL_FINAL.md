# SECUREVAL v1.0 - DOCUMENTACIÓN FINAL
# ====================================

## METODOLOGÍA SECUREVAL PARA EVALUACIÓN DE RIESGOS

### FÓRMULA PRINCIPAL
```
Riesgo = Valor_Activo × Probabilidad × Vulnerabilidad
```

### UBICACIÓN EN CÓDIGO
- **Archivo**: `/home/kali/Documents/Secureval/app/analyzer.py`
- **Función**: `evaluar_riesgo_secureval(va, cvss)`
- **Líneas**: 154-201

### COMPONENTES DE LA FÓRMULA

#### 1. Valor del Activo (va)
- **Rango**: 1.0 - 5.0
- **Fuente**: Definido por el usuario en el módulo de activos
- **Significado**: Importancia del activo para la organización

#### 2. Probabilidad (prob)
- **Rango**: 1 - 5
- **Fuente**: Calculado automáticamente basado en CVSS
- **Significado**: Probabilidad de que la vulnerabilidad sea explotada

#### 3. Vulnerabilidad (vul)
- **Rango**: 1 - 5  
- **Fuente**: Calculado automáticamente basado en CVSS
- **Significado**: Nivel de vulnerabilidad del sistema

### MAPEO CVSS A ESCALAS SECUREVAL

| CVSS Range | Nivel | Probabilidad | Vulnerabilidad | Descripción |
|------------|-------|--------------|----------------|-------------|
| 9.0 - 10.0 | 5 | 5 | 5 | **Crítico** - Vulnerabilidades extremas |
| 7.0 - 8.9  | 4 | 4 | 4 | **Alto** - Vulnerabilidades severas |
| 4.0 - 6.9  | 3 | 3 | 3 | **Medio** - Vulnerabilidades moderadas |
| 0.1 - 3.9  | 2 | 2 | 2 | **Bajo** - Vulnerabilidades menores |
| 0.0        | 1 | 1 | 1 | **Mínimo** - Sin vulnerabilidades |

### CLASIFICACIÓN DE RIESGO FINAL

| Riesgo Calculado | Nivel | Color | Acción Recomendada |
|------------------|-------|-------|-------------------|
| 80 - 125 | 🔴 **CRÍTICO** | Rojo | Acción inmediata requerida |
| 50 - 79  | 🟠 **ALTO** | Naranja | Revisar y mitigar urgente |
| 25 - 49  | 🟡 **MEDIO** | Amarillo | Monitoreo continuo |
| 1 - 24   | 🟢 **BAJO** | Verde | Mantener buenas prácticas |

### EJEMPLOS DE CÁLCULO

#### Ejemplo 1: Riesgo Crítico
- **Valor_Activo**: 5.0 (Servidor crítico)
- **CVSS**: 9.2 (Vulnerabilidad crítica)
- **Probabilidad**: 5 (Crítico)
- **Vulnerabilidad**: 5 (Crítico)
- **Riesgo**: 5.0 × 5 × 5 = **125** (🔴 CRÍTICO)

#### Ejemplo 2: Riesgo Alto  
- **Valor_Activo**: 4.0 (Servidor importante)
- **CVSS**: 7.5 (Vulnerabilidad alta)
- **Probabilidad**: 4 (Alto)
- **Vulnerabilidad**: 4 (Alto)
- **Riesgo**: 4.0 × 4 × 4 = **64** (🟠 ALTO)

#### Ejemplo 3: Riesgo Medio
- **Valor_Activo**: 3.0 (Servidor normal)
- **CVSS**: 5.2 (Vulnerabilidad media)
- **Probabilidad**: 3 (Medio)
- **Vulnerabilidad**: 3 (Medio)
- **Riesgo**: 3.0 × 3 × 3 = **27** (🟡 MEDIO)

#### Ejemplo 4: Riesgo Bajo
- **Valor_Activo**: 2.0 (Servidor secundario)
- **CVSS**: 2.1 (Vulnerabilidad baja)
- **Probabilidad**: 2 (Bajo)
- **Vulnerabilidad**: 2 (Bajo)
- **Riesgo**: 2.0 × 2 × 2 = **8** (🟢 BAJO)

### INTEGRACIÓN EN SECUREVAL

#### Módulos que Utilizan la Metodología:

1. **analyzer.py**: Calcula riesgos durante el análisis
2. **monitoreo.py**: Muestra riesgos en dashboard y KPIs
3. **export_pdf.py**: Incluye riesgos en reportes PDF
4. **tratamiento.py**: Analiza riesgos para tratamiento

#### Flujo de Procesamiento:

1. **Detección**: Se identifica una tecnología en un subdominio
2. **CVE Lookup**: Se buscan vulnerabilidades en base NIST NVD
3. **CVSS Extracción**: Se extrae el puntaje CVSS más alto
4. **Valor Activo**: Se obtiene del módulo de activos
5. **Cálculo**: Se aplica la fórmula SECUREVAL
6. **Clasificación**: Se asigna nivel de criticidad
7. **Almacenamiento**: Se guarda en riesgo.json
8. **Visualización**: Se muestra en monitoreo y reportes

### VENTAJAS DE LA METODOLOGÍA SECUREVAL

✅ **Estandarizada**: Basada en CVSS reconocido mundialmente
✅ **Contextual**: Considera el valor específico del activo
✅ **Escalable**: Funciona para cualquier tipo de organización
✅ **Automatizada**: Cálculo automático sin intervención manual
✅ **Trazable**: Cada componente está documentado y justificado
✅ **Flexible**: Permite ajustar valores de activos según necesidades
✅ **Integrada**: Compatible con herramientas estándar de seguridad

### VALIDACIÓN Y TESTING

La metodología ha sido probada y validada con:

- ✅ **Dominios reales**: bancodeloja.fin.ec, vulqanopark.com, marfishecuador.com
- ✅ **CVEs reales**: Integración con base NIST NVD
- ✅ **Diferentes niveles**: Crítico (7.5), Alto (6.1), Medio (5.3)
- ✅ **Casos extremos**: Sin vulnerabilidades (0.0) y críticas (9.0+)
- ✅ **Monitoreo**: Visualización correcta en dashboard
- ✅ **Reportes**: Exportación correcta en PDF

### MANTENIMIENTO

Para mantener la precisión de la metodología:

1. **Actualizar CVE Database**: Mantener conexión con NIST NVD
2. **Revisar Valores de Activos**: Actualizar según cambios organizacionales
3. **Validar Escalas**: Revisar clasificaciones periódicamente
4. **Monitorear Resultados**: Verificar coherencia de resultados
5. **Feedback de Usuarios**: Incorporar experiencias del equipo de seguridad

---

**SECUREVAL v1.0** - Sistema completo de evaluación de riesgos de seguridad
Desarrollado con metodología propia validada y probada en entornos reales.
