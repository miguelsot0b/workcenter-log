FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para Playwright
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar navegador Chromium para Playwright
RUN playwright install --with-deps chromium

# Copiar el resto de los archivos
COPY . .

# Crear directorio de descargas
RUN mkdir -p downloads

# Comando por defecto
CMD ["python", "main.py"]
