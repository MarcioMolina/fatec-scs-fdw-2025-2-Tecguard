#!/bin/bash

# Script de inicialização para a aplicação TecGuard no Docker

echo "========================================="
echo "Iniciando TecGuard Application"
echo "========================================="

# Configura o display virtual
export DISPLAY=:99

# Inicia o X virtual framebuffer em background
echo "Iniciando Xvfb..."
Xvfb :99 -screen 0 1280x800x24 -ac +extension GLX +render -noreset &
XVFB_PID=$!

# Aguarda o Xvfb inicializar
sleep 3

# Verifica se o Xvfb está rodando
if ! ps -p $XVFB_PID > /dev/null; then
    echo "ERRO: Xvfb falhou ao iniciar"
    exit 1
fi

echo "Xvfb iniciado com PID: $XVFB_PID"

# Configura variáveis de ambiente para Qt
export QT_DEBUG_PLUGINS=1
export QT_QPA_PLATFORM=xcb

# Verifica se as dependências Python estão instaladas
echo "Verificando dependências Python..."
python3 -c "import PySide6, psutil, numpy, pandas, PIL, watchdog, reportlab, requests" && echo "Todas as dependências OK!" || echo "Alguma dependência faltando"

# Navega para o diretório do app
cd /app

echo "Iniciando aplicação Qt..."
echo "========================================="

# Inicia a aplicação Python
exec python3 backend_py/back_Hometabwidget.py