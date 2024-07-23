import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import sys

sns.set_theme()

# Função para gerar os gráficos


def plot_sinasc_mes_savefig(dataframe):

    mes_ano = pd.to_datetime(
        dataframe.DTNASC, dayfirst=True).max().strftime("%m-%Y")

    os.makedirs(f'./output/figs/{mes_ano}', exist_ok=True)

    pd.pivot_table(dataframe, values='IDADEMAE', index='DTNASC',
                   aggfunc='mean').plot(figsize=[15, 5], title="Média Idade da Mãe x Data de Nascimento")
    plt.xlabel("data de nascimento")
    plt.ylabel('média idade mãe')
    plt.tight_layout()
    plt.savefig(
        f'./output/figs/{mes_ano}/media idade mae x qtd nascimentos.png')
    plt.close()

    pd.pivot_table(dataframe, values='IDADEMAE', index='DTNASC',
                   aggfunc='count').plot(figsize=[15, 5], title="Quantidade de nascimentos x Data de Nascimento")
    plt.xlabel("data de nascimento")
    plt.ylabel('qtd nascimentos')
    plt.tight_layout()
    plt.savefig(f'./output/figs/{mes_ano}/quantidade de nascimentos.png')
    plt.close()

    pd.pivot_table(dataframe, values='IDADEMAE', index=['DTNASC', 'SEXO'],
                   aggfunc='count').unstack().plot(figsize=[15, 6], title="Quantidade de nascimentos x Data de Nascimento e Sexo")
    plt.legend()
    plt.xlabel("data de nascimento")
    plt.ylabel('qtd nascimentos')
    plt.tight_layout()
    plt.savefig(
        f'./output/figs/{mes_ano}/quantidade de nascimentos por sexo.png')
    plt.close()

    pd.pivot_table(dataframe, values='PESO', index=['DTNASC', 'SEXO'],
                   aggfunc='mean').unstack().plot(figsize=[15, 6], title="Peso médio x Data de Nascimento e Sexo")
    plt.legend()
    plt.xlabel("data de nascimento")
    plt.ylabel('peso médio')
    plt.tight_layout()
    plt.savefig(
        f'./output/figs/{mes_ano}/peso medio por sexo de nascimentos.png')
    plt.close()

    pd.pivot_table(dataframe, values='PESO', index=['ESCMAE'],
                   aggfunc='median').sort_values('PESO').plot(figsize=[18, 6], title="Mediana do Peso x Escolaridade da mãe")
    plt.xlabel("escolaridade da mãe")
    plt.ylabel('mediana peso')
    plt.tight_layout()
    plt.savefig(f'./output/figs/{mes_ano}/mediana peso x escolaridade mae.png')
    plt.close()

    pd.pivot_table(dataframe, values='APGAR1', index=['GESTACAO'],
                   aggfunc='mean').sort_values('APGAR1').plot(figsize=[18, 6], title="APGAR1 médio x Tempo de gestação")
    plt.ylabel('apgar1 medio')
    plt.xlabel('gestacao')
    plt.tight_layout()
    plt.savefig(f'./output/figs/{mes_ano}/media apgar1 x tempo gestacao.png')
    plt.close()

    pd.pivot_table(dataframe, values='APGAR5', index=['GESTACAO'],
                   aggfunc='mean').sort_values('APGAR5').plot(figsize=[18, 6], title="APGAR5 médio x Tempo de gestação")
    plt.ylabel('apgar5 médio')
    plt.xlabel('gestação')
    plt.tight_layout()
    plt.savefig(f'./output/figs/{mes_ano}/media apgar1 x tempo gestacao.png')
    plt.close()

# Função para ler os arquivos .csv e formatar a data


def get_data_format(caminho):

    dados = pd.read_csv(caminho)
    dados['DTNASC'] = pd.to_datetime(dados['DTNASC'])

    return dados

# Execução do script


for arg in sys.argv[1:]:
    df = get_data_format(f'input\SINASC_RO_2019_{arg}.csv')
    plot_sinasc_mes_savefig(df)
