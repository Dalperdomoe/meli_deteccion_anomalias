# Imagen base con Python
FROM python:3.10-slim

# Crear y establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto al contenedor
COPY . /app

# Instalar las dependencias de Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Puerto por si usás Streamlit
EXPOSE 8501

# Comando por defecto (podés cambiarlo)
CMD ["python"]