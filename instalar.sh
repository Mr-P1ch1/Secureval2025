#!/bin/bash
# instalar.sh - Script de instalación automática para SECUREVAL

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                  INSTALADOR SECUREVAL                       ║${NC}"
echo -e "${CYAN}║              Configuración Automática                       ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Función para detectar el sistema operativo
detectar_os() {
    if [ -f /etc/debian_version ]; then
        echo "debian"
    elif [ -f /etc/redhat-release ]; then
        echo "redhat"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    else
        echo "unknown"
    fi
}

# Instalar dependencias del sistema
instalar_dependencias_sistema() {
    local os_type=$(detectar_os)
    
    echo -e "${BLUE}🔧 Instalando dependencias del sistema...${NC}"
    
    case $os_type in
        "debian")
            echo -e "${GREEN}📦 Detectado: Sistema basado en Debian/Ubuntu${NC}"
            sudo apt update
            sudo apt install -y python3 python3-pip python3-tk nmap whatweb
            ;;
        "redhat")
            echo -e "${GREEN}📦 Detectado: Sistema basado en Red Hat/CentOS${NC}"
            sudo yum install -y python3 python3-pip python3-tkinter nmap
            # whatweb puede requerir instalación manual en Red Hat
            ;;
        "macos")
            echo -e "${GREEN}📦 Detectado: macOS${NC}"
            if command -v brew &> /dev/null; then
                brew install python3 nmap
            else
                echo -e "${YELLOW}⚠️  Homebrew no encontrado. Instala manualmente: python3, nmap${NC}"
            fi
            ;;
        *)
            echo -e "${YELLOW}⚠️  Sistema operativo no reconocido. Instala manualmente:${NC}"
            echo -e "   - python3"
            echo -e "   - python3-pip"
            echo -e "   - python3-tk (tkinter)"
            echo -e "   - nmap"
            echo -e "   - whatweb"
            ;;
    esac
}

# Instalar dependencias Python
instalar_dependencias_python() {
    echo -e "\n${BLUE}🐍 Instalando dependencias Python...${NC}"
    
    if [ -f "requirements.txt" ]; then
        pip3 install --user -r requirements.txt
    else
        echo -e "${YELLOW}📝 Instalando dependencias básicas...${NC}"
        pip3 install --user requests psutil
    fi
}

# Configurar estructura de directorios
configurar_estructura() {
    echo -e "\n${BLUE}📁 Configurando estructura de directorios...${NC}"
    
    # Crear directorios necesarios
    mkdir -p resultados
    mkdir -p data
    
    # Verificar permisos
    chmod +x iniciar.sh 2>/dev/null || echo -e "${YELLOW}⚠️  No se pudo hacer ejecutable iniciar.sh${NC}"
    
    echo -e "${GREEN}✅ Estructura configurada${NC}"
}

# Verificar instalación
verificar_instalacion() {
    echo -e "\n${BLUE}🔍 Verificando instalación...${NC}"
    
    local errores=0
    
    # Python 3
    if command -v python3 &> /dev/null; then
        echo -e "${GREEN}✅ Python 3${NC}"
    else
        echo -e "${RED}❌ Python 3${NC}"
        errores=$((errores + 1))
    fi
    
    # Tkinter
    if python3 -c "import tkinter" 2>/dev/null; then
        echo -e "${GREEN}✅ Tkinter${NC}"
    else
        echo -e "${RED}❌ Tkinter${NC}"
        errores=$((errores + 1))
    fi
    
    # Requests
    if python3 -c "import requests" 2>/dev/null; then
        echo -e "${GREEN}✅ Requests${NC}"
    else
        echo -e "${YELLOW}⚠️  Requests (opcional)${NC}"
    fi
    
    # Nmap
    if command -v nmap &> /dev/null; then
        echo -e "${GREEN}✅ Nmap${NC}"
    else
        echo -e "${YELLOW}⚠️  Nmap (opcional)${NC}"
    fi
    
    # Whatweb
    if command -v whatweb &> /dev/null; then
        echo -e "${GREEN}✅ Whatweb${NC}"
    else
        echo -e "${YELLOW}⚠️  Whatweb (opcional)${NC}"
    fi
    
    return $errores
}

# Función principal
main() {
    echo -e "${BLUE}🚀 Iniciando instalación de SECUREVAL...${NC}"
    echo ""
    
    # Solicitar confirmación
    echo -e "${YELLOW}¿Deseas instalar las dependencias del sistema? (requiere sudo) [y/N]:${NC}"
    read -r respuesta
    
    if [[ $respuesta =~ ^[Yy]$ ]]; then
        instalar_dependencias_sistema
    else
        echo -e "${YELLOW}⚠️  Saltando instalación de dependencias del sistema${NC}"
    fi
    
    # Instalar dependencias Python
    instalar_dependencias_python
    
    # Configurar estructura
    configurar_estructura
    
    # Verificar instalación
    if verificar_instalacion; then
        echo -e "\n${GREEN}🎉 ¡Instalación completada exitosamente!${NC}"
        echo -e "${CYAN}📝 Para iniciar SECUREVAL, ejecuta: ./iniciar.sh${NC}"
    else
        echo -e "\n${YELLOW}⚠️  Instalación completada con advertencias${NC}"
        echo -e "${CYAN}📝 Revisa las dependencias faltantes e intenta ejecutar: ./iniciar.sh${NC}"
    fi
}

# Ejecutar instalación
main "$@"
