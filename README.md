# Projeto de Análise de Dados | BigQuery


## Automação de Consultas de COVID-19 com Python


## Sobre o Projeto


Este projeto foi desenvolvido durante a formação em Análise de Dados da EBAC, com o objetivo de automatizar consultas no Google BigQuery utilizando Python e trabalhar com os resultados por meio de DataFrames.


O desenvolvimento foi realizado no **Visual Studio Code**, onde foi configurado o ambiente Python e realizada a integração com o **Google BigQuery**, permitindo a execução das consultas SQL por meio do Python e o processamento dos dados com pandas. 


Para o projeto, foi utilizada uma base de dados de COVID-19 contendo informações sobre casos confirmados, mortes, países e evolução temporal dos registros. A base foi disponibilizada no BigQuery no projeto criado para o desenvolvimento da atividade.


O fluxo desenvolvido contempla a conexão com o BigQuery, execução das consultas, transformação dos resultados em DataFrames, tratamento e validação dos dados e exportação das bases processadas nos formatos **CSV e Parquet**.


## Objetivo


Automatizar consultas e o processamento de dados de COVID-19 utilizando Python e Google BigQuery, gerando bases estruturadas para análise e reutilização.


O projeto também busca demonstrar a integração entre SQL, Python, pandas e BigQuery, contemplando desde a configuração do ambiente e execução das consultas até o tratamento, validação e exportação dos resultados.


## Etapas Desenvolvidas


### 1. Configuração do Ambiente e Integração com o BigQuery


O ambiente de desenvolvimento foi configurado no **Visual Studio Code**, com a criação de um ambiente virtual Python e instalação das bibliotecas necessárias para o projeto.


Foi realizada a integração com o **Google BigQuery**, incluindo a autenticação no Google Cloud e a configuração do projeto utilizado para executar as consultas.


Após a configuração do ambiente, o script Python foi utilizado para estabelecer a conexão com o BigQuery e executar as consultas SQL diretamente pelo script.


### 2. Fonte e Exploração dos Dados


Foi utilizada uma base de dados de COVID-19 armazenada no BigQuery na tabela:


`projeto-ebac-bigquery.db_covid19.covid_19_geographic_distribution_worldwide`


A base reúne informações relacionadas à distribuição geográfica e temporal da COVID-19, incluindo registros de casos confirmados, mortes, países e população.


Entre os campos utilizados no projeto estão `date`, `daily_confirmed_cases`, `daily_deaths`, `confirmed_cases` e `countries_and_territories`.


Como etapa inicial de inspeção, foi realizada uma consulta de visualização com **10 registros** da tabela.


### 3. Desenvolvimento das Consultas SQL


Foram executadas **três consultas SQL** durante o pipeline:


1. Visualização inicial de registros da base;
2. Agregação dos dados para identificar os 20 países com maior número de casos confirmados;
3. Série temporal dos casos confirmados no Brasil.


A consulta de agregação reúne o total de casos confirmados, o total de mortes e a soma dos valores de casos confirmados por país. 


A consulta direcionada ao Brasil organiza os casos confirmados por data, permitindo obter uma série temporal da evolução dos registros.


Os resultados das consultas são convertidos automaticamente em DataFrames do pandas para processamento e validação.


### 4. Análise dos Resultados


A consulta agregada permitiu identificar os países com maiores totais de casos confirmados presentes na base.


Entre os primeiros resultados encontrados estão **Estados Unidos, Índia e Brasil**, que aparecem nas primeiras posições da agregação realizada pelo pipeline.


A análise específica do Brasil resultou em uma série temporal com **350 registros**, organizados cronologicamente, permitindo acompanhar os casos confirmados ao longo do período disponível na base.


Os resultados foram estruturados em DataFrames e preparados para exportação e utilização em análises posteriores.


### 5. Validação dos Dados


Os resultados processados foram validados considerando estrutura, tipos de dados, valores nulos, possíveis duplicidades e presença de dados nos DataFrames.


Foram verificadas:


- Colunas esperadas;
- Tipos de dados;
- Presença de valores nulos;
- Linhas duplicadas;
- Consistência dos DataFrames.


Na execução final, as duas bases processadas apresentaram **schema válido, ausência de valores nulos e 0 linhas duplicadas**.


Também foram aplicados procedimentos de padronização dos nomes das colunas e conversão dos tipos necessários antes da geração dos arquivos finais.


### 6. Conclusões


O projeto permitiu desenvolver um fluxo automatizado de consultas e processamento de dados utilizando Python integrado ao Google BigQuery.


A automação possibilitou executar consultas SQL, transformar os resultados em DataFrames, realizar procedimentos de tratamento e validação e gerar arquivos estruturados nos formatos CSV e Parquet.


A análise permitiu obter uma visão agregada dos países com maiores números de casos confirmados e construir uma série temporal específica para o Brasil.


De forma geral, o projeto demonstra a aplicação conjunta de **Python, SQL, pandas e Google BigQuery** na construção de um pipeline simples e organizado de processamento de dados.


## Habilidades Demonstradas


- Análise de Dados
- Python
- SQL
- Google BigQuery
- Google Cloud
- Visual Studio Code
- pandas
- Integração com BigQuery
- DataFrames
- Consultas SQL
- Agregação e Agrupamento de Dados
- Tratamento de Dados
- Padronização de Dados
- Validação de Dados
- Verificação de Valores Nulos
- Verificação de Duplicidades
- Análise Temporal
- Automação de Consultas
- Exportação em CSV
- Exportação em Parquet
- Documentação Técnica


## Arquivos do Projeto


Os principais arquivos do projeto estão organizados entre o script responsável pela automação e os dados utilizados e gerados durante o processamento.


### Script


🐍 **Script - Automação de Consultas de COVID-19**


` scripts/projeto_covid_bigquery.py `


Script desenvolvido no Visual Studio Code, contendo a conexão com o Google BigQuery, as consultas SQL, o processamento dos DataFrames, os procedimentos de validação e a exportação dos resultados.


### Dados


📊 **Dados do Projeto**


` data/ `


A pasta contém a base utilizada no projeto e os resultados processados das consultas, organizados entre `raw` e `ready`. Os resultados finais estão disponíveis nos formatos **CSV e Parquet**.