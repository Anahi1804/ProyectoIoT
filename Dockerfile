# Usamos una imagen oficial de Python ligera
FROM python:3.9-slim

# Le decimos a Docker en qué carpeta trabajar adentro del contenedor
WORKDIR /app

# Copiamos nuestros archivos a la nube
COPY requirements.txt requirements.txt
COPY servidor.py servidor.py

# Instalamos las librerías
RUN pip install -r requirements.txt

# Exponemos el puerto
EXPOSE 5000

# Le decimos qué comando ejecutar al prender el contenedor
CMD ["python", "servidor.py"]