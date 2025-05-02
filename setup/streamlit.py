import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import seaborn as sns

BASE_PATH = os.getcwd()
raw_data_path = os.path.join(BASE_PATH, 'data', 'raw', 'trafico_web_sintetico.csv')

def plot_horizontal_bars(plot_data, type='bar'):
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20,6))
    axes = axes.flatten()
    
    for i, (data, title, xlabel, ylabel) in enumerate(plot_data):
        if type == 'bar':
            colors = cm.RdBu(np.linspace(0, 1, len(data)))
            axes[i].barh(data.index, data.values, color=colors)
        else:
            axes[i].plot(data.index, data.values)
        axes[i].set_title(title)
        axes[i].set_xlabel(xlabel)
        axes[i].set_ylabel(ylabel)

    if len(plot_data) < len(axes):
        fig.delaxes(axes[-1])

    plt.tight_layout()
    st.pyplot(fig)


## Load Data
df = pd.read_csv(os.path.join(BASE_PATH, 'data', 'raw', 'trafico_web_sintetico.csv'))

## Dashboard
st.markdown("""
# MeLi\: :red[Detección de Tráfico Web Anómalo] :robot_face: :warning:
            
## Proposito: 
Crear un sistema automatico cuya única tarea sea detectar si la visita al sitio web de Mercado Libre es o no es hecha por un ser humano.
""")

tab1, tab2, tab3, tab4 = st.tabs(["¿Qué tenemos? :open_book:", 
                                        "Mise en place :scientist:", 
                                        "Golem :shield:",
                                        "Sugerencias :bell:"])

with tab1:
    st.image(os.path.join(BASE_PATH, 'references', 'memes', 'gandalf_reading.jpeg'), width=400)

    st.markdown("""
    ### ¿Cómo voy a destruir algo que no conozco? ¡A explorar!
    | Campo             | Descripción |
    |------------------|-------------|
    | `timestamp`       | Momento exacto de la visita |
    | `ip_address`      | Dirección pública del visitante |
    | `user_agent`      | Descripcion del software del visitante: navegador, sistema operativo, etc. |
    | `url_path`        | Parte de la ruta que tomó el visitante en el sitio web (ej. /checkout, /item/12345). |
    | `http_method`     | Tipo de operación del visitante, típicamente GET, POST, PUT, DELETE. |
    | `response_code`   | Estado de la operación que hizo el visitante (200 = OK, 404 = no encontrado, 403 = prohibido, etc). |
    | `bytes_sent`      | Tamaño en bytes de la información devuelta por el servidor. |
    | `referrer`        | Página desde la cual el usuario accedió a la actual (header Referer). |
    | `session_id`      | Identificador único para una sesión (puede venir de cookies o headers). |
    | `country_code`    | Código de país desde donde proviene la IP. |

    - 120K visitas al sitio web
    - `referrer` único campo con valores vacíos (30%)     

    """)

    # Convertir 'timestamp' a datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df['response_code'] = df['response_code'].astype('string')

    # Convertir el resto de columnas object a string (excepto las ya transformadas)
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype('string')

    df['referrer'] = df['referrer'].fillna('NULO')

    st.markdown("#### 1. Comportamiento general de los visitantes")

    # Preparar los datos (esto asume que ya tienes `df` cargado)
    top_agents = df['user_agent'].value_counts().head(10).sort_values()
    top_http_methods = df['http_method'].value_counts().head(10).sort_values()
    top_ip_address = df['ip_address'].value_counts().head(10).sort_values()
    top_response_code = df['response_code'].value_counts().head(10).sort_values()
    top_sessions = df['session_id'].value_counts().head(10).sort_values()
    top_country_code = df['country_code'].value_counts().head(10).sort_values()
    top_url_path = df['url_path'].value_counts().head(10).sort_values()
    top_referrer = df['referrer'].value_counts().head(10).sort_values()
    top_timestamp_date = df["timestamp"].dt.date.astype('str').value_counts().sort_index()
    top_timestamp_hour = df["timestamp"].dt.hour.value_counts().sort_index()

    # Lista de datos y configuraciones
    plots = [
        (top_agents, 'User agents por número de solicitudes', 'numero de solicitudes', 'User Agents'),
        (top_http_methods, 'Métodos HTTP por número de solicitudes', 'numero de solicitudes', 'Método HTTP'),
        (top_ip_address, 'Top 10 IPS por número de solicitudes', 'numero de solicitudes', 'IPS'),
        (top_sessions, 'Top 10 session_id por número de solicitudes', 'numero de solicitudes', 'session_id'),
        (top_response_code, 'Códigos de respuesta HTTP', 'numero de solicitudes', 'Código HTTP'),
        (top_country_code, 'País por número de solicitudes', 'numero de solicitudes', 'Código de país'),
        (top_url_path, 'Top 10 rutas visitadas por número de solicitudes', 'numero de solicitudes', 'Rutas'),
        (top_referrer, 'Top 10 referrer por número de solicitudes', '% de solicitudes', 'referrer'),
        (top_timestamp_date, 'Fecha de visita por número de solicitudes', 'Fecha', 'Numero de solicitudes'),
        (top_timestamp_hour, 'Hora de visita por número de solicitudes', 'Numero de solicitudes', ''),
    ]

    # Crear figura y ejes
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20,6))
    axes = axes.flatten()

    plot_horizontal_bars(plots[0:2])

    st.markdown("""
    :blue-background[**Observaciones**]

    - **Software usado por los visitantes:** 
        - Solo hay 10 agentes de usuario distintos
        - `python-request`, `go-http-client`, `Scrapy`, `curl` son hechos por procesos automaticos (~8000 visitas cada uno).
                
    - **Metodos usados**
        - Solo 2 tipos de métodos: GET (consultar información) y POST (enviar datos).
        - Casi todo el tráfico es GET ~95%.
    """)

    plot_horizontal_bars(plots[2:4])  
             
    st.markdown("""
    :blue-background[**Observaciones**]
    - **IPS de visitantes**:
        - Hay IPs repetidas (la IP más repetida aparece 172 veces).
                
    - **Session ID:**
        - Casi todos son únicos (99.5%).
        - Algunos session_id que se repiten parecen de bots (bot-session-1784). Con hasta 5 repeticiones
    """)

    plot_horizontal_bars(plots[4:6])

    st.markdown("""
    :blue-background[**Observaciones**]
    - **Codigos de respuesta:**
        - Solo 4 tipos de codigos: 200 (OK), 404 (Not Found), 301 (Moved Permanently) and 500 (Internal Server)
        - Casi todo el tráfico es 200 ~90%.
    
    - **Codigo de País:**
        - Solo 6 códigos de país distintos.
        - ?? es el más frecuente (30%). Los demas tienen tráfico similar
    """)

    plot_horizontal_bars(plots[6:8])

    st.markdown("""
    :blue-background[**Observaciones**]
    - **Rutas visitadas:**
        - Es probable que /item esté siendo objetivo principal de scrapers, tratando de obtener información de productos masivamente.

    - **Referrer:**
        - 28% faltante.
        - El más común es https://compras.fake/api (2,017 veces).
        - Hay url que no tienen que ver con el sitio web como smith.com, williams.com, etc
    """)

    plot_horizontal_bars(plots[8:10], type='line')

    st.markdown("""
    :blue-background[**Observaciones**]
    - **Fechas de las visitas:** 
        - Rango entre 2025-04-01 y 2025-04-05.
        - Muchas visitas en la madrugada (0-4 am)
    """)

    df['log_bytes'] = np.log1p(df['bytes_sent'])

    fig, axes = plt.subplots(
        nrows=2, ncols=2,
        figsize=(20,6),
        sharey=False,
        gridspec_kw={"height_ratios": [0.3, 0.7]}
    )

    # --- Fila 1: Boxplots ---
    # Boxplot bytes_sent
    sns.boxplot(x=df['bytes_sent'], ax=axes[0, 0], color='skyblue')
    axes[0, 0].set_title('Boxplot de bytes enviados')
    axes[0, 0].set_xlabel('')

    # Boxplot log_bytes
    sns.boxplot(x=df['log_bytes'], ax=axes[0, 1], color='skyblue')
    axes[0, 1].set_title('Boxplot log(bytes enviados)')
    axes[0, 1].set_xlabel('')

    # --- Fila 2: Histogramas ---
    # Histograma bytes_sent
    sns.histplot(df['bytes_sent'], bins=50, kde=True, ax=axes[1, 0], color='lightblue')
    axes[1, 0].set_title('Histograma de bytes enviados')
    axes[1, 0].set_xlabel('Bytes enviados')
    axes[1, 0].set_ylabel('Frecuencia')

    # Histograma log_bytes
    sns.histplot(df['log_bytes'], bins=50, kde=True, ax=axes[1, 1], color='lightblue')
    axes[1, 1].set_title('Histograma log(bytes enviados)')
    axes[1, 1].set_xlabel('log(Bytes enviados)')
    axes[1, 1].set_ylabel('Frecuencia')

    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("""
    :blue-background[**Observaciones**] 
    - **Bytes enviados:**
        - Concentracion sobre valores pequeños
        - Valores extremadamente altos atípicos
                
    - **Distribucion log Bytes:**
        - La mayoría de los datos caen entre log_bytes 7.5 y 8.9, es decir, entre 1KB y 13KB
        - Caída rápida en valores altos desde 8.9
                
                
    ### Ideas e hipotesis

    | **Campo**     | **Normal en humanos**                         | **Sospechoso en bots o anomalías**                                | **Cómo detectar**                                                                                            |
    | ----------------- | ------------------------------------------------- | --------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
    | `timestamp`     | horarios de visitas durante el dia. // visitas aleatorias                | horarios de visitas en la madrugada. // visitas regulares en el tiempo                                   | Calcular numero de visitas de IP por jornada del dia |
    | `ip_address`    | Muchas IPs con baja frecuencia                    | IPs con alto número de solicitudes                                    | Contar requests por IP y marcar las que están por encima del percentil 95-99 de frecuencia.                      |
    | `user_agent`    | Navegadores comunes (Chrome, Mozilla, etc.)       | `curl`, `Scrapy`, `python-requests` o valores raros y repetidos | Identificar user-agents sospechosos y verificar diversidad por IP                                                |
    | `url_path`      | Navegación variada                                | Frecuencia alta en rutas                                              | Ver rutas más frecuentes por IP                                                                                  |
    | `http_method`   | Uso mayoritario de `GET`, algunos `POST`      | Repetitivo uso de `POST`                                            | Revisar metodos inusuales por `url_path`                                                                       |
    | `response_code` | Mayoría `200`, pocos errores (`404`, `403`) | Alto porcentaje de errores desde una IP                               | Revisar errores por IP (especialmente 404)                                                                 |
    | `bytes_sent`    | Varía según recurso     | Constante (ej. 500 bytes)                                  | Analizar desviación estándar de `bytes_sent` por IP; baja variabilidad es sospechosa.                          |
    | `referrer`      | Presente y coherente (misma sesión)               | Vacío o referrers inconsistentes                                      | Calcular % sin referrer por IP y ver si se concentra en ciertos patrones                                         |
    | `session_id`    | Reutilizado durante la sesión                     | Uno diferente por request o patrones tipo `bot-session-*`          | Detectar exceso de `session_id` únicos por IP y patrones en su nomenclatura (`regex`).                       |
    | `country_code`  | Códigos coherentes con tu mercado objetivo        | `??` o países atípicos                                              | Filtrar por país, marcar IPs con código `??` o regiones atípicas según distribución general.                   |   
        
                
""")

with tab2:
    st.image(os.path.join(BASE_PATH, 'references', 'memes', 'lab.jpg'), width=500)

with tab3:
    st.image(os.path.join(BASE_PATH, 'references', 'memes', 'golem.png'), width=500)

    st.markdown("""
    # ¿Y como construimos este golem?
                
    1. ❌ No tenemos etiquetas reales
    2. ✅ Pero sí tenemos comportamientos sospechosos
                
    Por eso debemos usar un método no supervisado.
                
    ## ¿Por qué elegimos KMeans?
    | Razón                       | Descripción                                                                        |
    | --------------------------- | ---------------------------------------------------------------------------------- |
    | 🔍 Detecta patrones comunes | Agrupa IPs según similitud en características como frecuencia, errores, UA.        |
    | ⚡ Rápido y escalable        | Funciona bien con +100K visitas (como las tuyas) y escala a datasets grandes.      |
    | 🧠 Fácil de interpretar     | Cada cluster tiene un centroide y es fácil examinar su perfil (humano, bot, etc.). |
    | 📈 Se puede visualizar bien | Con PCA se pueden graficar los clusters y explicarlos fácilmente.                  |
    | 🛠️ Simple de implementar   | Requiere solo número de clusters como parámetro, fácil de ajustar con métricas.    |
    """)

    st.image(os.path.join(BASE_PATH, 'reports', 'figures', 'metodo_codo.png'), width=700)
    st.image(os.path.join(BASE_PATH, 'reports', 'figures', 'metricas_kmeans.png'), width=2000)

    st.markdown("""
    | Criterio                  | ¿Qué evalúa?                                                       | ¿Qué buscamos?                          | Resultado con K=3                           | ¿Por qué importa?                                                                 |
    |---------------------------|---------------------------------------------------------------------|------------------------------------------|---------------------------------------------|------------------------------------------------------------------------------------|
    | Método del Codo           | Si agregar más grupos mejora realmente la agrupación               | Un punto de equilibrio ("codo")          | K=3 es donde la mejora se estabiliza         | Nos ayuda a elegir una cantidad adecuada de grupos sin hacer el modelo más complejo |
    | Silhouette Score          | Qué tan bien separados y definidos están los grupos                | Valor alto (hasta 1)                     | K=3 da 0.60 (bueno)                          | Los grupos están bien diferenciados y tienen sentido                               |
    | Índice Calinski-Harabasz | Qué tan distintos son los grupos entre sí                          | Valor alto                               | K=3 da un valor alto                         | Muestra que los grupos tienen buena separación estadística                         |
    | Índice Davies-Bouldin     | Cuánto se parecen los grupos entre sí (menos es mejor)             | Valor bajo (cerca de 0)                  | K=3 da 0.44 (bajo)                           | Los grupos están bien separados, sin mezclarse                                     |

    """)

    st.image(os.path.join(BASE_PATH, 'reports', 'figures', 'cluster.png'), width=700)

    st.markdown("""
    | Cluster | Descripción General        | Comportamiento Destacado                                                                                  | Señales Sospechosas                         | Actividad Nocturna     | Posible Etiqueta     |
    |---------|----------------------------|------------------------------------------------------------------------------------------------------------|---------------------------------------------|------------------------|----------------------|
    | 0       | Tráfico humano típico      | Navegación variada. Referrer normal o desde API. Rutas visitadas diversas.                  | Ninguna. Sin errores, UA válido, IPs limpias. | Moderada (esperable)   | Humano               |
    | 1       | Bot       | Accesos automáticos frecuentes. Navegación mecánica, desde IPs con país desconocido y UA sospechoso.       | Todas activadas: errores, bots, referrer nulo, scraping. | Muy alta (principalmente madrugada) | Bot                  |
    | 2       | Tráfico humano enfocado    | Navegación centrada casi exclusivamente en `/item`, sin errores, desde referrers internos.                 | Ruta muy específica. Comportamiento uniforme. | Algo elevada           | Humano / Requiere revisión |
            
    """)

with tab4:

    st.markdown("""
    # Propuestas de Mitigación
                
    ## 1. Bloqueo o limitación de IPs sospechosas
        - Bloqueadas temporal o permanentemente
        - rate limiting para rutas sensibles como /item
    ## 2. Implementación de CAPTCHAs 
        - Si detecta comportamiento nocturno inusual
        - Vienen de user-agents sospechosos (curl, Scrapy, etc.)
        - No hay referrer o referrer sospechoso

    """)