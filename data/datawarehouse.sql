-- Dimensao tempo
DROP TABLE dim_tempo;
CREATE TABLE dim_tempo (
  id_tempo SERIAL PRIMARY KEY,
  data DATE UNIQUE,
  ano INT,
  mes INT,
  dia_mes INT
);

-- Dimensao prospect
DROP TABLE dim_prospect;
CREATE TABLE dim_prospect (
  id_prospect INT PRIMARY KEY,
  nome VARCHAR(100),
  idade INT,
  sexo VARCHAR(6),
  profissao VARCHAR(100),
  marketing_channel VARCHAR(100)
);

-- Dimensao vendedor
DROP TABLE dim_vendedor;
CREATE TABLE dim_vendedor (
  id_vendedor INT PRIMARY KEY,
  nome VARCHAR(100),
  email VARCHAR(100),
  telefone VARCHAR(20)
);

-- Dimensao cardapio
DROP TABLE dim_cardapio;
CREATE TABLE dim_cardapio (
  id_cardapio INT PRIMARY KEY,
  tipo VARCHAR(50)
);

-- Dimensao tema
DROP TABLE dim_tema;
CREATE TABLE dim_tema(
	id_tema INT PRIMARY KEY,
	tema VARCHAR(100)
)

-- Fato evento
DROP TABLE fato_evento;
CREATE TABLE fato_evento (
  sk_evento INT PRIMARY KEY,
  fk_tempo INT REFERENCES dim_tempo(id_tempo),
  fk_prospect INT REFERENCES dim_prospect(id_prospect),
  fk_vendedor INT REFERENCES dim_vendedor(id_vendedor),
  fk_cardapio INT REFERENCES dim_cardapio(id_cardapio),
  fk_tema INT REFERENCES dim_tema(id_tema),
  data_interesse DATE,
  tipo_evento VARCHAR(50),
  duracao_horas TIME,
  status VARCHAR(50),
  qtd_adultos INT,
  qtd_criancas INT,
  faturamento NUMERIC(10,2),
  custo NUMERIC(10,2),
  dias_para_evento INT,
  total_pessoas INT,
  lucro_total NUMERIC(10,2)
);