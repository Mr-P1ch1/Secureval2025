# SECUREVAL - Sistema de Evaluación de Seguridad

![SECUREVAL](https://img.shields.io/badge/SECUREVAL-v2.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.7+-green.svg)
![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)

## 🎯 Descripción

SECUREVAL es un sistema profesional de evaluación de seguridad diseñado para realizar análisis completos de vulnerabilidades, gestión de activos y generación de reportes. Ofrece una interfaz gráfica moderna con herramientas integradas para el análisis de seguridad.

## ✨ Características Principales

- 🔍 **Análisis de Vulnerabilidades**: Escaneo completo de puertos y servicios
- 🏢 **Gestión de Activos**: Registro completo de información organizacional
- 📊 **Monitor de Actividad**: Seguimiento en tiempo real del sistema
- 🖥️ **Consola Integrada**: Salida de logs y comandos en tiempo real
- 📄 **Exportación PDF**: Generación de reportes profesionales
- 🌐 **Detección de Tecnologías**: Identificación de frameworks y servicios web
- 🎨 **Interfaz Moderna**: GUI intuitiva y profesional

## 🚀 Instalación Rápida

### Opción 1: Instalación Automática (Recomendada)
```bash
./instalar.sh
```

### Opción 2: Instalación Manual

#### Dependencias del Sistema
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-tk nmap whatweb

# CentOS/RHEL
sudo yum install python3 python3-pip python3-tkinter nmap

# macOS (con Homebrew)
brew install python3 nmap
```

#### Dependencias Python
```bash
pip3 install -r requirements.txt
```

## 🎮 Uso

### Inicio Rápido
```bash
./iniciar.sh
```

### Opciones Disponibles
1. **Iniciar SECUREVAL** - Lanza la interfaz gráfica principal
2. **Test Rápido** - Ejecuta pruebas de integridad del sistema
3. **Información** - Muestra detalles del sistema
4. **Instalar Dependencias** - Instala paquetes Python adicionales

## 📁 Estructura del Proyecto

```
Secureval/
├── app/                    # Módulos principales
│   ├── main.py            # Interfaz principal
│   ├── activos.py         # Gestión de activos
│   ├── analyzer.py        # Motor de análisis
│   ├── tratamiento.py     # Análisis de riesgos
│   ├── export_pdf.py      # Exportación de reportes
│   └── monitoreo.py       # Monitor del sistema
├── resultados/            # Análisis y reportes generados
├── test_*.py              # Pruebas del sistema
├── iniciar.sh             # Script de inicio
├── instalar.sh            # Script de instalación
└── requirements.txt       # Dependencias Python
```

## 🔧 Módulos del Sistema

### 🏢 Gestión de Activos
- Registro completo de información organizacional
- Almacenamiento en formato JSON
- Interfaz de formulario intuitiva

### 🔍 Analyzer (Motor de Análisis)
- Escaneo de puertos con nmap
- Detección de tecnologías web
- Análisis de subdominios
- Guardado por dominio con metadatos

### 📊 Tratamiento de Riesgos
- Análisis textual de vulnerabilidades
- Evaluación de criticidad
- Recomendaciones de mitigación

### 📄 Exportación PDF
- Reportes profesionales
- Selector de dominio con combobox
- Vista previa de metadatos
- Formato empresarial

### 🖥️ Monitor de Actividad
- Pestañas de sistema, análisis y estadísticas
- Barras de progreso en tiempo real
- Lista de análisis ejecutados
- Compatible con/sin psutil

## 🧪 Pruebas del Sistema

### Test Rápido
```bash
python3 test_rapido.py
```

### Test Completo
```bash
python3 test_sistema_final.py
```

### Pruebas Incluidas
- ✅ Verificación de estructura de archivos
- ✅ Importación de módulos
- ✅ Funcionalidad de guardado/carga
- ✅ Dependencias del sistema
- ✅ Herramientas externas
- ✅ Integridad de datos

## 📋 Requisitos

### Sistema Operativo
- Linux (Ubuntu 18.04+, Debian 10+, CentOS 7+)
- Windows 10+ (con WSL recomendado)
- macOS 10.14+

### Python
- Python 3.7 o superior
- tkinter (incluido en la mayoría de instalaciones)

### Herramientas Externas (Opcionales)
- `nmap` - Para escaneo de puertos avanzado
- `whatweb` - Para detección de tecnologías web

## 🎨 Capturas de Pantalla

### Interfaz Principal
- Botonera organizada en grid 3x3
- Consola de salida integrada
- Monitor de actividad con pestañas

### Gestión de Activos
- Formulario completo de información
- Validación de campos
- Almacenamiento automático

### Análisis de Seguridad
- Escaneo de puertos en tiempo real
- Detección de servicios y versiones
- Análisis de tecnologías web

## 🛠️ Desarrollo

### Arquitectura
- **Interfaz**: Tkinter con diseño moderno
- **Backend**: Python puro con threading
- **Almacenamiento**: Archivos JSON estructurados
- **Integración**: Herramientas de línea de comandos

### Contribuir
1. Fork del repositorio
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## 📞 Soporte

### Problemas Comunes

#### Error: "tkinter not found"
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# CentOS/RHEL
sudo yum install python3-tkinter
```

#### Error: "nmap not found"
```bash
sudo apt install nmap  # Ubuntu/Debian
sudo yum install nmap  # CentOS/RHEL
```

#### Permisos de ejecución
```bash
chmod +x iniciar.sh
chmod +x instalar.sh
```

### Logs y Debugging
- Los logs se muestran en la consola integrada
- Archivos de error en `resultados/[dominio]/errores.log`
- Test de diagnóstico disponible en el menú principal

## 📝 Changelog

### v2.0 (Actual)
- ✨ Interfaz gráfica completamente renovada
- 🔧 Consola de salida integrada
- 📊 Monitor de actividad del sistema
- 📄 Exportación PDF mejorada con selector de dominio
- 🏢 Gestión completa de activos
- 🧪 Sistema de pruebas automáticas
- 🚀 Scripts de instalación y lanzamiento

### v1.0
- 🔍 Funcionalidad básica de análisis
- 📁 Estructura inicial del proyecto

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Equipo SECUREVAL** - *Desarrollo inicial* - Sistema de Evaluación de Seguridad

---

⭐ **¡Dale una estrella al proyecto si te ha sido útil!**

📧 **Contacto**: Para consultas y soporte técnico, abre un issue en el repositorio.

🔒 **Nota de Seguridad**: Este software está diseñado para pruebas autorizadas únicamente. El uso no autorizado en sistemas ajenos puede ser ilegal.
