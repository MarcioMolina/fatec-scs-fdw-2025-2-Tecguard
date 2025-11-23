import xgboost as xgb
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import numpy as np

# Lista com os caminhos dos seus arquivos .csv
arquivos_csv = [
    "data\\02-14-2018.csv",
    "data\\02-15-2018.csv",
    "data\\02-21-2018.csv",
    "data\\02-22-2018.csv"
]

# Lista exata de colunas usadas pelo modelo + "Label"
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
    'Active Std', 'Active Max', 'Active Min', 'Idle Max', 'Idle Min', 'Label'  # <--- Adicionada Label
]

# 1. Carregar todos os CSVs e juntar
df = pd.concat([pd.read_csv(f, usecols=colunas_usadas) for f in arquivos_csv], ignore_index=True)

# 2. Remover valores ausentes
df = df.dropna()

# 3. Separar X e y
X = df.drop(columns=["Label"])
y = df["Label"]

# 4. Codificar os rótulos
le = LabelEncoder()
y_encoded = le.fit_transform(y)

# 5. Carregar o modelo treinado
xgb_model = xgb.XGBClassifier()
xgb_model.load_model("Models\\xgboost_model.model")

# 6. Prever
y_pred = xgb_model.predict(X)

# 7. Avaliação
print("Total de registros carregados:", len(df))
print("=== Avaliação do Modelo XGBoost ===")
print("Matriz de Confusão:")
print(confusion_matrix(y_encoded, y_pred))

print("\nRelatório de Classificação:")
labels = np.unique(y_encoded)  # agora definido corretamente
print(classification_report(
    y_encoded,
    y_pred,
    labels=labels,
    target_names=le.inverse_transform(labels),
    zero_division=0
))