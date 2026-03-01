import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# ------------------------------------------------------------------------
# 1. CONEXÃO
# ------------------------------------------------------------------------
connection_string = 'postgresql://postgres:123456@localhost:5432/projetoint3'
engine = create_engine(connection_string)

# ------------------------------------------------------------------------
# 2. QUERY
# ------------------------------------------------------------------------
query = """
SELECT
    t2.marketing_channel,
    SUM(t1.faturamento) AS faturamento_total,
    SUM(t1.lucro_total) AS lucro_total,
    COUNT(t1.sk_evento) AS n_contratos,
    AVG(t1.faturamento) AS ticket_medio
FROM
    fato_evento AS t1
JOIN
    dim_prospect AS t2 ON t1.fk_prospect = t2.id_prospect
WHERE
    t1.status = 'Confirmado'
GROUP BY
    t2.marketing_channel
ORDER BY
    lucro_total DESC;
"""

# ------------------------------------------------------------------------
# 3. GERAR DASHBOARD COM MARGEM PARA RÓTULOS
# ------------------------------------------------------------------------
try:
    df = pd.read_sql(query, engine)
    
    # Pega Top 8 para não poluir
    df_plot = df.head(8).copy()

    # Configura o grid 2x2
    fig, axes = plt.subplots(2, 2, figsize=(16, 10))
    palette = sns.color_palette("viridis", n_colors=len(df_plot))

    # Função para formatar valores (Milhões/Milhares)
    def format_val(x):
        if x >= 1e6: return f'R${x/1e6:.1f}M'
        if x >= 1e3: return f'R${x/1e3:.0f}K'
        return f'{x:.0f}'

    # --- 1. LUCRO (Superior Esquerdo) ---
    sns.barplot(x='lucro_total', y='marketing_channel', data=df_plot, ax=axes[0, 0], palette=palette)
    axes[0, 0].set_title('Top Canais por Lucro Real', fontsize=14)
    axes[0, 0].set_xlabel('')
    axes[0, 0].set_ylabel('')
    
    # CORREÇÃO: Aumenta o limite direito em 20%
    max_val = df_plot['lucro_total'].max()
    axes[0, 0].set_xlim(0, max_val * 1.2)
    
    for container in axes[0, 0].containers:
        axes[0, 0].bar_label(container, fmt=lambda x: format_val(x), padding=3)

    # --- 2. FATURAMENTO (Superior Direito) ---
    sns.barplot(x='faturamento_total', y='marketing_channel', data=df_plot, ax=axes[0, 1], palette=palette)
    axes[0, 1].set_title('Top Canais por Faturamento Bruto', fontsize=14)
    axes[0, 1].set_xlabel('')
    axes[0, 1].set_ylabel('')
    
    # CORREÇÃO: Margem de 20%
    max_val = df_plot['faturamento_total'].max()
    axes[0, 1].set_xlim(0, max_val * 1.2)

    for container in axes[0, 1].containers:
        axes[0, 1].bar_label(container, fmt=lambda x: format_val(x), padding=3)

    # --- 3. VOLUME (Inferior Esquerdo) ---
    sns.barplot(x='n_contratos', y='marketing_channel', data=df_plot, ax=axes[1, 0], palette=palette)
    axes[1, 0].set_title('Volume de Vendas (Qtd)', fontsize=14)
    axes[1, 0].set_xlabel('')
    axes[1, 0].set_ylabel('')
    
    # CORREÇÃO: Margem de 20%
    max_val = df_plot['n_contratos'].max()
    axes[1, 0].set_xlim(0, max_val * 1.2)

    for container in axes[1, 0].containers:
        axes[1, 0].bar_label(container, padding=3)

    # --- 4. TICKET MÉDIO (Inferior Direito) ---
    sns.barplot(x='ticket_medio', y='marketing_channel', data=df_plot, ax=axes[1, 1], palette=palette)
    axes[1, 1].set_title('Ticket Médio por Canal', fontsize=14)
    axes[1, 1].set_xlabel('Ticket Médio (R$)')
    axes[1, 1].set_ylabel('')
    
    # CORREÇÃO: Margem de 20%
    max_val = df_plot['ticket_medio'].max()
    axes[1, 1].set_xlim(0, max_val * 1.2)

    for container in axes[1, 1].containers:
        axes[1, 1].bar_label(container, fmt=lambda x: f'R${x/1e3:.1f}K', padding=3)

    plt.tight_layout()
    plt.show()
    print("Dashboard gerado com sucesso!")

except Exception as e:
    print(f"Erro: {e}")