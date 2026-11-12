# Projeto de Big Data — Gestão de Vendas e Previsão de Demanda para a Casa de Festas Ilha Mágica (ULABUM)

Projeto Integrador (3º e 4º semestres) — FATEC Ipiranga "Pastor Enéas Tognini"

## Problema

A Casa de Festas Ilha Mágica (nome fantasia ULABUM), buffet infantil e de eventos escolares localizado em Santo André (SP), enfrentava dois problemas que afetam diretamente a margem de lucro:

- **Falta de gestão de vendas:** sem um controle estruturado do processo comercial (do primeiro contato ao pós-venda), a empresa sofria com vendas perdidas e desqualificadas, falhas de follow-up e dificuldade de fidelizar clientes.
- **Falta de antecipação de tendências e sazonalidade:** as decisões eram baseadas em percepções empíricas, deixando a empresa mal preparada para mudanças no comportamento dos consumidores e para períodos de maior ou menor demanda.

**Solução proposta:** um sistema de acompanhamento e análise de vendas (Data Warehouse com ETL, estatística inferencial e redes neurais) somado a uma plataforma de inteligência de dados para análise de tendências e sazonalidade (Data Lake com ELT, estatística descritiva e Machine Learning), com dashboards para apoiar a decisão dos gestores.

## Dados

**Origem:**
- Dados internos de eventos, clientes e vendas da empresa, organizados em um Data Warehouse no PostgreSQL (tabela `fato_evento` e tabela `evento`) e em planilha Excel (`PlanilhaDeEventos.xlsx`).
- Dados externos de tendências de busca do setor de eventos (Google Trends), consolidados no arquivo `eventos_unificados.csv` e armazenados no MongoDB (banco `PI4`, coleção `tendencia_eventos`).
- Dados financeiros de uma empresa similar do mesmo setor (ano de 2024), usados como referência para a análise financeira.

**Descrição:**
- **Eventos (Data Warehouse):** faturamento, quantidade de adultos, quantidade de crianças, total de pessoas, dias entre a contratação e o evento (`dias_para_evento`) e status do evento (ex.: "Tornou-se cliente"), além de valor e custo do evento.
- **Tendências (série temporal):** documentos com `data`, `tipo_evento` e `valor` (índice de interesse de busca, de 0 a 100) para 7 tipos de evento: casamento, festa infantil, formatura, festa de adulto, festa de 15 anos, chá revelação e festa corporativa. São 1.715 registros, com 245 meses analisados por tipo de evento.
- **Financeiro (2024):** faturamento, lucro, custos, contratos fechados, pendentes e cancelados.

## Tecnologias

- Python (Pandas, NumPy, SciPy, Scikit-learn, Matplotlib, Seaborn, SQLAlchemy, PyMongo)
- R (readxl, DBI, RPostgres, moments)
- SQL / PostgreSQL (stored procedure com cursor dinâmico e trigger em PL/pgSQL)
- MongoDB (MongoDB Atlas / Compass)
- Azure Data Lake Storage Gen2 e Azure Data Factory
- Databricks / PySpark (processamento e catálogo de metadados)
- Power BI
- Google Colab
- GitHub

## Metodologias

- **CRISP-DM** (principal): o ciclo de vida dos dois projetos se alinha às fases dessa metodologia, que organiza o trabalho de mineração de dados em etapas iterativas:
  - *Entendimento do negócio:* levantamento do problema da Casa de Festas Ilha Mágica (falta de gestão de vendas e de antecipação de tendências), dos objetivos e dos requisitos, apoiado pelas análises PESTEL, Cinco Forças de Porter e SWOT.
  - *Entendimento dos dados:* análise exploratória das bases de eventos (PostgreSQL e Excel) e de tendências de busca (Google Trends / MongoDB), com medidas de tendência central, dispersão, forma da distribuição, histogramas, boxplots e QQ-plots.
  - *Preparação dos dados:* ETL para o Data Warehouse, ELT para o Data Lake (camadas Bronze, Silver e Gold), limpeza, padronização e engenharia de atributos (ano, mês e componentes de sazonalidade).
  - *Modelagem:* regressão linear, rede neural (MLPRegressor), Regressão Linear Múltipla e Random Forest para prever faturamento e demanda.
  - *Avaliação:* métricas como R², MAE, RMSE e MAPE, além de relatório de classificação e matriz de confusão, comparando valores reais e previstos.
  - *Implantação:* dashboards no Power BI, stored procedure e trigger no banco de dados para apoiar a decisão dos gestores.
- **Scrum**: a construção do sistema seria conduzida em Sprints curtas, com entregas incrementais alinhadas às prioridades da empresa (por exemplo: Data Warehouse e ETL, modelos preditivos, dashboards). As reuniões semanais de acompanhamento do plano de riscos e do controle de mudanças funcionariam como as cerimônias de revisão e planejamento, mantendo o escopo e o cronograma sob controle.

## Pipeline

Coleta → Limpeza → Transformação → Análise → Visualização

- **Coleta:** dados internos (PostgreSQL, Excel) e externos (Google Trends via API, CSV), com ingestão em MongoDB e envio ao Azure Data Lake via Python e Azure Data Factory.
- **Limpeza:** padronização, tipagem e resolução de inconsistências (camada Silver), além de filtros de qualidade nas consultas (ex.: faturamento > 0).
- **Transformação:** ETL para o Data Warehouse (modelo dimensões + fato), ELT no Data Lake e engenharia de atributos (ano, mês e transformação senoidal/cossenoidal para capturar a sazonalidade).
- **Análise:** estatística descritiva e inferencial, regressão linear (Python e R), rede neural (MLPRegressor), Regressão Linear Múltipla e Random Forest para previsão de demanda.
- **Visualização:** histogramas, boxplots, QQ-plots, gráficos de valores reais vs. previstos, matriz de confusão e dashboards no Power BI (camada Gold).

## Resultados

**Análise financeira (referência 2024):**
- Faturamento anual de R$ 350.900,00, lucro de aproximadamente R$ 140.000,00 e margem de lucro de 40%.
- 33 contratos fechados, ticket médio de cerca de R$ 10.633,00, taxa de conversão de aproximadamente 73% e taxa de cancelamento de 13%.

**Análise estatística das tendências:**
- Média de 36,07, mediana de 35 e desvio padrão de 24,93 (coeficiente de variação de 69,10%), indicando alta dispersão.
- Distribuição assimétrica positiva (assimetria de 0,27) e platicúrtica (curtose de 2,31).
- Casamento é o evento com maior tendência média (57,26), seguido por festa infantil (46,02) e formatura (43,69). Festa corporativa apresenta a menor média (7,16).

**Modelos preditivos:**
- Regressão linear (Python e R) e rede neural MLPRegressor (2 camadas ocultas de 10 neurônios) para prever o faturamento dos eventos a partir de adultos, crianças e antecedência da contratação, avaliados por R², RMSE, MAE e MAPE.
- Regressão Linear Múltipla e Random Forest (regressão e classificação de demanda "Alta"/"Baixa") para prever a sazonalidade por tipo de evento.

**Banco de dados:**
- Stored procedure `sp_calcula_lucro_total`, que calcula o lucro total dos eventos que se tornaram clientes usando cursor dinâmico, e trigger que confirma automaticamente o cadastro de novos eventos.
- Operações CRUD no MongoDB e rotina automatizada de estatísticas por tipo de evento.

## Insights

- Centralizar o processo comercial em um sistema integrado (CRM, propostas, contratos, agenda e financeiro) reduz falhas de comunicação, vendas perdidas e retrabalho entre os times comercial, financeiro, contabilidade e compras.
- Prever o faturamento a partir de variáveis operacionais (número de adultos, crianças e antecedência) dá previsibilidade para ajustar preços e pacotes.
- Conhecer a sazonalidade e as tendências de cada tipo de evento permite direcionar marketing, dimensionar equipes, negociar antecipadamente com fornecedores e organizar a agenda, substituindo decisões empíricas por decisões orientadas a dados.
- A arquitetura ELT com Data Lake em camadas oferece flexibilidade e escalabilidade para integrar novas fontes de dados conforme a empresa cresce.
- Como próximos passos, recomenda-se ampliar as fontes de dados, refinar os modelos preditivos e automatizar totalmente o pipeline.

## Como executar

1. Clone o repositório:
   ```bash
   git clone https://github.com/ProjetoIntegrador20253/Projeto.git
   cd Projeto
   ```
2. Instale as dependências Python:
   ```bash
   pip install pandas numpy scipy scikit-learn matplotlib seaborn sqlalchemy psycopg2-binary python-dotenv pymongo dnspython azure-storage-file-datalake
   ```
3. Para os scripts em R, instale os pacotes necessários:
   ```r
   install.packages(c("readxl", "DBI", "RPostgres", "dotenv", "moments"))
   ```
4. Crie um arquivo `.env` na raiz do projeto com as credenciais do PostgreSQL (não envie esse arquivo ao GitHub):
   ```env
   DB_USER=seu_usuario
   DB_PASSWORD=sua_senha
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=nome_do_banco
   ```
5. Ajuste os caminhos das bases (`PlanilhaDeEventos.xlsx` e `eventos_unificados.csv`) nos scripts para o local onde você salvou os arquivos.
6. Execute os scripts Python (`python nome_do_script.py`) ou abra os notebooks no Google Colab. Para o MongoDB, é necessário ter uma instância local ou no Atlas em execução. Para o envio ao Azure Data Lake, configure as credenciais da conta de armazenamento como variáveis de ambiente.
7. As stored procedures e triggers (SQL) devem ser executadas no PostgreSQL, por exemplo pelo pgAdmin, antes de rodar `CALL sp_calcula_lucro_total();`.

## Integrantes

| Nome | RA |
|------|----|
| Felipe Chicarolli dos Santos | 2041382421024 |
| Felipe Hideki Rodrigues Shinozaki | 2041382421018 |
| Gustavo Marques de Assis Santos | 2041382421028 |
| Jefferson de Carvalho Quintilhano | 2041382421032 |
| Rayssa Pinheiro de Freitas Santos | 2041382421036 |
| Vanessa Batista Ribeiro | 2041382421006 |