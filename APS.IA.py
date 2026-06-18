import math
import pandas as pd
import json

def calcular_entropia(df, alvo):
    n_linhas = len(df)
    if n_linhas == 0:
        return 0

    classes = df[alvo].value_counts()
    
    entropia = 0.0
    for qtd in classes:
        p = qtd / n_linhas
        entropia -= p * math.log2(p)
        
    return entropia

def informacao(df, atributo, alvo):
    entropia_total = calcular_entropia(df, alvo)
    n_linhas = len(df)
    
    valores_atributo = df[atributo].unique()
    
    soma_ent = 0.0
    for valor in valores_atributo:
        subconjunto = df[df[atributo] == valor]
        peso = len(subconjunto) / n_linhas
        soma_ent += peso * calcular_entropia(subconjunto, alvo)
        
    return entropia_total - soma_ent

def id3(df, atrib, alvo):
    classes_unicas = df[alvo].unique()
    if len(classes_unicas) == 1:
        return classes_unicas[0]

    if len(atrib) == 0:
        return df[alvo].mode()[0]

    melhor = atrib[0]
    maior_ganho = -1.0
    
    for attr in atrib:
        ganho = informacao(df, attr, alvo)
        if ganho > maior_ganho:
            maior_ganho = ganho
            melhor = attr

    arvore = {melhor: {}}
    valores_possiveis = df[melhor].unique()
    restantes = [attr for attr in atrib if attr != melhor]

    for valor in valores_possiveis:
        subconjunto = df[df[melhor] == valor]
        
        if len(subconjunto) == 0:
            arvore[melhor][valor] = df[alvo].mode()[0]
        else:
            arvore[melhor][valor] = id3(subconjunto, restantes, alvo)
            
    return arvore

def id3_excel(caminho_arquivo, alvo):
    df = pd.read_excel(caminho_arquivo)
    
    if df.empty:
        print("Arquivo vazio!")
        return

    atrib = [col for col in df.columns if col != alvo]
    
    
    print(f"Dataset carregado com {len(df)} linhas.")
    print(f"Atributos analisados: {atrib}\n")
    
    arvore_gerada = id3(df, atrib, alvo)
    
    print("Árvore de Decisão Resultante:")
    print(json.dumps(arvore_gerada, indent=2, ensure_ascii=False))


CAMINHO_EXCEL = "dataset.xlsx"
COLUNA_ALVO = "Jogar"

id3_excel(CAMINHO_EXCEL, COLUNA_ALVO)