import os
import pandas as pd
import numpy as np
from pathlib import Path


def clasificar_referrer(ref):
    if ref == 'NULO':
        return 'NULO'
    elif 'mercadolibre' in ref:
        return 'INTERNO'
    elif 'api' in ref.strip().lower():
        return 'API'
    else:
        return 'OTRO'


def main():
    # Paths
    BASE_PATH = os.getcwd()
    RAW_PATH = os.path.join(BASE_PATH, 'data', 'raw', 'trafico_web_sintetico.csv')
    PROCESSED_PATH = os.path.join(BASE_PATH, 'data', 'processed', 'processed.csv')

    # Cargar datos
    df = pd.read_csv(RAW_PATH)

    # Preprocesamiento básico
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce', utc=True)
    df['response_code'] = df['response_code'].astype('string')
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].astype('string')
    df['referrer'] = df['referrer'].fillna('NULO')

    # Clasificación de referrer
    df['referrer_type'] = df['referrer'].apply(clasificar_referrer)
    df = pd.concat([
        df.reset_index(drop=True),
        pd.get_dummies(df['referrer_type'], prefix='referrer_type')
    ], axis=1)

    # Normalización de rutas
    df['standar_url_path'] = df['url_path'].str.extract(r'^(/[^/?]+)', expand=False)

    # Variables binarias por fila
    df['is_bot_session'] = df['session_id'].str.contains(r'bot-session-\d+', na=False)
    df['is_country_unknown'] = df['country_code'] == '??'

    df['suspicious_post_usage'] = (
        (df['http_method'] == 'POST') &
        (df['standar_url_path'].isin(['/item', '/search', '/home', '/category', '/profile', '/checkout']))
    )

    df['suspicious_high_freq_path'] = df['standar_url_path'].isin(['/item'])

    suspicious_agents = ['python-requests', 'curl', 'Scrapy', 'go-http-client']
    df['is_suspicious_ua'] = df['user_agent'].str.contains('|'.join(suspicious_agents), case=False, na=False)

    df = df.sort_values(by=['session_id', 'timestamp'])
    df['delta_seconds'] = df.groupby('session_id')['timestamp'].diff().dt.total_seconds()

    df['is_not_found_error'] = df['response_code'].isin(['404'])


    # Agrupación por IP
    ip_features = df.groupby('ip_address').agg(
        total_requests=('timestamp', 'count'),
        std_byte_size=('bytes_sent', 'std')
    )
    ip_features['std_byte_size'] = ip_features['std_byte_size'].fillna(0)

    p95 = ip_features['total_requests'].quantile(0.95)
    ip_features['total_requests_above_p95'] = ip_features['total_requests'] > p95

    ip_features['had_error'] = df.groupby('ip_address')['is_not_found_error'].max()
    ip_features['had_suspicious_ua'] = df.groupby('ip_address')['is_suspicious_ua'].max()
    ip_features['had_referrer_type_interno'] = df.groupby('ip_address')['referrer_type_INTERNO'].max()
    ip_features['had_referrer_type_api'] = df.groupby('ip_address')['referrer_type_API'].max()
    ip_features['had_referrer_type_nulo'] = df.groupby('ip_address')['referrer_type_NULO'].max()
    ip_features['had_bot_sessions'] = df.groupby('ip_address')['is_bot_session'].max()
    ip_features['had_unknown_country'] = df.groupby('ip_address')['is_country_unknown'].max()
    ip_features['had_suspicious_post_usage'] = df.groupby('ip_address')['suspicious_post_usage'].max()
    ip_features['had_suspicious_high_freq_path'] = df.groupby('ip_address')['suspicious_high_freq_path'].max()

    ip_features['night_activity_rate'] = (
        df[df['timestamp'].dt.hour.between(0, 4)]
        .groupby('ip_address')
        .size() / df.groupby('ip_address').size()
    ).fillna(0)

    # Guardar resultados
    ip_features.drop(columns='total_requests').to_csv(PROCESSED_PATH, index=False)
    print(f"✅ Datos procesados guardados en: {PROCESSED_PATH}")


if __name__ == "__main__":
    main()
