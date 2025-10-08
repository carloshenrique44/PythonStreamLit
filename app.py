import streamlit as st
from dataset import df 
import plotly.express as px

st.set_page_config(page_title="Dashboard Financeiro", layout="wide", page_icon="💸")
st.title("Dashboard de Gastos Pessoais")

aba1, aba2, aba3 = st.tabs(["📊 Visão Geral", "📈 Análises", "📋 Dataset"])

with aba1:
    total = df["Valor"].sum()
    qtd_transacoes = len(df)
    media = df["Valor"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Total gasto", f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    col2.metric("🧾 Transações", qtd_transacoes)
    col3.metric("📊 Média por gasto", f"R$ {media:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

with aba2:
    st.subheader("Gastos por Categoria")
    fig_cat = px.bar(df, x="Categoria", y="Valor", color="Categoria", title="Gastos por Categoria")
    st.plotly_chart(fig_cat, use_container_width=True, key="grafico_categoria")  # <- adiciona key

    st.subheader("Evolução dos Gastos ao Longo do Tempo")
    fig_tempo = px.line(df.sort_values("Lançamento"), x="Lançamento", y="Valor", color="Tipo")
    st.plotly_chart(fig_tempo, use_container_width=True, key="grafico_evolucao")  # <- adiciona key

with aba3:
    st.dataframe(df)