# Usa uma imagem base do Windows
FROM mcr.microsoft.com/windows:ltsc2019

# Define o diretório de trabalho
WORKDIR C:/app

# Copia os arquivos do projeto
COPY . .

# Instala Python
RUN powershell -Command \
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.10.0/python-3.10.0-amd64.exe" -OutFile python.exe ; \
    Start-Process python.exe -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait ; \
    Remove-Item python.exe

# Instala as dependências Python UMA POR UMA para debug
RUN pip install PySide6
RUN pip install psutil
RUN pip install pillow
RUN pip install pandas
RUN pip install numpy
RUN pip install requests
RUN pip install reportlab
RUN pip install watchdog
RUN pip install pystray
RUN pip install win10toast
RUN pip install pywin32


# Tenta instalar as opcionais (ignora erros)
RUN pip install xgboost || echo "XGBoost falhou - continuando..."
RUN pip install scapy || echo "Scapy falhou - continuando..."
RUN pip install scikit-learn || echo "Scikit-learn falhou - continuando..."
RUN pip install joblib || echo "Joblib falhou - continuando..."
RUN pip install pybloom-live || echo "Pybloom-live falhou - continuando..."



# Comando para executar a aplicação
CMD ["python", "backend_py/back_Hometabwidget.py"]