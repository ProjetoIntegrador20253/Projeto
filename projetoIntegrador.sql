DROP TABLE vendedor;
CREATE TABLE vendedor(
	id_vendedor SERIAL PRIMARY KEY,
	nome VARCHAR(100) NOT NULL,
	email VARCHAR(100) NOT NULL,
	telefone VARCHAR(11) NOT NULL
);

INSERT INTO vendedor (nome, email, telefone) VALUES
('Ana Martins', 'ana.martins@ulabum.com', '11987654321'),
('Bruno Oliveira', 'bruno.oliveira@ulabum.com', '11965432109'),
('Carla Souza', 'carla.souza@ulabum.com', '11991234567'),
('Daniel Lima', 'daniel.lima@ulabum.com', '11977889900'),
('Eduardo Santos', 'eduardo.santos@ulabum.com', '11999887766'),
('Fernanda Costa', 'fernanda.costa@ulabum.com', '11988776655'),
('Gabriel Pereira', 'gabriel.pereira@ulabum.com', '11990011223'),
('Helena Alves', 'helena.alves@ulabum.com', '11993334444'),
('Igor Fernandes', 'igor.fernandes@ulabum.com', '11995556677'),
('Julia Ramos', 'julia.ramos@ulabum.com', '11997778899');

SELECT * FROM vendedor;


DROP TABLE prospect;
CREATE TABLE prospect(
	id_prospect SERIAL PRIMARY KEY,
	nome VARCHAR(100) NOT NULL,
	data_nasc DATE,
	sexo VARCHAR(3),
	telefone VARCHAR(11) NOT NULL,
	email VARCHAR(100) NOT NULL,
	profissao VARCHAR(100),
	endereço VARCHAR(100),
	marketing VARCHAR(100)
);

INSERT INTO prospect (nome, data_nasc, sexo, telefone, email, profissao, endereço, marketing) VALUES
('Ana Martins', '1990-05-12', 'F', '11987654321', 'ana.martins@email.com', 'Advogada', 'Rua das Flores, 123', 'ABC DAS MÃES'),
('Bruno Oliveira', '1985-08-23', 'M', '11965432109', 'bruno.oliveira@email.com', 'Engenheiro', 'Av. Paulista, 456', 'CONVIDADO'),
('Carla Souza', '1992-11-05', 'F', '11991234567', 'carla.souza@email.com', 'Médica', 'Rua Bela Vista, 78', 'FACEBOOK'),
('Daniel Lima', '1988-02-17', 'M', '11977889900', 'daniel.lima@email.com', 'Analista', 'Rua das Laranjeiras, 99', 'FAIXADA'),
('Eduardo Santos', '1995-07-30', 'M', '11999887766', 'eduardo.santos@email.com', 'Professor', 'Av. Brasil, 321', 'GOOGLE'),
('Fernanda Costa', '1991-09-14', 'F', '11988776655', 'fernanda.costa@email.com', 'Designer', 'Rua das Acácias, 12', 'INDICAÇÃO'),
('Gabriel Pereira', '1987-12-01', 'M', '11990011223', 'gabriel.pereira@email.com', 'Contador', 'Rua Nova, 55', 'INSTAGRAM'),
('Helena Alves', '1993-04-20', 'F', '11993334444', 'helena.alves@email.com', 'Psicóloga', 'Av. Santos Dumont, 100', 'SITE'),
('Igor Fernandes', '1990-10-10', 'M', '11995556677', 'igor.fernandes@email.com', 'Programador', 'Rua da Harmonia, 77', 'INDICAÇÃO'),
('Julia Ramos', '1994-01-25', 'F', '11997778899', 'julia.ramos@email.com', 'Jornalista', 'Rua Primavera, 88', 'ABC DAS MÃES');

SELECT * FROM prospect;


DROP TABLE cardapio;
CREATE TABLE cardapio(
	id_cardapio SERIAL PRIMARY KEY,
	tipo VARCHAR(50) NOT NULL
);

INSERT INTO cardapio (tipo) VALUES
('Ouro'),
('Prata'),
('Bronze'),
('Escolar');

SELECT * FROM cardapio;


CREATE TABLE tema(
	id_tema SERIAL PRIMARY KEY,
	nome_tema VARCHAR(100) NOT NULL
);

INSERT INTO tema (nome_tema) VALUES
('Homem-Aranha'),
('Unicórnio'),
('Moana'),
('Cinderela'),
('Batman'),
('Superman'),
('Galinha Pintadinha'),
('Mundo Bita'),
('Mundo dos Sonhos'),
('Circo Vintage');


DROP TABLE evento;
CREATE TABLE evento(
	id_evento SERIAL PRIMARY KEY,
	tipo VARCHAR(50) NOT NULL,
	primeiro_contato DATE NOT NULL,
	data_interesse DATE NOT NULL,
	horario_interesse TIME NOT NULL,
	qtd_adultos INT NOT NULL,
	qtd_criancas INT NOT NULL,
	duracao TIME NOT NULL,
	status VARCHAR(50) NOT NULL,
	valor NUMERIC(10,2),
	pagamento VARCHAR(50),
	custo_evento NUMERIC(10, 2),
	fk_prospect INT NOT NULL,
	fk_vendedor INT NOT NULL,
	fk_cardapio INT,
	fk_tema INT,

	FOREIGN KEY (fk_prospect) REFERENCES prospect(id_prospect),
	FOREIGN KEY (fk_vendedor) REFERENCES vendedor(id_vendedor),
	FOREIGN KEY (fk_cardapio) REFERENCES cardapio(id_cardapio),
	FOREIGN KEY (fk_tema) REFERENCES tema(id_tema)
);

-- Exemplo de inserção de desistencia
INSERT INTO evento (tipo, primeiro_contato, data_interesse, horario_interesse, qtd_adultos, qtd_criancas, duracao, status, fk_prospect, fk_vendedor) VALUES
('Aniversário infantil', '2018-03-15', '2018-07-20', '18:00', 28, 37, '05:00', 'Desistência', 8, 3),
('Aniversário de 15 anos', '2019-07-20', '2019-10-17', '18:00', 50, 20, '05:00', 'Desistência', 2, 9),
('Aniversário de adulto', '2020-04-07', '2020-08-09', '19:00', 34, 39, '04:00', 'Desistência', 1, 5),
('Formatura', '2023-05-10', '2023-12-08', '19:00', 102, 74, '05:00', 'Desistência', 4, 1),
('Chá revelação', '2024-10-05', '2025-01-24', '15:00', 26, 35, '04:00', 'Desistência', 9, 2),
('Casamento', '2021-01-28', '2022-06-22', '17:00', 52, 39, '05:00', 'Desistência', 3, 7);

SELECT * FROM evento;

-- Exemplo de inserção de quanto a festa acontece

INSERT INTO evento (tipo, primeiro_contato, data_interesse, horario_interesse, qtd_adultos, qtd_criancas, duracao, status, valor, pagamento, custo_evento, fk_prospect, fk_vendedor, fk_cardapio) VALUES
('Aniversário infantil', '2025-08-27', '2025-11-15', '16:00', 31, 42, '04:00', 'Tornou-se cliente', 450.00, 'Pix', 300.00, 10, 4, 3),
('Aniversário de 15 anos', '2024-02-20', '2024-05-13', '18:00', 50, 20, '05:00', 'Tornou-se cliente', 475.00, 'Cartão de crédito', 325.00, 5, 10, 1),
('Aniversário de adulto', '2023-11-22', '2024-02-21', '17:00', 43, 41, '04:00', 'Tornou-se cliente', 390.00, 'Cartão de débito', 260.00, 6, 8, 2),
('Formatura', '2025-04-28', '2025-12-15', '18:00', 110, 83, '05:00', 'Tornou-se cliente', 14350.00, 'Pix', 870.00, 7, 6, 1);

-- Exemplo de quando está em negociação
INSERT INTO evento (tipo, primeiro_contato, data_interesse, horario_interesse, qtd_adultos, qtd_criancas, duracao, status, valor, pagamento, custo_evento, fk_prospect, fk_vendedor, fk_cardapio) VALUES
('Aniversário de 15 anos', '2025-07-18', '2025-12-19', '18:00', 49, 45, '05:00', 'Em negociação', 425.00, NULL, 300.00, 8, 7, 1);