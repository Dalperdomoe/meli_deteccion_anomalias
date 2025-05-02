import os
import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler
from .constants import cluster_labels_map

BASE_PATH = os.getcwd()
MODEL_PATH = os.path.join(BASE_PATH, 'models','kmeans_model.pkl')
NEW_DATA_PATH = os.path.join(BASE_PATH, 'data', 'raw', 'new_data.csv')
PREDICTION_PATH = os.path.join(BASE_PATH, 'data', 'prediction', 'prediction.csv')

def main():
    kmeans = joblib.load(MODEL_PATH)

    df = pd.read_csv(NEW_DATA_PATH)

    X_scaled_nuevo = StandardScaler().fit_transform(df)

    labels_nuevos = kmeans.predict(X_scaled_nuevo)

    df['cluster'] = labels_nuevos
    df['etiqueta'] = df['cluster'].map(cluster_labels_map)

    df.to_csv(PREDICTION_PATH, index=False)

if __name__ == "__main__":
    main()
