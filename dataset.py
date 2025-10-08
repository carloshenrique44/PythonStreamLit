import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("dados/faturainter.csv", sep=",") 

df['Valor'] = df['Valor'].replace({'R\$': '', ',': '.'}, regex=True).astype(float)

st.title("Dashboard de Gastos Pessoais")

st.sidebar.header("Filtros")
categorias = st.sidebar.multiselect("Selecione as categorias:", df["Categoria"].unique())
tipos = st.sidebar.multiselect("Selecione o tipo:", df["Tipo"].unique())
datas = st.sidebar.date_input("Período:", [])

df_filtrado = df.copy()

if categorias:
    df_filtrado = df_filtrado[df_filtrado["Categoria"].isin(categorias)]
if tipos:
    df_filtrado = df_filtrado[df_filtrado["Tipo"].isin(tipos)]
if len(datas) == 2:
    df_filtrado = df_filtrado[
        (df_filtrado["Lançamento"] >= pd.to_datetime(datas[0])) &
        (df_filtrado["Lançamento"] <= pd.to_datetime(datas[1]))
    ]
    
total = df_filtrado["Valor"].sum()
qtd_transacoes = len(df_filtrado)
media = df_filtrado["Valor"].mean()

st.metric("Total gasto", f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
st.metric("Transações", qtd_transacoes)
st.metric("Média por gasto", f"R$ {media:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

fig_cat = px.bar(
    df_filtrado,
    x="Categoria",
    y="Valor",
    color="Categoria",
    title="Gastos por Categoria"
)
st.plotly_chart(fig_cat, use_container_width=True)

fig_tempo = px.line(
    df_filtrado.sort_values("Lançamento"),
    x="Lançamento",
    y="Valor",
    color="Tipo",
    title="Evolução dos Gastos ao Longo do Tempo"
)
st.plotly_chart(fig_tempo, use_container_width=True)

st.subheader("Dados completos")
st.dataframe(df_filtrado)
