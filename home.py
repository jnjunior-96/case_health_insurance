import numpy as np
import pandas as pd
import streamlit as st

from joblib import load

# from notebooks.src.config import DADOS_TRATADOS_CLUSTER, MODELO_FINAL, MODELO_CLUSTER

DADOS_TRATADOS_CLUSTER = "dados/Health Insurance Cluster.parquet"
MODELO_CLUSTER = "modelos/CLUSTER.joblib"
MODELO_FINAL = "modelos/liner_regression.joblib"

@st.cache_data
def carregar_dados_limpos():
    return pd.read_parquet(DADOS_TRATADOS_CLUSTER)

@st.cache_resource
def carregar_modelo_cluster():
    return load(MODELO_CLUSTER)

@st.cache_resource
def carregar_modelo():
    return load(MODELO_FINAL)

df = carregar_dados_limpos()
modelo_cluster = carregar_modelo_cluster()
modelo = carregar_modelo()

st.title("Previsão de cobrança. :hospital:")
st.header("Health Insurance", divider="gray")

genero = sorted(list(df["gender"].unique()))
desconto = sorted(list(df["discount_eligibility"].unique()))
regiao = sorted(list(df["region"].unique()))



with st.form(key="formulario"):
    selecionar_genero = st.selectbox("Genero", genero)
    idade = st.number_input("Idade", value=30, min_value=18, max_value=150)
    bmi = st.number_input("IMC", value=30, min_value=1, max_value=60)
    filhos = st.number_input("Filhos", value=0, min_value=0, max_value=20)
    selecionar_desconto = st.selectbox("Desconto", desconto)
    selecionar_regiao = st.selectbox("Região", regiao)

    entrada_cluster = {
        "gender": selecionar_genero,
        "discount_eligibility": selecionar_desconto,
        "region": selecionar_regiao,
        "age": idade,
        "bmi": bmi,
        "children": filhos,
    }

    df_entrada_cluster = pd.DataFrame(entrada_cluster, index=[0])
    cluster = modelo_cluster.predict(df_entrada_cluster)

    entrada_modelo = {
        "gender": selecionar_genero,
        "discount_eligibility": selecionar_desconto,
        "region": selecionar_regiao,
        "age": idade,
        "bmi": bmi,
        "children": filhos,
        "cluster": cluster
    }

    margem_desejada = {
        0: 0.25,
        1: 0.25,
        2: 0.20,
        3: 0.25
    }


    df_entrada_modelo = pd.DataFrame(entrada_modelo, index=[0])

    df_entrada_modelo["margem_desejada"] = df_entrada_modelo["cluster"].map(
    margem_desejada
    )


    botao_previsao_modelo = st.form_submit_button("Prever Modelo")
    # st.metric(label="Margem: ", value= f"Margem: {df_entrada_modelo['margem_desejada'][0]}")

if botao_previsao_modelo:
    modelo_gastos = modelo.predict(df_entrada_modelo)
    modelo_cobrar = modelo_gastos / (1 - df_entrada_modelo["margem_desejada"][0])

    st.metric(label="Previsão de Gastos: ", value= f"Previsão de Gastos: R$ {modelo_gastos[0][0]:,.2f}")
    st.metric(label="Cobrar: ", value= f"Cobrar: R$ {modelo_cobrar[0][0]:,.2f}")
    st.metric(label="Lucro: ", value= f"Lucro: R$ {modelo_cobrar[0][0] - modelo_gastos[0][0]:,.2f}")
    st.metric(label="Margem: ", value= f"Margem: {df_entrada_modelo['margem_desejada'][0]:,.1%}")

