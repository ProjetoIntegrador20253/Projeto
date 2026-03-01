import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# ------------------------------------------------------------------------
# 1. CONEXÃO (Substitua pelos seus dados)
# ------------------------------------------------------------------------
connection_string = 'postgresql://postgres:123456@localhost:5432/projetoint3'
engine = create_engine(connection_string)

# ------------------------------------------------------------------------
# 2. SUA QUERY COM CTE
# ------------------------------------------------------------------------
query = """
WITH PrimeiraCompra AS (
    SELECT
        p.id_prospect,
        MIN(t.data) AS data_primeira_compra
    FROM
        fato_evento AS f
    JOIN
        dim_tempo AS t ON f.fk_tempo = t.id_tempo
    JOIN
        dim_prospect AS p ON f.fk_prospect = p.id_prospect
    WHERE
        f.status = 'Confirmado'
    GROUP BY
        p.id_prospect
)
SELECT
    CASE
        WHEN t2.data = pc.data_primeira_compra THEN 'Novo Cliente'
        ELSE 'Cliente Recorrente'
    END AS tipo_cliente,
    
    COUNT(t1.sk_evento) AS n_contratos,
    SUM(t1.faturamento) AS faturamento_total,
    SUM(t1.lucro_total) AS lucro_total
FROM
    fato_evento AS t1
JOIN
    dim_tempo AS t2 ON t1.fk_tempo = t2.id_tempo
JOIN
    PrimeiraCompra AS pc ON t1.fk_prospect = pc.id_prospect
WHERE
    t1.status = 'Confirmado'
GROUP BY
    tipo_cliente;
"""

# ------------------------------------------------------------------------
# 3. GERAR OS 3 GRÁFICOS (SUBPLOTS)
# ------------------------------------------------------------------------
try:
    df = pd.read_sql(query, engine)
    
    # Configura 3 gráficos lado a lado
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Cores para distinguir as categorias
    colors = ['#1f77b4', '#ff7f0e'] # Azul e Laranja
    
    # --- Gráfico 1: Número de Contratos ---
    sns.barplot(x='tipo_cliente', y='n_contratos', data=df, ax=axes[0], palette=colors)
    axes[0].set_title('Volume de Contratos', fontsize=14)
    axes[0].set_ylabel('Quantidade')
    axes[0].bar_label(axes[0].containers[0]) # Adiciona o número em cima da barra

    # --- Gráfico 2: Faturamento Total ---
    sns.barplot(x='tipo_cliente', y='faturamento_total', data=df, ax=axes[1], palette=colors)
    axes[1].set_title('Faturamento Total', fontsize=14)
    axes[1].set_ylabel('Valor (R$)')
    # Formata rótulos em Milhões (M) ou Milhares (K)
    for p in axes[1].patches:
        valor = p.get_height()
        texto = f'R${valor/1e6:.1f}M' if valor > 1e6 else f'R${valor/1e3:.0f}K'
        axes[1].annotate(texto, 
                         (p.get_x() + p.get_width() / 2., p.get_height()), 
                         ha='center', va='bottom', fontsize=11, fontweight='bold')

    # --- Gráfico 3: Lucro Total ---
    sns.barplot(x='tipo_cliente', y='lucro_total', data=df, ax=axes[2], palette=colors)
    axes[2].set_title('Lucro Total', fontsize=14)
    axes[2].set_ylabel('Valor (R$)')
    for p in axes[2].patches:
        valor = p.get_height()
        texto = f'R${valor/1e6:.1f}M' if valor > 1e6 else f'R${valor/1e3:.0f}K'
        axes[2].annotate(texto, 
                         (p.get_x() + p.get_width() / 2., p.get_height()), 
                         ha='center', va='bottom', fontsize=11, fontweight='bold')

    # Ajustes finais de layout
    for ax in axes:
        ax.set_xlabel('') # Remove o label X redundante
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        
    plt.tight_layout()
    plt.show()
    
    print("Gráficos gerados com sucesso!")

except Exception as e:
    print(f"Erro: {e}")