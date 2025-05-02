# 🕵️‍♂️ MeLi: Detección de Tráfico Web Anómalo

Este proyecto tiene como objetivo desarrollar un sistema automático que permita detectar si una visita al sitio web de Mercado Libre fue realizada por un **humano** o por un **proceso automatizado** (bot, scraper, etc).

---

## ⚙️ Estructura del Proyecto

```bash
.
├── data/               # Datos crudos y procesados
│   ├── processed/
│   └── raw/
├── Dockerfile          # Imagen Docker para reproducibilidad
├── models/             # Modelos entrenados o serializados
├── notebooks/          # Exploración inicial y modelado
│   ├── 1.0-dape-initial-data-exploration.ipynb
│   └── 2.0-dape-model.ipynb
├── references/         # Material de apoyo y documentación técnica
├── reports/            # Figuras, gráficos y reportes generados
├── requirements.txt    # Dependencias del entorno
├── run_docker.sh       # Script para ejecutar el proyecto con Docker
├── setup/              # Código de configuración y app en Streamlit
│   └── streamlit.py
└── README.md           # Este archivo
```

---

## 🧪 Metodología

### 1. Exploración inicial
- Análisis del comportamiento general de visitantes: horarios, user-agents, IPs, rutas accedidas, códigos de respuesta.
- Identificación de patrones típicos de bots: user-agents como `curl`, `Scrapy`, referrers vacíos, frecuencias nocturnas.

### 2. Ingeniería de características
- Creación de variables por fila (por visita):
  - `is_suspicious_ua`, `is_bot_session`, `suspicious_post_usage`, etc.
- Agregación por IP:
  - Total de requests, tasa de errores, actividad nocturna, desviación de bytes enviados, etc.

### 3. Detección no supervisada
- Reducción dimensional con PCA.

---

## 🚀 Uso con Docker

### 1. Construir y ejecutar

```bash
chmod +x run_docker.sh
./run_docker.sh

