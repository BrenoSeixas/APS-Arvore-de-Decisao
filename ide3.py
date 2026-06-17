import math
import pandas as pd
import pprint

def calcular_entropia(df, coluna_alvo):
    total_registros = len(df)
    if total_registros == 0:
        return 0

    contagem_classes = df[coluna_alvo].value_counts()
    
    entropia = 0.0
    for qtd in contagem_classes:
        p = qtd / total_registros
        entropia -= p * math.log2(p)
        
    return entropia

def calcular_ganho_informacao(df, atributo, coluna_alvo):
    entropia_total = calcular_entropia(df, coluna_alvo)
    total_registros = len(df)
    
    valores_atributo = df[atributo].unique()
    
    soma_entropia_subconjuntos = 0.0
    for valor in valores_atributo:
        subconjunto = df[df[atributo] == valor]
        peso = len(subconjunto) / total_registros
        soma_entropia_subconjuntos += peso * calcular_entropia(subconjunto, coluna_alvo)
        
    return entropia_total - soma_entropia_subconjuntos

def id3(df, atributos, coluna_alvo):
    classes_unicas = df[coluna_alvo].unique()
    if len(classes_unicas) == 1:
        return classes_unicas[0]

    if len(atributos) == 0:
        return df[coluna_alvo].mode()[0]

    melhor_atributo = atributos[0]
    maior_ganho = -1.0
    
    for attr in atributos:
        ganho = calcular_ganho_informacao(df, attr, coluna_alvo)
        if ganho > maior_ganho:
            maior_ganho = ganho
            melhor_atributo = attr

    arvore = {melhor_atributo: {}}
    valores_possiveis = df[melhor_atributo].unique()
    atributos_restantes = [attr for attr in atributos if attr != melhor_atributo]

    for valor in valores_possiveis:
        subconjunto = df[df[melhor_atributo] == valor]
        
        if len(subconjunto) == 0:
            arvore[melhor_atributo][valor] = df[coluna_alvo].mode()[0]
        else:
            arvore[melhor_atributo][valor] = id3(subconjunto, atributos_restantes, coluna_alvo)
            
    return arvore

def executar_id3_excel(caminho_arquivo, coluna_alvo):
    try:
        try:
            df = pd.read_excel(caminho_arquivo)
        except Exception:
            # Caso o arquivo não seja um Excel válido, tenta ler como CSV (ex: CSV salvo com extensão .xlsx)
            df = pd.read_csv(caminho_arquivo)
        
        if df.empty:
            print("O arquivo está vazio.")
            return

        atributos = [col for col in df.columns if col != coluna_alvo]
        
        print(f"Dataset carregado com sucesso ({len(df)} linhas).")
        print(f"Coluna Alvo (Classe): {coluna_alvo}")
        print(f"Atributos Analisados: {', '.join(atributos)}\n")
        
        arvore_gerada = id3(df, atributos, coluna_alvo)
        
        print("Árvore de Decisão Gerada:")
        pprint.pprint(arvore_gerada, indent=4)

    except Exception as e:
        print(f"Erro ao processar o arquivo: {e}")

CAMINHO_EXCEL = "dataset.xlsx"
COLUNA_ALVO = "Jogar"

executar_id3_excel(CAMINHO_EXCEL, COLUNA_ALVO)