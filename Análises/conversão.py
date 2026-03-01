import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
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
    t2.nome AS vendedor,
    COUNT(t1.sk_evento) AS total_negociacoes,
    SUM(CASE WHEN t1.status = 'Confirmado' THEN 1 ELSE 0 END) AS contratos_fechados,
    SUM(CASE WHEN t1.status = 'Cancelado' THEN 1 ELSE 0 END) AS contratos_cancelados,
    (
        SUM(CASE WHEN t1.status = 'Confirmado' THEN 1 ELSE 0 END)::numeric /
        NULLIF(SUM(CASE WHEN t1.status IN ('Confirmado', 'Cancelado') THEN 1 ELSE 0 END), 0)::numeric
    ) * 100 AS taxa_conversao_percentual
FROM
    fato_evento AS t1
JOIN
    dim_vendedor AS t2 ON t1.fk_vendedor = t2.id_vendedor
WHERE 
    t1.status IN ('Confirmado', 'Cancelado')
GROUP BY
    t2.nome
ORDER BY
    taxa_conversao_percentual DESC;
"""

# ------------------------------------------------------------------------
# 3. GERAR GRÁFICO COMBINADO (BARRAS + LINHA)
# ------------------------------------------------------------------------
try:
    df = pd.read_sql(query, engine)
    
    # Filtrar Top 10 ou 15 para não poluir o visual
    df = df.head(12)

    fig, ax1 = plt.subplots(figsize=(14, 7))

    # --- EIXO 1 (Esquerda): Volume de Contratos (Barras Empilhadas) ---
    # Barra de baixo (Fechados - Verde Sucesso)
    p1 = ax1.bar(df['vendedor'], df['contratos_fechados'], label='Fechados', color='#2ca02c', alpha=0.8)
    
    # Barra de cima (Cancelados - Vermelho Alerta)
    # O parametro 'bottom' faz o empilhamento
    p2 = ax1.bar(df['vendedor'], df['contratos_cancelados'], bottom=df['contratos_fechados'], label='Cancelados', color='#d62728', alpha=0.8)

    ax1.set_xlabel('Vendedor', fontsize=12)
    ax1.set_ylabel('Quantidade de Negociações', fontsize=12)
    
    # --- EIXO 2 (Direita): Taxa de Conversão (Linha) ---
    ax2 = ax1.twinx()
    
    # Linha preta ou azul escura para destacar a métrica de eficiência
    line = ax2.plot(df['vendedor'], df['taxa_conversao_percentual'], color='black', marker='o', linewidth=2, linestyle='-', label='Taxa de Conversão (%)')
    
    ax2.set_ylabel('Conversão (%)', fontsize=12, color='black')
    ax2.tick_params(axis='y', labelcolor='black')
    
    # Define limite do eixo Y da porcentagem (ex: até 110% para dar respiro)
    ax2.set_ylim(0, 110)

    # Rótulos nas bolinhas da linha (Porcentagem)
    for i, txt in enumerate(df['taxa_conversao_percentual']):
        ax2.annotate(f'{txt:.1f}%', 
                     (i, txt), 
                     textcoords="offset points", 
                     xytext=(0,10), 
                     ha='center', 
                     fontweight='bold')

    # Legenda Combinada (Barras + Linha)
    # Precisamos juntar as legendas dos dois eixos manualmente
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')

    # Ajustes finais
    plt.xticks(rotation=45, ha='right')
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.show()
    print("Gráfico de conversão gerado com sucesso!")

except Exception as e:
    print(f"Erro: {e}")