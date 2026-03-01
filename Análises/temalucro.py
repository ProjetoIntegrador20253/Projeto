import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

# ------------------------------------------------------------------------
# 1. CONEXÃO (Lembre-se de usar os seus dados reais aqui)
# ------------------------------------------------------------------------
connection_string = 'postgresql://postgres:123456@localhost:5432/projetoint3'
engine = create_engine(connection_string)

# ------------------------------------------------------------------------
# 2. QUERY
# ------------------------------------------------------------------------
query = """
SELECT
    COALESCE(t2.tema, 'Não Atribuído') AS tema,
    SUM(t1.lucro_total) AS lucro_total_por_tema
FROM
    fato_evento AS t1
LEFT JOIN 
    dim_tema AS t2 ON t1.fk_tema = t2.id_tema
WHERE
    t1.status = 'Confirmado'
GROUP BY
    t2.tema
ORDER BY
    lucro_total_por_tema DESC;
"""

# ------------------------------------------------------------------------
# 3. GERAR GRÁFICO DE BARRAS SIMPLES
# ------------------------------------------------------------------------
try:
    df = pd.read_sql(query, engine)
    
    fig, ax = plt.subplots(figsize=(12, 6))

    # Apenas o gráfico de barras agora
    # Usei 'zorder=3' para garantir que as barras fiquem na frente das linhas de grade
    bars = ax.bar(df['tema'], df['lucro_total_por_tema'], color='#1f77b4', alpha=0.8, zorder=3)
    
    # Configurações do Eixo
    ax.set_xlabel('Tema', fontsize=12)
    ax.set_ylabel('Lucro Total (R$)', fontsize=12)

    
    # Adicionando linhas de grade (grid) no fundo para facilitar a leitura de valores
    ax.grid(axis='y', linestyle='--', alpha=0.7, zorder=0)

    # Formatando o eixo Y para não usar notação científica (opcional, mas bom para dinheiro)
    ax.ticklabel_format(style='plain', axis='y')

    # Rótulos de valor nas barras
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                 f'R${height:,.0f}',
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.xticks(rotation=45, ha='right')
    fig.tight_layout()
    
    plt.show()
    print("Gráfico de barras gerado com sucesso!")

except Exception as e:
    print(f"Erro: {e}")