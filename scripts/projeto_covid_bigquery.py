"""
projeto_covid_bigquery.py

OBJETIVO GERAL
--------------
Este script automatiza consultas em uma base de dados de COVID-19 no BigQuery.
Ele executa três análises simples, transforma os resultados em tabelas (DataFrames)
e salva arquivos prontos para uso em Excel, Power BI ou análises futuras.

Fluxo resumido:
1. Conecta ao BigQuery
2. Executa 3 consultas SQL
3. Converte os resultados em DataFrames (tabelas)
4. Salva os resultados em arquivos
5. Se o BigQuery falhar, tenta usar um CSV local

DEPENDÊNCIAS
------------
- pandas: tratamento e manipulação dos DataFrames
- google-cloud-bigquery: conexão e execução de consultas no BigQuery
- db-dtypes: suporte à conversão de tipos do BigQuery para DataFrames pandas
- pyarrow: geração dos arquivos no formato Parquet

PARÂMETROS PRINCIPAIS
---------------------
- PROJECT_ID: projeto utilizado no Google Cloud
- TABLE: tabela consultada no BigQuery
- OUTPUT_DIR: pasta de destino dos arquivos processados
- LOCAL_CSV_FALLBACK: arquivo local utilizado caso o BigQuery não esteja disponível

REUTILIZAÇÃO
------------
As funções de conexão, execução de queries, padronização de colunas,
conversão de tipos e validação de DataFrames podem ser reutilizadas
em outros pipelines de dados com pequenas alterações nos parâmetros
e nas consultas SQL.
"""


# ======================
# IMPORTAÇÃO DE BIBLIOTECAS
# ======================

import os                 # Manipulação de pastas e caminhos no sistema
import logging            # Registro de mensagens (logs)
import pandas as pd       # Manipulação de dados em formato de tabela
from google.cloud import bigquery  # Conexão com o BigQuery

# ======================
# CONFIGURAÇÕES GERAIS
# ======================

# ID do projeto no BigQuery
PROJECT_ID = "projeto-ebac-bigquery"

# Tabela que será consultada no BigQuery
TABLE = "projeto-ebac-bigquery.db_covid19.covid_19_geographic_distribution_worldwide"

# Localização do dataset (pode ser None se não souber)
DATASET_LOCATION = None

# ======================
# CAMINHOS DE SAÍDA
# ======================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

OUTPUT_DIR = os.path.join(BASE_DIR, "data", "ready")

CSV_AGG = os.path.join(
    OUTPUT_DIR,
    "covid_agg_top20.csv"
)

PARQUET_AGG = os.path.join(
    OUTPUT_DIR,
    "covid_agg_top20.parquet"
)

CSV_TS = os.path.join(
    OUTPUT_DIR,
    "covid_timeseries_brazil.csv"
)

PARQUET_TS = os.path.join(
    OUTPUT_DIR,
    "covid_timeseries_brazil.parquet"
)

LOCAL_CSV_FALLBACK = os.path.join(
    BASE_DIR,
    "data",
    "raw",
    "db_covid19.csv"
)

# ======================
# CONFIGURAÇÃO DE LOGS
# ======================

# Define o formato e o nível das mensagens exibidas no terminal
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

# Cria um identificador para os logs deste script
logger = logging.getLogger("projeto_covid_bigquery")

# ======================
# FUNÇÃO: CRIAR CLIENTE DO BIGQUERY
# ======================

def create_bq_client(project_id: str):
    """
    Cria a conexão com o BigQuery usando o projeto informado.

    Se houver problema de autenticação ou permissão,
    o erro será registrado e o script será interrompido.
    """
    try:
        client = bigquery.Client(project=project_id)
        logger.info(
            "BigQuery client criado — project=%s cred_type=%s",
            client.project,
            type(client._credentials)
        )
        return client
    except Exception as e:
        logger.exception("Erro ao criar BigQuery client: %s", e)
        raise

# ======================
# FUNÇÃO: EXECUTAR QUERY SQL E RETORNAR DATAFRAME
# ======================

def run_query_to_df(client: bigquery.Client, sql: str, location: str = None) -> pd.DataFrame:
    """
    Executa uma query SQL no BigQuery e retorna o resultado
    como um DataFrame do pandas (tabela semelhante ao Excel).
    """
    logger.debug("Executando SQL: %s", sql.replace("\n", " ")[:500])

    # Executa a query (com ou sem localização)
    if location:
        job = client.query(sql, location=location)
    else:
        job = client.query(sql)

    # Aguarda a execução terminar e converte para DataFrame
    df = job.result().to_dataframe()
    return df

# ======================
# FUNÇÃO: GARANTIR COLUNAS NUMÉRICAS
# ======================

def ensure_int_columns(df: pd.DataFrame, cols):
    """
    Converte colunas informadas para números inteiros.
    Valores inválidos ou vazios viram zero.
    """
    for col in cols:
        if col in df.columns:
            df[col] = (
                pd.to_numeric(df[col], errors="coerce")
                .fillna(0)
                .astype("int64")
            )
    return df

def validate_dataframe(df: pd.DataFrame, expected_columns: list, name: str):
    """
    Executa validações mínimas no DataFrame:
    - verifica colunas esperadas;
    - exibe tipos de dados;
    - verifica valores nulos;
    - verifica se o DataFrame está vazio.
    """

    print(f"\n=== Validação: {name} ===")

    missing_columns = [
        col for col in expected_columns
        if col not in df.columns
    ]

    if missing_columns:
        print("Colunas ausentes:", missing_columns)
    else:
        print("Schema: OK")

    print("\nTipos:")
    print(df.dtypes)

    print("\nValores nulos:")
    print(df.isna().sum())
    
    print("\nLinhas duplicadas:")
    print(df.duplicated().sum())

    if df.empty:
        print("\nConsistência: DataFrame vazio")
    else:
        print("\nConsistência: DataFrame contém dados")

    print("============================\n")

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza os nomes das colunas:
    - remove espaços extras;
    - converte para minúsculas;
    - substitui espaços por underline.
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

# ======================
# FUNÇÃO PRINCIPAL
# ======================

def main():
    """
    Função principal do script.
    Controla todo o fluxo: consultas, tratamento e salvamento dos dados.
    """

    # Cria a pasta outputs se ela não existir
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    logger.info("Job iniciado")

    # Inicializa variáveis
    client = None
    df_preview = None
    df_agg = None
    df_ts = None

    try:
        # ======================
        # CONEXÃO COM BIGQUERY
        # ======================

        client = create_bq_client(PROJECT_ID)

        # ======================
        # QUERY 1 — PREVIEW DOS DADOS
        # ======================

        # Busca apenas 10 linhas para inspeção
        sql_preview = f"""
        SELECT *
        FROM `{TABLE}`
        LIMIT 10
        """

        df_preview = run_query_to_df(client, sql_preview, DATASET_LOCATION)
        logger.info("Query 1 executada — preview rows=%d", len(df_preview))
        print(df_preview.head())

        # ======================
        # QUERY 2 — AGREGAÇÃO POR PAÍS
        # ======================

        # Soma casos e mortes por país
        sql_agg = f"""
        SELECT
            countries_and_territories AS country_region,
            SUM(CAST(daily_confirmed_cases AS INT64)) AS total_confirmed,
            SUM(CAST(daily_deaths AS INT64)) AS total_deaths,
            SUM(CAST(confirmed_cases AS INT64)) AS total_confirmed_accumulated
        FROM `{TABLE}`
        GROUP BY country_region
        ORDER BY total_confirmed DESC
        LIMIT 20
        """

        df_agg = run_query_to_df(client, sql_agg, DATASET_LOCATION)
        df_agg = standardize_columns(df_agg)
        logger.info("Query 2 executada — agg rows=%d", len(df_agg))

        # Garante que colunas numéricas estejam corretas
        df_agg = ensure_int_columns(
            df_agg,
            ["total_confirmed", "total_deaths", "total_confirmed_accumulated"]
        )

        print(df_agg.head())

        validate_dataframe(
            df_agg,
            [
                  "country_region",
                  "total_confirmed",
                  "total_deaths",
                  "total_confirmed_accumulated"
            ],
            "Query 2 - Top 20 países"
        )

        # ======================
        # QUERY 3 — SÉRIE TEMPORAL DO BRASIL
        # ======================

        # Evolução diária de casos no Brasil
        sql_timeseries = f"""
        SELECT
            date,
            countries_and_territories AS country_region,
            SUM(CAST(daily_confirmed_cases AS INT64)) AS confirmed
        FROM `{TABLE}`
        WHERE countries_and_territories = 'Brazil'
        GROUP BY date, country_region
        ORDER BY date
        """

        df_ts = run_query_to_df(client, sql_timeseries, DATASET_LOCATION)
        df_ts = standardize_columns(df_ts)
        logger.info("Query 3 executada — timeseries rows=%d", len(df_ts))

        # Converte a coluna de data para formato correto
        df_ts["date"] = pd.to_datetime(df_ts["date"])
        print(df_ts.tail())

        validate_dataframe(
            df_ts,
            [
                 "date",
                 "country_region",
                 "confirmed"
            ],
            "Query 3 - Série temporal do Brasil"
        )

    except Exception as bq_err:
        # ======================
        # FALLBACK: CSV LOCAL
        # ======================

        logger.warning("Erro ao acessar BigQuery: %s", bq_err)

        if os.path.exists(LOCAL_CSV_FALLBACK):
            logger.info("Usando CSV local como alternativa")

            df_local = pd.read_csv(LOCAL_CSV_FALLBACK)
            df_local.to_csv(
                os.path.join(OUTPUT_DIR, "covid_local_copy.csv"),
                index=False
            )
        else:
            logger.error("Nenhum CSV local disponível. Abortando.")
            raise

    # ======================
    # SALVAMENTO DOS RESULTADOS
    # ======================

    if df_agg is not None and not df_agg.empty:
        df_agg.to_csv(CSV_AGG, index=False)
        df_agg.to_parquet(PARQUET_AGG, index=False)
        logger.info("Arquivos CSV e Parquet da agregação salvos")

    if df_ts is not None and not df_ts.empty:
        df_ts.to_csv(CSV_TS, index=False)
        df_ts.to_parquet(PARQUET_TS, index=False)
        logger.info("Arquivos CSV e Parquet da série temporal salvos")

    # ======================
    # FINALIZAÇÃO
    # ======================

    logger.info("Job finalizado com sucesso")

# ======================
# PONTO DE ENTRADA DO SCRIPT
# ======================

if __name__ == "__main__":
    main()
