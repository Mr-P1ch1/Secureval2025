#!/bin/bash
# iniciar.sh - Script de inicio para SECUREVAL
# Sistema de Evaluación de Seguridad Profesional

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner del sistema
mostrar_banner() {
    clear
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                        SECUREVAL                             ║${NC}"
    echo -e "${CYAN}║              Sistema de Evaluación de Seguridad              ║${NC}"
    echo -e "${CYAN}║                       Versión 2.0                            ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Verificar dependencias
verificar_dependencias() {
    echo -e "${BLUE}🔍 Verificando dependencias del sistema...${NC}"
    
    # Python 3
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 no encontrado${NC}"
        echo -e "${YELLOW}💡 Instalar: sudo apt install python3${NC}"
        return 1
    else
        echo -e "${GREEN}✅ Python 3 encontrado${NC}"
    fi
    
    # Pip
    if ! command -v pip3 &> /dev/null; then
        echo -e "${RED}❌ pip3 no encontrado${NC}"
        echo -e "${YELLOW}💡 Instalar: sudo apt install python3-pip${NC}"
        return 1
    else
        echo -e "${GREEN}✅ pip3 encontrado${NC}"
    fi
    
    # Nmap (opcional)
    if command -v nmap &> /dev/null; then
        echo -e "${GREEN}✅ nmap encontrado${NC}"
    else
        echo -e "${YELLOW}⚠️  nmap no encontrado (opcional)${NC}"
        echo -e "${YELLOW}💡 Para análisis avanzado: sudo apt install nmap${NC}"
    fi
    
    # Whatweb (opcional)
    if command -v whatweb &> /dev/null; then
        echo -e "${GREEN}✅ whatweb encontrado${NC}"
    else
        echo -e "${YELLOW}⚠️  whatweb no encontrado (opcional)${NC}"
        echo -e "${YELLOW}💡 Para detección de tecnologías: sudo apt install whatweb${NC}"
    fi
    
    return 0
}

# Verificar estructura del proyecto
verificar_estructura() {
    echo -e "\n${BLUE}📁 Verificando estructura del proyecto...${NC}"
    
    local errores=0
    
    # Directorios principales
    if [ ! -d "app" ]; then
        echo -e "${RED}❌ Directorio 'app' no encontrado${NC}"
        errores=$((errores + 1))
    else
        echo -e "${GREEN}✅ Directorio 'app'${NC}"
    fi
    
    if [ ! -d "resultados" ]; then
        echo -e "${YELLOW}⚠️  Creando directorio 'resultados'...${NC}"
        mkdir -p resultados
    else
        echo -e "${GREEN}✅ Directorio 'resultados'${NC}"
    fi
    
    # Archivos principales
    local archivos=("app/main.py" "app/activos.py" "app/analyzer.py" "app/tratamiento.py" "app/export_pdf.py")
    
    for archivo in "${archivos[@]}"; do
        if [ ! -f "$archivo" ]; then
            echo -e "${RED}❌ Archivo '$archivo' no encontrado${NC}"
            errores=$((errores + 1))
        else
            echo -e "${GREEN}✅ $archivo${NC}"
        fi
    done
    
    return $errores
}

# Test rápido del sistema
test_rapido() {
    echo -e "\n${PURPLE}🧪 Ejecutando test rápido del sistema...${NC}"
    
    if [ -f "test_rapido.py" ]; then
        python3 test_rapido.py
        return $?
    else
        echo -e "${YELLOW}⚠️  test_rapido.py no encontrado, continuando...${NC}"
        return 0
    fi
}

# Menú principal
mostrar_menu() {
    echo -e "\n${CYAN}📋 ¿Qué deseas hacer?${NC}"
    echo -e "${GREEN}1)${NC} Iniciar SECUREVAL (Interfaz Gráfica)"
    echo -e "${GREEN}2)${NC} Ejecutar test rápido del sistema"
    echo -e "${GREEN}3)${NC} Ver información del sistema"
    echo -e "${GREEN}4)${NC} Instalar dependencias Python"
    echo -e "${GREEN}5)${NC} Salir"
    echo ""
    echo -e -n "${BLUE}Selecciona una opción [1-5]: ${NC}"
}

# Instalar dependencias Python
instalar_dependencias() {
    echo -e "\n${BLUE}📦 Instalando dependencias Python...${NC}"
    
    # Crear requirements.txt si no existe
    if [ ! -f "requirements.txt" ]; then
        echo -e "${YELLOW}📝 Creando requirements.txt...${NC}"
        cat > requirements.txt << EOF
tkinter
requests
subprocess
json
os
sys
threading
datetime
time
socket
EOF
    fi
    
    echo -e "${BLUE}🔧 Instalando paquetes adicionales recomendados...${NC}"
    pip3 install --user requests psutil 2>/dev/null || echo -e "${YELLOW}⚠️  Algunas dependencias opcionales no se pudieron instalar${NC}"
    
    echo -e "${GREEN}✅ Dependencias instaladas${NC}"
}

# Información del sistema
mostrar_info() {
    echo -e "\n${CYAN}ℹ️  INFORMACIÓN DEL SISTEMA SECUREVAL${NC}"
    echo -e "${CYAN}════════════════════════════════════════${NC}"
    echo -e "${GREEN}🎯 Propósito:${NC} Sistema de evaluación de seguridad profesional"
    echo -e "${GREEN}🚀 Características:${NC}"
    echo -e "   • Análisis de vulnerabilidades por dominio"
    echo -e "   • Gestión completa de activos"
    echo -e "   • Monitor de actividad del sistema"
    echo -e "   • Consola de salida integrada"
    echo -e "   • Exportación de reportes PDF"
    echo -e "   • Interfaz gráfica moderna"
    echo ""
    echo -e "${GREEN}🔧 Herramientas integradas:${NC}"
    echo -e "   • Escaneo de puertos (nmap)"
    echo -e "   • Detección de tecnologías (whatweb)"
    echo -e "   • Análisis de subdominios"
    echo -e "   • Evaluación de riesgos"
    echo ""
    echo -e "${GREEN}📁 Estructura:${NC}"
    echo -e "   • app/         - Módulos principales"
    echo -e "   • resultados/  - Análisis y reportes"
    echo -e "   • test_*.py    - Pruebas del sistema"
    echo ""
}

# Función principal
main() {
    mostrar_banner
    
    # Verificaciones iniciales
    if ! verificar_dependencias; then
        echo -e "\n${RED}💥 Error: Dependencias faltantes${NC}"
        echo -e "${YELLOW}🔧 Instala las dependencias requeridas y vuelve a ejecutar${NC}"
        exit 1
    fi
    
    if ! verificar_estructura; then
        echo -e "\n${RED}💥 Error: Estructura del proyecto incompleta${NC}"
        echo -e "${YELLOW}🔧 Asegúrate de ejecutar desde el directorio correcto${NC}"
        exit 1
    fi
    
    # Menú interactivo
    while true; do
        mostrar_menu
        read -r opcion
        
        case $opcion in
            1)
                echo -e "\n${GREEN}🚀 Iniciando SECUREVAL...${NC}"
                echo -e "${BLUE}💡 Interfaz gráfica cargando...${NC}"
                python3 -m app.main
                break
                ;;
            2)
                test_rapido
                echo -e "\n${BLUE}Presiona Enter para continuar...${NC}"
                read -r
                ;;
            3)
                mostrar_info
                echo -e "\n${BLUE}Presiona Enter para continuar...${NC}"
                read -r
                ;;
            4)
                instalar_dependencias
                echo -e "\n${BLUE}Presiona Enter para continuar...${NC}"
                read -r
                ;;
            5)
                echo -e "\n${GREEN}👋 ¡Hasta luego!${NC}"
                exit 0
                ;;
            *)
                echo -e "\n${RED}❌ Opción inválida. Selecciona 1-5${NC}"
                sleep 1
                ;;
        esac
    done
}

# Ejecutar función principal
main "$@"
