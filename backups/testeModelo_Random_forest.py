import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import joblib  # ou use pickle se preferir
import numpy as np
# Lista com os caminhos dos seus arquivos .csv
arquivos_csv = [
    "data\\02-14-2018.csv",
    "data\\02-15-2018.csv",
    "data\\02-21-2018.csv",
    "data\\02-22-2018.csv"
]

# Lista exata de colunas usadas pelo modelo
colunas_usadas = [
    'Dst Port', 'Protocol', 'Flow Duration', 'Tot Fwd Pkts', 'TotLen Fwd Pkts',
    'Fwd Pkt Len Max', 'Fwd Pkt Len Min', 'Fwd Pkt Len Mean', 'Fwd Pkt Len Std',
    'Bwd Pkt Len Max', 'Bwd Pkt Len Min', 'Bwd Pkt Len Mean', 'Bwd Pkt Len Std',
    'Flow Pkts/s', 'Flow IAT Max', 'Fwd IAT Tot', 'Fwd IAT Max', 'Bwd IAT Tot',
    'Bwd IAT Mean', 'Bwd IAT Std', 'Bwd IAT Max', 'Bwd IAT Min', 'Fwd Header Len',
    'Fwd Pkts/s', 'Bwd Pkts/s', 'Pkt Len Min', 'Pkt Len Max', 'Pkt Len Mean',
    'Pkt Len Std', 'RST Flag Cnt', 'PSH Flag Cnt', 'ACK Flag Cnt', 'URG Flag Cnt',
    'ECE Flag Cnt', 'Down/Up Ratio', 'Pkt Size Avg', 'Fwd Seg Size Avg',
    'Bwd Seg Size Avg', 'Subflow Fwd Pkts', 'Subflow Fwd Byts', 'Init Fwd Win Byts',
    'Init Bwd Win Byts', 'Fwd Act Data Pkts', 'Fwd Seg Size Min', 'Active Mean',
    'Active Std', 'Active Max', 'Active Min', 'Idle Max', 'Idle Min'
]

# Carregar e concatenar os arquivos
df = pd.concat([pd.read_csv(f, usecols=colunas_usadas + ["Label"]) for f in arquivos_csv], ignore_index=True)

# Pré-processamento
df = df.dropna()
X = df[colunas_usadas]
y = df["Label"]

# Encode dos rótulos
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# Carregar modelo Random Forest
rf_model = joblib.load("Models\\random_forest_model.pkl")

# Substituir valores infinitos por nan
X = np.where(np.isinf(X), np.nan, X)

# Substituir NaNs por 0 (ou média, ou outro valor apropriado)
X = np.nan_to_num(X, nan=0.0, posinf=1e6, neginf=-1e6)  # você pode ajustar esses valores conforme o contexto

# Garantir que está como float32
X = X.astype(np.float32)


# Previsão
y_pred = rf_model.predict(X)

# Avaliação
print("Total de registros carregados:", len(df))
print("=== Avaliação do Modelo Random Forest ===")
print("Matriz de Confusão:")
print(confusion_matrix(y_encoded, y_pred))

print("\nRelatório de Classificação:")
labels = sorted(set(y_encoded))
print(classification_report(
    y_encoded,
    y_pred,
    labels=labels,
    target_names=le.inverse_transform(labels),
    zero_division=0
))
