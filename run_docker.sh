#!/bin/bash

# Nombre de la imagen
IMAGE_NAME="meli-bot-detector"

# Ruta del script de Streamlit (opcional)
STREAMLIT_SCRIPT="setup/streamlit.py"

# Verificar si la imagen ya existe
if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" == "" ]]; then
  echo "🔨 Imagen no encontrada, construyendo $IMAGE_NAME..."
  docker build -t $IMAGE_NAME .
else
  echo "✅ Imagen Docker '$IMAGE_NAME' ya existe. No se reconstruye."
fi

# Menú de opciones
echo ""
echo "¿Qué querés ejecutar dentro del contenedor?"
echo "1) Bash interactivo"
echo "2) Jupyter Notebook (http://localhost:8888)"
echo "3) Streamlit App (http://localhost:8501)"
read -p "Seleccioná una opción (1/2/3): " OPTION

# Ejecutar según opción
case $OPTION in
  1)
    echo "🔧 Ejecutando bash interactivo..."
    docker run -it --rm -v $(pwd):/app $IMAGE_NAME bash
    ;;
  2)
    echo "📒 Ejecutando Jupyter Notebook en http://localhost:8888 ..."
    docker run -it --rm -v $(pwd):/app -p 8888:8888 $IMAGE_NAME \
    jupyter notebook --ip=0.0.0.0 --no-browser --allow-root --NotebookApp.token='' --NotebookApp.password=''

    ;;
  3)
    echo "🌐 Ejecutando Streamlit en http://localhost:8501 ..."
    docker run -it --rm -v $(pwd):/app -p 8501:8501 $IMAGE_NAME \
      streamlit run $STREAMLIT_SCRIPT
    ;;
  *)
    echo "❌ Opción inválida. Abortando."
    exit 1
    ;;
esac
