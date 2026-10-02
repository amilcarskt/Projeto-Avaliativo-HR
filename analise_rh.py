"""
===============================================================================
PROJETO: Análise de Dados de Recursos Humanos (HR) - FreeSQL
DISCIPLINA: Visualização de Dados e Business Intelligence [T3]
SITUAÇÃO DE APRENDIZAGEM: Projeto Avaliativo - Módulo 1 - Semana 13
ALUNO: Amilcar
===============================================================================
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração de diretórios
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
IMG_DIR = BASE_DIR / "img"

IMG_DIR.mkdir(parents=True, exist_ok=True)

# Configuração visual global do Matplotlib/Seaborn
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams["font.sans-serif"] = "DejaVu Sans"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 10


def carregar_dados():
    """
    Carrega os dados dos arquivos CSV gerados pelas consultas SQL no FreeSQL.
    Compatível com os nomes query_01.csv / Query_1.csv e query_02.csv / Query_2.csv.
    """
    caminho_q1 = DATA_DIR / "query_01.csv" if (DATA_DIR / "query_01.csv").exists() else DATA_DIR / "Query_1.csv"
    caminho_q2 = DATA_DIR / "query_02.csv" if (DATA_DIR / "query_02.csv").exists() else DATA_DIR / "Query_2.csv"

    if not caminho_q1.exists() or not caminho_q2.exists():
        raise FileNotFoundError(f"Arquivos CSV não encontrados na pasta '{DATA_DIR}'. Verifique a extração.")

    df_cargos = pd.read_csv(caminho_q1)
    df_regioes = pd.read_csv(caminho_q2)

    # Padronização dos nomes de colunas (caixa alta e sem espaços)
    df_cargos.columns = [col.strip().upper() for col in df_cargos.columns]
    df_regioes.columns = [col.strip().upper() for col in df_regioes.columns]

    return df_cargos, df_regioes


def calcular_estatisticas(df, coluna_salario="SALARIO"):
    """
    Calcula e exibe as estatísticas descritivas básicas exigidas no projeto:
    Média, Mediana, Mínimo, Máximo, Desvio Padrão, Amplitude e Quartis.
    """
    media = df[coluna_salario].mean()
    mediana = df[coluna_salario].median()
    minimo = df[coluna_salario].min()
    maximo = df[coluna_salario].max()
    desvio = df[coluna_salario].std()
    amplitude = maximo - minimo
    q25 = df[coluna_salario].quantile(0.25)
    q75 = df[coluna_salario].quantile(0.75)

    print("\n" + "=" * 65)
    print(f"ESTATÍSTICAS DESCRITIVAS GERAIS DE SALÁRIO ({len(df)} Colaboradores)")
    print("=" * 65)
    print(f"  • Média Salarial:         $ {media:,.2f}")
    print(f"  • Mediana Salarial:       $ {mediana:,.2f}")
    print(f"  • Salário Mínimo:         $ {minimo:,.2f}")
    print(f"  • Salário Máximo:         $ {maximo:,.2f}")
    print(f"  • Desvio Padrão:          $ {desvio:,.2f}")
    print(f"  • Amplitude Salarial:     $ {amplitude:,.2f}")
    print(f"  • 1º Quartil (Q1 - 25%):  $ {q25:,.2f}")
    print(f"  • 3º Quartil (Q3 - 75%):  $ {q75:,.2f}")
    print("=" * 65)

    return {
        "media": media,
        "mediana": mediana,
        "minimo": minimo,
        "maximo": maximo,
        "desvio": desvio,
        "amplitude": amplitude,
        "q25": q25,
        "q75": q75,
    }


def calcular_estatisticas_agrupadas(df, agrupador, coluna_salario="SALARIO"):
    """Calcula estatísticas agrupadas por departamento ou região."""
    stats = df.groupby(agrupador)[coluna_salario].agg(
        Qtd="count",
        Media="mean",
        Mediana="median",
        Minimo="min",
        Maximo="max",
        Desvio_Padrao="std"
    ).reset_index()

    stats = stats.sort_values(by="Mediana", ascending=False)
    print(f"\n--- Estatísticas Agrupadas por {agrupador} ---")
    print(stats.to_string(index=False, formatters={
        "Media": lambda x: f"${x:,.2f}",
        "Mediana": lambda x: f"${x:,.2f}",
        "Minimo": lambda x: f"${x:,.2f}",
        "Maximo": lambda x: f"${x:,.2f}",
        "Desvio_Padrao": lambda x: f"${x:,.2f}" if pd.notnull(x) else "N/A"
    }))
    return stats


def gerar_grafico_boxplot(df):
    """
    Gráfico 1: Boxplot da distribuição salarial por departamento com stripplot de pontos individuais.
    Destaca a dispersão, os quartis e os cargos de alta liderança (outliers).
    """
    plt.figure(figsize=(12, 6))

    col_dept = "NOME_DEPARTAMENTO" if "NOME_DEPARTAMENTO" in df.columns else "DEPARTAMENTO"
    ordem = df.groupby(col_dept)["SALARIO"].median().sort_values(ascending=False).index

    palette = sns.color_palette("Blues_r", n_colors=len(ordem))
    ax = sns.boxplot(
        x=col_dept,
        y="SALARIO",
        hue=col_dept,
        data=df,
        order=ordem,
        palette=palette,
        legend=False,
        width=0.6
    )
    sns.stripplot(
        x=col_dept,
        y="SALARIO",
        data=df,
        order=ordem,
        color="#2c3e50",
        alpha=0.5,
        jitter=0.2,
        size=6
    )

    plt.title("Distribuição Salarial por Departamento (com Dispersão Individual)", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Departamento", fontsize=11, fontweight="bold")
    plt.ylabel("Salário Mensal (USD)", fontsize=11, fontweight="bold")
    plt.xticks(rotation=35, ha="right")
    
    # Formatação do eixo Y em milhares
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    plt.tight_layout()
    caminho = IMG_DIR / "boxplot_salarios_departamento.png"
    plt.savefig(caminho, dpi=300)
    plt.close()
    print(f"[OK] Gráfico salvo: {caminho}")


def gerar_grafico_histograma(df):
    """
    Gráfico 2: Histograma com KDE destacando a assimetria positiva entre Média e Mediana.
    """
    plt.figure(figsize=(10, 5.5))

    media = df["SALARIO"].mean()
    mediana = df["SALARIO"].median()

    ax = sns.histplot(
        df["SALARIO"],
        bins=12,
        kde=True,
        color="#2980b9",
        edgecolor="#1c2833",
        alpha=0.65
    )

    plt.axvline(media, color="#e74c3c", linestyle="--", linewidth=2.5, label=f"Média: $ {media:,.2f}")
    plt.axvline(mediana, color="#27ae60", linestyle="-", linewidth=2.5, label=f"Mediana: $ {mediana:,.2f}")

    plt.title("Distribuição Geral de Salários: Evidência de Assimetria Positiva", fontsize=14, fontweight="bold", pad=15)
    plt.xlabel("Salário (USD)", fontsize=11, fontweight="bold")
    plt.ylabel("Frequência de Colaboradores", fontsize=11, fontweight="bold")
    
    # Formatação do eixo X em moeda
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    
    plt.legend(fontsize=11, loc="upper right")
    plt.tight_layout()
    caminho = IMG_DIR / "histograma_distribuicao_salarial.png"
    plt.savefig(caminho, dpi=300)
    plt.close()
    print(f"[OK] Gráfico salvo: {caminho}")


def gerar_grafico_barras_regiao(df):
    """
    Gráfico 3: Comparativo regional com Média Salarial e Total de Colaboradores (Americas vs Europe).
    """
    col_reg = "REGIAO"
    resumo = df.groupby(col_reg)["SALARIO"].agg(["mean", "count"]).reset_index()

    fig, ax1 = plt.subplots(figsize=(8.5, 5))
    cor_barras = "#1f4e79"

    bars = ax1.bar(
        resumo[col_reg],
        resumo["mean"],
        color=cor_barras,
        width=0.45,
        label="Média Salarial"
    )
    ax1.set_xlabel("Região Geográfica", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Média Salarial (USD)", color=cor_barras, fontsize=11, fontweight="bold")
    ax1.tick_params(axis="y", labelcolor=cor_barras)
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))

    for bar in bars:
        altura = bar.get_height()
        ax1.annotate(
            f"$ {altura:,.2f}",
            xy=(bar.get_x() + bar.get_width() / 2, altura),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontweight="bold",
            fontsize=10
        )

    ax2 = ax1.twinx()
    cor_linha = "#d35400"
    ax2.plot(
        resumo[col_reg],
        resumo["count"],
        color=cor_linha,
        marker="o",
        linewidth=2.5,
        markersize=9,
        label="Total de Colaboradores"
    )
    ax2.set_ylabel("Total de Colaboradores", color=cor_linha, fontsize=11, fontweight="bold")
    ax2.tick_params(axis="y", labelcolor=cor_linha)
    ax2.grid(False)

    for i, row in resumo.iterrows():
        ax2.annotate(
            f"{row['count']} func.",
            xy=(row[col_reg], row["count"]),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            va="bottom",
            color=cor_linha,
            fontweight="bold",
            fontsize=10
        )

    plt.title("Comparativo Regional: Média Salarial vs Contagem de Pessoal", fontsize=13, fontweight="bold", pad=15)
    plt.tight_layout()
    caminho = IMG_DIR / "media_salarial_regiao.png"
    plt.savefig(caminho, dpi=300)
    plt.close()
    print(f"[OK] Gráfico salvo: {caminho}")


def gerar_grafico_media_departamento(df):
    """
    Gráfico 4: Ranking horizontal da média salarial por departamento.
    """
    plt.figure(figsize=(10, 6))

    col_dept = "NOME_DEPARTAMENTO" if "NOME_DEPARTAMENTO" in df.columns else "DEPARTAMENTO"
    ranking = df.groupby(col_dept)["SALARIO"].mean().sort_values(ascending=True)

    ax = ranking.plot(kind="barh", color="#2c7bb6", width=0.7)
    plt.title("Ranking da Média Salarial por Departamento", fontsize=13, fontweight="bold", pad=15)
    plt.xlabel("Média Salarial (USD)", fontsize=11, fontweight="bold")
    plt.ylabel("Departamento", fontsize=11, fontweight="bold")

    for i, valor in enumerate(ranking):
        ax.text(valor + 200, i, f"$ {valor:,.2f}", va="center", fontweight="bold", fontsize=9)

    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.xlim(0, ranking.max() * 1.15)
    plt.tight_layout()

    caminho = IMG_DIR / "media_salarial_departamento.png"
    plt.savefig(caminho, dpi=300)
    plt.close()
    print(f"[OK] Gráfico salvo: {caminho}")


def main():
    print("=" * 65)
    print("INICIANDO ANÁLISE EXPLORATÓRIA DE DADOS (EDA) - HR FREESQL")
    print("=" * 65)

    df_cargos, df_regioes = carregar_dados()

    # 1. Estatísticas descritivas gerais
    calcular_estatisticas(df_cargos)

    # 2. Estatísticas agrupadas por Departamento
    col_dept = "NOME_DEPARTAMENTO" if "NOME_DEPARTAMENTO" in df_cargos.columns else "DEPARTAMENTO"
    calcular_estatisticas_agrupadas(df_cargos, col_dept)

    # 3. Estatísticas agrupadas por Região
    calcular_estatisticas_agrupadas(df_regioes, "REGIAO")

    # 4. Geração dos gráficos
    print("\nGerando gráficos informativos de alta resolução...")
    gerar_grafico_boxplot(df_cargos)
    gerar_grafico_histograma(df_cargos)
    gerar_grafico_barras_regiao(df_regioes)
    gerar_grafico_media_departamento(df_cargos)

    print("\nProcessamento concluído com êxito! Imagens salvas na pasta 'img/'.")


if __name__ == "__main__":
    main()
