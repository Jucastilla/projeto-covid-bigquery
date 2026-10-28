# Análise de Dados da COVID-19

## Contexto

Este projeto foi desenvolvido durante a formação em **Análise de Dados da EBAC**, a partir de uma atividade de automação de consultas no **Google BigQuery** utilizando **Python**.

Foi utilizada uma base de COVID-19 com informações sobre casos confirmados, mortes, países, população e evolução temporal dos registros, disponibilizada no BigQuery no projeto criado para a atividade.

O desenvolvimento foi realizado no **Visual Studio Code**, com configuração do ambiente Python e integração com o BigQuery. O **pandas** foi utilizado para trabalhar com os resultados das consultas em DataFrames.

## Objetivo

Automatizar a execução de consultas SQL e o processamento de dados de COVID-19 utilizando Python e Google BigQuery, gerando bases estruturadas para análise e reutilização.

O projeto também teve como objetivo integrar SQL, Python e pandas em um fluxo de consulta, tratamento, validação e exportação de dados nos formatos **CSV e Parquet**.

## Desenvolvimento

### Configuração do Ambiente e Integração

O ambiente foi configurado no **Visual Studio Code**, com criação de um ambiente virtual Python e instalação das bibliotecas necessárias.

A integração com o **Google BigQuery** incluiu a autenticação no Google Cloud e a configuração do projeto utilizado nas consultas.

Após essa configuração, o script Python foi utilizado para estabelecer a conexão e executar as consultas SQL no BigQuery.

### Fonte e Inspeção dos Dados

Foi utilizada a tabela:

`projeto-ebac-bigquery.db_covid19.covid_19_geographic_distribution_worldwide`

Entre os campos utilizados estão:

- `date`;
- `daily_confirmed_cases`;
- `daily_deaths`;
- `confirmed_cases`;
- `countries_and_territories`.

A inspeção inicial foi realizada por meio de uma consulta com **10 registros**, permitindo visualizar os dados disponíveis na tabela.

### Desenvolvimento das Consultas SQL

Foram executadas **três consultas** durante o fluxo de processamento:

1. Visualização inicial de registros da base;
2. Agregação dos dados para identificar os 20 países com maior número de casos confirmados;
3. Construção de uma série temporal dos casos confirmados no Brasil.

A consulta por país reuniu totais de casos confirmados, mortes e a soma dos valores de casos confirmados.

A consulta específica do Brasil organizou os registros por data para acompanhar a evolução dos casos no período disponível.

### Processamento com pandas

Os resultados das consultas foram convertidos automaticamente em **DataFrames do pandas**.

Antes da exportação, foram realizados procedimentos de:

- Padronização dos nomes das colunas;
- Conversão dos tipos de dados necessários;
- Organização cronológica da série temporal do Brasil;
- Preparação das bases para validação e exportação.

### Validação dos Dados

Foram realizadas verificações sobre:

- Presença de dados nos DataFrames;
- Colunas esperadas;
- Tipos de dados;
- Valores nulos;
- Linhas duplicadas;
- Consistência da estrutura dos DataFrames.

### Exportação dos Resultados

As bases processadas foram exportadas nos formatos **CSV e Parquet**, permitindo sua utilização em análises posteriores.

Os dados do projeto foram organizados entre as pastas `raw` e `ready`.

## Resultados

### Agregação por País

Foi gerada uma base com os **20 países com maior número de casos confirmados**, conforme a agregação realizada sobre os dados disponíveis.

**Estados Unidos, Índia e Brasil** apareceram entre as primeiras posições do resultado.

### Série Temporal do Brasil

A consulta específica do Brasil gerou uma série temporal com **350 registros**, organizados cronologicamente para acompanhar os casos confirmados ao longo do período disponível na base.

### Qualidade das Bases Processadas

Na execução final, as duas bases processadas apresentaram:

- Schema válido;
- Ausência de valores nulos;
- **0 linhas duplicadas**.

### Entregas do Projeto

O projeto resultou em um script que integra a conexão com o BigQuery, a execução de consultas SQL, o processamento em DataFrames, a validação e a exportação dos resultados.

Foram geradas bases estruturadas em **CSV e Parquet**, contendo a agregação por país e a série temporal do Brasil.

O desenvolvimento permitiu aplicar **Python, SQL, pandas e Google BigQuery** em um pipeline de processamento de dados.

## Habilidades Demonstradas

- Análise de dados;
- Python;
- SQL;
- Google BigQuery;
- Google Cloud;
- Visual Studio Code;
- pandas;
- Integração com BigQuery;
- DataFrames;
- Consultas SQL;
- Agregação e agrupamento de dados;
- Tratamento de dados;
- Padronização de dados;
- Validação de dados;
- Verificação de valores nulos;
- Verificação de duplicidades;
- Análise temporal;
- Automação de consultas;
- Exportação em CSV;
- Exportação em Parquet;
- Documentação técnica.

## Arquivos do Projeto

Os arquivos estão organizados entre o script de automação e os dados utilizados e gerados durante o processamento.

### [Script — Automação de Consultas de COVID-19](https://github.com/Jucastilla/projeto-covid-bigquery/blob/main/scripts/projeto_covid_bigquery.py)

Script desenvolvido no Visual Studio Code, contendo a conexão com o Google BigQuery, as consultas SQL, o processamento dos DataFrames, os procedimentos de validação e a exportação dos resultados.

### [Dados do Projeto](https://github.com/Jucastilla/projeto-covid-bigquery/tree/main/data)

Pasta contendo a base utilizada e os resultados processados, organizados entre `raw` e `ready`.

Os resultados finais estão disponíveis nos formatos **CSV e Parquet**.
