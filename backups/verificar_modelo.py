import xgboost as xgb
import numpy as np

# 1. Carregue o modelo
model = xgb.Booster()
model.load_model('backend_py\\xgboost_model.ubj')  # ou .json

# 2. Obtenha os nomes das features
expected_features = model.feature_names

# 3. Verifique
num_features = model.num_features()
print(f"O modelo espera {num_features} features (mas não sabemos os nomes)")

dummy_data = np.zeros((1, model.num_features()))
dmatrix = xgb.DMatrix(dummy_data)

try:
    model.predict(dmatrix)
except Exception as e:
    print("Erro que pode conter pistas:", str(e))


