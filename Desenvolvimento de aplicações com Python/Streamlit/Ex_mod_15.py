import pandas as pd  # Importa a biblioteca pandas para manipulação de dados
import streamlit as st  # Importa a biblioteca Streamlit para a criação da aplicação web
# Importa a biblioteca matplotlib para criação de gráficos
import matplotlib.pyplot as plt

# Configuração inicial da página do Streamlit
st.set_page_config(
    page_title="SINASC Rondônia",  # Define o título da página
    layout='wide',  # Define o layout como "wide" (larga)
    page_icon="https://media.istockphoto.com/id/1131451829/pt/vetorial/emblem-of-rondonia-state-of-brazil.jpg?s=612x612&w=0&k=20&c=wLFBnEkRSZNxNvji8r7r4ROshnwnxxRUrYHVz-Cu-e8="  # Define um ícone para a página
)

st.write("# Análise Sinasc")  # Escreve o título da análise na aplicação

# Função para carregar e formatar os dados


@st.cache_data  # Cacheia os dados para otimizar a performance, evitando a recarga desnecessária
def get_data_format(caminho):
    dados = pd.read_csv(caminho)  # Lê o arquivo CSV no caminho especificado
    # Converte a coluna de data para o formato datetime
    dados['DTNASC'] = pd.to_datetime(dados['DTNASC'])
    return dados  # Retorna o DataFrame formatado


# Carrega os dados do arquivo CSV e os formata
df = get_data_format('input_M15_SINASC_RO_2019.csv')

# Seleciona o intervalo de datas com um único slider na barra lateral
date_range = st.sidebar.slider(
    "Selecione o intervalo de datas",  # Título do slider
    # Define o valor mínimo como a data inicial no DataFrame
    min_value=df['DTNASC'].min().to_pydatetime(),
    # Define o valor máximo como a data final no DataFrame
    max_value=df['DTNASC'].max().to_pydatetime(),
    # Define o intervalo padrão como o intervalo total de datas
    value=(df['DTNASC'].min().to_pydatetime(),
           df['DTNASC'].max().to_pydatetime()),
    format="DD-MM-YYYY"  # Formata as datas no slider como "dia-mês-ano"
)

# Extrai a data inicial e final do intervalo selecionado
start_date, end_date = date_range

# Cria três colunas na página para exibir as datas
col1, col2, _, _ = st.columns(4)

with col1:
    st.write(f"""
        <div style='text-align: center;'>
            <b>Data inicial:</b><br>
            <span style='font-size: 24px;'>{start_date.strftime("%d/%m/%Y")}</span>
        </div>
        """, unsafe_allow_html=True)

with col2:
    st.write(f"""
        <div style='text-align: center;'>
            <b>Data final:</b><br>
            <span style='font-size: 24px;'>{end_date.strftime("%d/%m/%Y")}</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown('---')

# Filtra o DataFrame para incluir apenas as datas selecionadas
df_filtrado = df[(df['DTNASC'] >= start_date) & (df['DTNASC'] <= end_date)]

# Conta o número total de nascimentos no período
total_nascidos = len(df_filtrado['DTNASC'])
# Calcula a média do APGAR1 no período
media_apgar1 = df_filtrado['APGAR1'].mean()
# Calcula a média do APGAR5 no período
media_apgar5 = df_filtrado['APGAR5'].mean()

# Cria três colunas para exibir as estatísticas calculadas
col1, col2, col3 = st.columns(3)

# Exibe o total de nascimentos no período na primeira coluna, centralizado e formatado
with col1:
    st.write(f"""
        <div style='text-align: center;'>
            <b>Total de nascimentos no período:</b><br>
            <span style='font-size: 24px;'>{total_nascidos}</span>
        </div>
        """, unsafe_allow_html=True)

# Exibe a média APGAR1 na segunda coluna, centralizado e formatado
with col2:
    st.write(f"""
        <div style='text-align: center;'>
            <b>Média APGAR1:</b><br>
            <span style='font-size: 24px;'>{round(media_apgar1, 1)}</span>
        </div>
        """, unsafe_allow_html=True)

# Exibe a média APGAR5 na terceira coluna, centralizado e formatado
with col3:
    st.write(f"""
        <div style='text-align: center;'>
            <b>Média APGAR5:</b><br>
            <span style='font-size: 24px;'>{round(media_apgar5, 1)}</span>
        </div>
        """, unsafe_allow_html=True)

# Exibe o subtítulo e o gráfico de média da idade da mãe por data de nascimento
st.subheader('Média Idade da Mãe x Data de Nascimento')

ax = pd.pivot_table(df_filtrado, values='IDADEMAE', index='DTNASC',
                    aggfunc='mean').plot(figsize=[15, 5])
plt.xlabel("data de nascimento")
plt.ylabel('média idade mãe')
ax.get_legend().remove()  # Remove a legenda do gráfico
plt.tight_layout()
st.pyplot(fig=plt)  # Exibe o gráfico na aplicação Streamlit
plt.close()  # Fecha a figura para evitar conflitos de renderização

# Exibe o subtítulo e o gráfico de quantidade de nascimentos por data de nascimento
st.subheader('Quantidade de nascimentos x Data de Nascimento')

ax = pd.pivot_table(df_filtrado, values='IDADEMAE', index='DTNASC',
                    aggfunc='count').plot(figsize=[15, 5])
plt.xlabel("data de nascimento")
plt.ylabel('Qtd nascimentos')
ax.get_legend().remove()
plt.tight_layout()
st.pyplot(fig=plt)
plt.close()
