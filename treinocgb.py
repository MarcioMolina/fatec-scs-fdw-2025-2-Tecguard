import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import xgboost as xgb
from sklearn.feature_selection import SelectKBest, f_classif
from imblearn.over_sampling import SMOTE
import matplotlib.pyplot as plt
import os
import joblib

# ========== CONFIGURAÇÕES ==========
DATASET_DIR = './data'
NUM_CSVS = 4
USE_GPU = True
FEATURE_SELECTION = True
APPLY_SMOTE = True  # Novo: aplicar oversampling

# ========== CARREGAMENTO DE DADOS ==========
def load_data(limit):
    files = [f for f in os.listdir(DATASET_DIR) if f.endswith('.csv')][:limit]
    dfs = []
    for f in files:
        df = pd.read_csv(os.path.join(DATASET_DIR, f), low_memory=False)
        df = df.loc[:, ~df.columns.duplicated()]
        if 'Timestamp' in df.columns:
            df.drop('Timestamp', axis=1, inplace=True)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

# ========== PRÉ-PROCESSAMENTO ==========
def preprocess(df):
    le = LabelEncoder()
    y = le.fit_transform(df['Label'])
    X = df.drop('Label', axis=1)

    for col in X.select_dtypes(include=['float64']).columns:
        X[col] = X[col].astype('float32')
    for col in X.select_dtypes(include=['int64']).columns:
        X[col] = X[col].astype('int32')

    X = X.replace([np.inf, -np.inf], np.nan)
    for col in X.columns:
        if X[col].isnull().any():
            if X[col].dtype.kind in 'fi':
                X[col].fillna(X[col].mean(), inplace=True)
            else:
                X[col].fillna(X[col].mode()[0], inplace=True)

    joblib.dump(le, 'label_encoder.pkl')
    return X, y, le.classes_

# ========== SELEÇÃO DE FEATURES ==========
def select_features(X, y, k=50):
    selector = SelectKBest(f_classif, k=k)
    X_new = selector.fit_transform(X, y)
    selected = X.columns[selector.get_support()]
    return X_new, selected

# ========== TREINAMENTO XGBOOST ==========
def train_xgboost(X, y, classes):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    if APPLY_SMOTE:
        print("\nAplicando SMOTE para balanceamento...")
        sm = SMOTE(random_state=42)
        X_train, y_train = sm.fit_resample(X_train, y_train)
        print(f"Shape após SMOTE: {X_train.shape}")

    params = {
        'objective': 'multi:softmax',
        'num_class': len(classes),
        'device': 'cuda',
        'eval_metric': 'mlogloss',
        'max_depth': 6,
        'learning_rate': 0.05,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'reg_alpha': 0.1,
        'reg_lambda': 0.1,
        'n_jobs': -1, 
        'seed': 42
    }

    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    results = []

    for fold, (train_idx, val_idx) in enumerate(skf.split(X_train, y_train)):
        print(f"\n=== Fold {fold+1} ===")
        dtrain = xgb.DMatrix(X_train[train_idx].astype('float32'), label=y_train[train_idx])
        dval = xgb.DMatrix(X_train[val_idx].astype('float32'), label=y_train[val_idx])

        model = xgb.train(
            params,
            dtrain,
            num_boost_round=1000,
            evals=[(dtrain, 'train'), (dval, 'val')],
            early_stopping_rounds=50,
            verbose_eval=50
        )

        preds = model.predict(xgb.DMatrix(X_train[val_idx].astype('float32')))
        report = classification_report(y_train[val_idx], preds, output_dict=True)
        accuracy = report['accuracy']
        results.append(accuracy)
        print(f"Fold {fold+1} Accuracy: {accuracy:.4f}")

    print("\nTreinando modelo final...")
    final_model = xgb.train(
        params,
        xgb.DMatrix(X_train.astype('float32'), label=y_train),
        num_boost_round=model.best_iteration + 50
    )

    test_preds = final_model.predict(xgb.DMatrix(X_test.astype('float32')))
    print("\nRelatório Final de Classificação:")
    print(classification_report(y_test, test_preds, target_names=classes))

    plt.figure(figsize=(12, 8))
    xgb.plot_importance(final_model, max_num_features=20)
    plt.show()

    model_path = 'xgboost_model.model'
    final_model.save_model(model_path)  # ✅ CORREÇÃO AQUI
    print(f"\nModelo salvo em: {model_path}")

    return final_model

class XGBModelValidator:
    def __init__(self, model_path, label_encoder_path=None):
        """
        Inicializa o validador com modelo XGBoost pré-treinado
        
        Args:
            model_path: caminho para o arquivo .model do XGBoost
            label_encoder_path: caminho para o LabelEncoder (opcional)
        """
        self.model = xgb.Booster()
        self.model.load_model(model_path)
        
        if label_encoder_path:
            import joblib
            self.le = joblib.load(label_encoder_path)
        else:
            self.le = None
    
    def predict(self, data):
        """
        Faz previsões para os dados fornecidos
        
        Args:
            data: DataFrame ou array numpy com as features
            
        Returns:
            array com as previsões
        """
        dmatrix = xgb.DMatrix(data.astype('float32'))
        return self.model.predict(dmatrix)
    
    def verify_with_row(self, row, expected_class=None, verbose=True):
        """
        Verifica a predição para uma linha específica
        
        Args:
            row: DataFrame com uma linha ou array numpy (1, n_features)
            expected_class: classe esperada (opcional para validação)
            verbose: se True, imprime resultados detalhados
            
        Returns:
            tuple: (classe prevista, probabilidades)
        """
        if isinstance(row, pd.DataFrame):
            row_data = row.values
        else:
            row_data = np.array(row).reshape(1, -1)
            
        pred = self.predict(row_data)
        pred_class = int(pred[0])
        
        if verbose:
            print("\n=== VERIFICAÇÃO DE LINHA ===")
            print(f"Input:\n{row}")
            
            if self.le:
                class_name = self.le.inverse_transform([pred_class])[0]
                print(f"Classe prevista: {pred_class} ({class_name})")
            else:
                print(f"Classe prevista: {pred_class}")
                
            if expected_class is not None:
                if self.le:
                    expected_name = self.le.inverse_transform([expected_class])[0]
                    print(f"Classe esperada: {expected_class} ({expected_name})")
                else:
                    print(f"Classe esperada: {expected_class}")
                
                print(f"✅ Acerto" if pred_class == expected_class else "❌ Erro")
        
        return pred_class, pred
    
    def evaluate_control_rows(self, feature_columns, verbose=True):
        """
        Avalia linhas de controle predefinidas
        
        Args:
            feature_columns: lista com nomes das features (para DataFrame)
            verbose: se True, imprime resultados detalhados
            
        Returns:
            DataFrame com resultados
        """
        # Linha de controle (valores zero)
        zero_row = pd.DataFrame([np.zeros(len(feature_columns))], columns=feature_columns)
        
        # Linha de anomalia (valores altos)
        anomaly_row = pd.DataFrame([np.full(len(feature_columns), 100)], columns=feature_columns)
        
        # Testes
        results = []
        for row, row_type in [(zero_row, 'zeros'), (anomaly_row, 'anomalia')]:
            pred_class, _ = self.verify_with_row(row, verbose=verbose)
            results.append({
                'tipo': row_type,
                'classe_prevista': pred_class,
                'dados': row.values[0]
            })
            
        return pd.DataFrame(results)

# Exemplo de uso:
if __name__ == "__main__":
    # 1. Carregar o validador
    validator = XGBModelValidator(
        model_path="xgboost_model.model",
        label_encoder_path="label_encoder.pkl"
    )
    
    # 2. Criar uma linha de teste (exemplo com 5 features)
    test_row = pd.DataFrame([[0.1, 10, 5, 100, 2]], 
                          columns=['feature1', 'feature2', 'feature3', 'feature4', 'feature5'])
    
    # 3. Verificar predição
    validator.verify_with_row(test_row, expected_class=0)
    
    # 4. Testar linhas de controle
    control_results = validator.evaluate_control_rows(test_row.columns)
    print("\nResultados de controle:")
    print(control_results)

# ========== EXECUÇÃO ==========
if __name__ == '__main__':
    print("=== Carregando dados ===")
    df = load_data(NUM_CSVS)

    print("\n=== Pré-processamento ===")
    X, y, classes = preprocess(df)

    if FEATURE_SELECTION:
        print("\nSelecionando melhores features...")
        X, selected = select_features(X, y, k=50)
        print(f"Features selecionadas: {list(selected)}")

    print("\n=== Treinando XGBoost ===")
    print(f"Shape final: {X.shape}")
    print(f"Classes: {classes}")
    model = train_xgboost(X, y, classes)
    