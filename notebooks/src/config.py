from pathlib import Path


PASTA_PROJETO = Path(__file__).resolve().parents[2]

PASTA_DADOS = PASTA_PROJETO / "dados"

# coloque abaixo o caminho para os arquivos de dados de seu projeto
DADOS_ORIGINAIS = PASTA_DADOS / "Health Insurance.xlsx"
DADOS_TRATADOS = PASTA_DADOS / "Health Insurance.parquet"
DADOS_TRATADOS_CLUSTER = PASTA_DADOS / "Health Insurance Cluster.parquet"



# coloque abaixo o caminho para os arquivos de modelos de seu projeto
PASTA_MODELOS = PASTA_PROJETO / "modelos"
MODELO_FINAL = PASTA_MODELOS / "liner_regression.joblib"
MODELO_CLUSTER= PASTA_MODELOS / "CLUSTER.joblib"




# coloque abaixo outros caminhos que você julgar necessário
PASTA_RELATORIOS = PASTA_PROJETO / "relatorios"
PASTA_IMAGENS = PASTA_RELATORIOS / "imagens"
