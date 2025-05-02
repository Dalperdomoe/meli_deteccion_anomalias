# 🧪 Prueba Técnica – Detección de Tráfico Web Anómalo
Agradecemos tu interés en participar en el proceso de selección de Data Scientist en Mercado Libre.

## 🎯 Objetivo
El propósito de esta prueba es evaluar tu capacidad para diseñar e implementar una solución de machine learning que permita detectar tráfico web anómalo o automatizado (por ejemplo, generado por bots o scrapers) a partir de logs HTTP simulados.

La prueba reta tus conocimientos en:
- Ciencia de datos y machine learning aplicado a ciberseguridad.
- Procesamiento y análisis de grandes volúmenes de datos.
- Pensamiento crítico y diseño de soluciones prácticas.
- Comunicación clara de resultados.

---

## 📁 Datos
Se incluye el archivo: `trafico_web_sintetico.csv`

Cada fila representa una solicitud HTTP y contiene los siguientes campos:

| Campo             | Descripción |
|------------------|-------------|
| `timestamp`       | Fecha y hora de la solicitud. |
| `ip_address`      | Dirección IP del cliente. |
| `user_agent`      | Identificador del navegador o cliente. |
| `url_path`        | Ruta solicitada en el sitio. |
| `http_method`     | Método HTTP (`GET`, `POST`, etc). |
| `response_code`   | Código de respuesta del servidor (200, 404, etc). |
| `bytes_sent`      | Tamaño de la respuesta. |
| `referrer`        | URL de referencia. |
| `session_id`      | ID de sesión del usuario o bot. |
| `country_code`    | Código de país del origen del tráfico. |

---

## 🧩 Tu desafío

### 1. **Exploración y Análisis**
- Realiza un análisis exploratorio del dataset.
- Busca patrones de comportamiento normales y anómalos.
- ¿Qué insights relevantes puedes extraer del tráfico?

### 2. **Diseño de la Solución**
- Describe tu enfoque para detectar tráfico automatizado.
- ¿Qué features derivadas son útiles para esta tarea?
- ¿Qué modelo/s usarías y por qué?

### 3. **Modelado**
- Implementa una solución basada en ML para identificar anomalías o bots.
- Puede ser supervisada o no supervisada.
- Justifica tu elección y describe tus pasos.

### 4. **Evaluación**
- ¿Cómo evaluás la efectividad de tu modelo?
- ¿Qué métricas usarías en ausencia de labels confiables?
- Identifica ejemplos concretos de tráfico sospechoso.

### 5. **Presentación de Resultados**
- Comunica de manera clara y visual tus hallazgos, adaptándolos a audiencias no técnicas, destacando el impacto y el valor que generan para el negocio.
- Propón posibles acciones de mitigación.
- (Plus) Construye un dashboard o visualización interactiva.

### 6. **(Plus) Automatización**
- Describe cómo se podría automatizar este flujo de análisis y detección.
- ¿Qué servicios o arquitectura usarías si esto estuviera en producción (cloud, scripts, pipelines, etc)?

---

## ✅ Entregables (GitHub asegurándote de que esté autenticado)

- Un **Jupyter Notebook** o script :
  - Código comentado y estructurado.
  - Visualizaciones y análisis.
  - Explicaciones claras sobre tus decisiones.
  
- **README** (puede ser parte del notebook) que incluya:
  - Tu entendimiento del problema.
  - Metodología y pasos seguidos.
  - Limitaciones y posibles mejoras.

---

## 🧠 Tips

- Se valorará la claridad, el razonamiento y la practicidad.
- No buscamos una solución perfecta, sino bien pensada.
- Puedes usar cualquier librería que consideres útil (scikit-learn, pandas, seaborn, PyOD, etc).
- Si haces suposiciones, ¡explícalas!

---

¡Buena suerte! 🚀
