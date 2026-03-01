import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

load_dotenv()
db_uri = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
sql_engine = create_engine(db_uri)

def load_regression_data():
    print("Carregando dados de eventos confirmados do DW...")
    query = """
        SELECT
            faturamento,
            qtd_adultos,
            qtd_criancas,
            dias_para_evento
        FROM
            fato_evento
        WHERE
            status = 'Confirmado'
            AND faturamento > 0
            AND total_pessoas > 0;
    """
    df = pd.read_sql(query, sql_engine)
    print(f"Carregados {len(df)} eventos confirmados para a análise.")
    return df

def visualizar_regressao(y_test, y_pred, features, coefs, intercept):
    """
    Gera um dashboard visual para avaliar a Regressão Linear.
    """
    sns.set_theme(style="whitegrid")
    fig = plt.figure(figsize=(16, 8))
    gs = fig.add_gridspec(2, 2)

    # --- GRÁFICO 1: Real vs Previsto ---
    ax1 = fig.add_subplot(gs[:, 0])
    sns.scatterplot(x=y_test, y=y_pred, color='blue', alpha=0.6, ax=ax1, s=60)
    
    min_val = min(y_test.min(), y_pred.min())
    max_val = max(y_test.max(), y_pred.max())
    ax1.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Previsão Perfeita')
    
    ax1.set_title('Precisão do Modelo: Valor Real vs. Previsto', fontsize=14)
    ax1.set_xlabel('Faturamento REAL (R$)')
    ax1.set_ylabel('Faturamento PREVISTO (R$)')
    ax1.legend()
    
    # --- GRÁFICO 2: Coeficientes (O que dá dinheiro?) ---
    ax2 = fig.add_subplot(gs[0, 1])
    
    df_coefs = pd.DataFrame({'Variável': features, 'Impacto (R$)': coefs})
    df_coefs = df_coefs.sort_values(by='Impacto (R$)', ascending=False)
    
    colors = ['#2ca02c' if x > 0 else '#d62728' for x in df_coefs['Impacto (R$)']]
    
    sns.barplot(data=df_coefs, x='Impacto (R$)', y='Variável', palette=colors, ax=ax2)
    
    ax2.set_title('Impacto Financeiro por Unidade', fontsize=14)
    ax2.set_xlabel('Aumento no Faturamento (R$)')
    ax2.axvline(0, color='black', linewidth=0.8)

    # --- LÓGICA DE LIMITES INTELIGENTE ---
    vals = df_coefs['Impacto (R$)']
    x_min, x_max = vals.min(), vals.max()
    amplitude = x_max - x_min if x_max != x_min else abs(x_max) # Evita div por zero
    padding = amplitude * 0.3 # 30% de margem para o texto caber

    # Definição dos limites:
    # Esquerda: Se o menor valor for positivo, trava no 0. Se for negativo, dá margem.
    left_limit = 0 if x_min >= 0 else (x_min - padding)
    
    # Direita: Se o maior valor for negativo, trava no 0. Se for positivo, dá margem.
    right_limit = 0 if x_max <= 0 else (x_max + padding)

    ax2.set_xlim(left_limit, right_limit)

    # --- ESCRITA DOS TEXTOS ---
    for i, v in enumerate(vals):
        offset = amplitude * 0.02 # Pequeno espaço entre barra e texto
        
        if v >= 0:
            # Positivo: Texto na direita
            ax2.text(v + offset, i, f'R$ {v:,.2f}', 
                     color='black', va='center', ha='left', fontweight='bold')
        else:
            # Negativo: Texto na esquerda
            ax2.text(v - offset, i, f'R$ {v:,.2f}', 
                     color='black', va='center', ha='right', fontweight='bold')

    # --- GRÁFICO 3: Resíduos (Erros) ---
    ax3 = fig.add_subplot(gs[1, 1])
    residuos = y_test - y_pred
    
    sns.histplot(residuos, kde=True, color='purple', ax=ax3)
    ax3.axvline(0, color='red', linestyle='--')
    
    ax3.set_title('Distribuição dos Erros', fontsize=14)
    ax3.set_xlabel('Erro (R$)')
    ax3.set_ylabel('Frequência')

    plt.tight_layout()
    plt.show()

def main():
    df = load_regression_data()
    
    if df.empty or len(df) < 5:
        print("Não há dados suficientes para uma análise de regressão.")
        return

    features = ['qtd_adultos', 'qtd_criancas', 'dias_para_evento']
    target = 'faturamento'
    
    X = df[features]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Treinando modelo de Regressão Linear...")
    model = LinearRegression()
    model.fit(X_train, y_train)

    print("\n--- 📈 Avaliação do Modelo ---")
    
    y_pred = model.predict(X_test)
    
    r2 = r2_score(y_test, y_pred)
    print(f"R-squared (R²): {r2 * 100:.2f}%")
    
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    print(f"RMSE (Erro Médio): R$ {rmse:.2f}")

    print("\n--- 💰 Impacto (Coeficientes) ---")
    intercept = model.intercept_
    coefficients = model.coef_ # Array numpy direto
    
    for feat, coef in zip(features, coefficients):
        print(f"  - {feat}: R$ {coef:.2f}")

    # --- CHAMADA DA VISUALIZAÇÃO ---
    print("\nGerando gráficos de Regressão...")
    visualizar_regressao(y_test, y_pred, features, coefficients, intercept)

if __name__ == "__main__":
    main()