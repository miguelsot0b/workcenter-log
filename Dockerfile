FROM mcr.microsoft.com/playwright/python:v1.40.0-noble

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto de los archivos
COPY . .

# Crear directorio de descargas
RUN mkdir -p downloads

# Comando por defecto
CMD ["python", "main.py"]
