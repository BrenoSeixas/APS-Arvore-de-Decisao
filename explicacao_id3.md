# Explicação do Algoritmo de Árvore de Decisão ID3

Este documento explica de forma detalhada e didática o funcionamento do algoritmo **ID3 (Iterative Dichotomiser 3)** implementado no arquivo [ide3.py](file:///c:/Users/olega/OneDrive/Área de Trabalho/Projetos/Arvore-de-Decisao/ide3.py).

---

## 1. O que é o Algoritmo ID3?

O **ID3** é um algoritmo clássico de aprendizado de máquina supervisionado usado para construir **Árvores de Decisão** a partir de um conjunto de dados. Ele foi desenvolvido por Ross Quinlan em 1986.

O objetivo principal do ID3 é criar uma árvore de decisão que classifique novos exemplos da melhor forma possível, fazendo perguntas binárias ou de múltiplos caminhos baseadas nos atributos do dataset.

Para decidir qual pergunta (ou divisão de atributo) é a melhor em cada ponto da árvore, o algoritmo usa dois conceitos matemáticos fundamentais da Teoria da Informação:
1. **Entropia** (Medida de desordem ou impureza)
2. **Ganho de Informação** (Redução da entropia após a divisão)

---

## 2. Conceitos Matemáticos Fundamentais

### A. Entropia
A entropia mede a impureza ou o nível de "mistura" das classes em um conjunto de dados.
- Se todos os exemplos em um subconjunto pertencem à mesma classe (por exemplo, todos são "Sim" para a pergunta "Jogar"), a **Entropia é 0** (conjunto totalmente puro).
- Se os exemplos estão divididos igualmente (por exemplo, 50% "Sim" e 50% "Não"), a **Entropia é 1** (máxima desordem).

A fórmula matemática da entropia para um conjunto $S$ é:

$$H(S) = - \sum_{i=1}^{c} p_i \log_2(p_i)$$

Onde:
- $p_i$ é a proporção (probabilidade) de exemplos pertencentes à classe $i$ no conjunto de dados.
- $c$ é o número total de classes.

No código, essa função é implementada em:
```python
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
```

---

### B. Ganho de Informação
O Ganho de Informação mede a eficácia de um atributo em classificar o conjunto de dados. Ele nos diz o quanto a entropia diminui se dividirmos o conjunto com base em um determinado atributo.

A fórmula é:

$$Gain(S, A) = H(S) - \sum_{v \in \text{valores}(A)} \frac{|S_v|}{|S|} H(S_v)$$

Onde:
- $H(S)$ é a entropia inicial do conjunto antes da divisão.
- $A$ é o atributo avaliado.
- $v$ representa cada valor possível que o atributo $A$ pode assumir (ex: para "Aparência", os valores podem ser "Sol", "Nublado", "Chuva").
- $S_v$ é o subconjunto de dados onde o atributo $A$ tem o valor $v$.
- $\frac{|S_v|}{|S|}$ é o "peso" (proporção) daquele subconjunto em relação ao total.

No código, essa função é implementada em:
```python
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
```

---

## 3. Estrutura de Decisão: O Algoritmo Recursivo `id3`

O algoritmo `id3` reconstrói a árvore dividindo o conjunto recursivamente. O fluxo principal é:

1. **Casos Base (Critérios de Parada)**:
   - **Se todos os registros pertencem à mesma classe**: Retorna essa classe diretamente (folha).
   - **Se não restarem mais atributos para avaliar**: Retorna a classe mais frequente (moda) nos registros atuais.
2. **Escolha do Melhor Atributo**:
   - Calcula o Ganho de Informação para cada atributo restante.
   - Seleciona o atributo com o **maior ganho**.
3. **Criação dos Ramos**:
   - Cria um nó de decisão com o melhor atributo.
   - Para cada valor exclusivo desse atributo, filtra o dataset para conter apenas as linhas correspondentes.
   - Se o subconjunto estiver vazio, cria uma folha com a classe mais comum do conjunto original.
   - Caso contrário, chama o `id3` recursivamente passando o subconjunto e a lista de atributos restantes (removendo o atributo recém-usado).

Implementação no código:
```python
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
```

---

## 4. Exemplo Prático com seu Dataset (`dataset.xlsx`)

Vamos analisar passo a passo o que acontece quando executamos o código sobre o seu arquivo [dataset.xlsx](file:///c:/Users/olega/OneDrive/Área de Trabalho/Projetos/Arvore-de-Decisao/dataset.xlsx):

### O Conjunto de Dados:
| Aparência | Temperatura | Umidade | Vento | Jogar (Alvo) |
| :--- | :--- | :--- | :--- | :--- |
| Sol | Quente | Alta | Fraco | **Nao** |
| Sol | Quente | Alta | Forte | **Nao** |
| Nublado | Quente | Alta | Fraco | **Sim** |
| Chuva | Amena | Normal | Fraco | **Sim** |

### Passo 1: Cálculo da Entropia Total de "Jogar" ($S$)
O dataset tem 4 linhas. A classe alvo `Jogar` tem:
- 2 instâncias de **Nao**
- 2 instâncias de **Sim**

$$H(S) = - \left( \frac{2}{4}\log_2\left(\frac{2}{4}\right) + \frac{2}{4}\log_2\left(\frac{2}{4}\right) \right) = - (0.5 \times (-1) + 0.5 \times (-1)) = 1.0$$
*A entropia é máxima (1.0) porque as classes estão divididas exatamente ao meio.*

### Passo 2: Avaliação dos Atributos
Para decidir a raiz da árvore, calculamos o Ganho de Informação para cada atributo:

#### A. Atributo: `Aparência`
Valores possíveis: `Sol` (2 ocorrências), `Nublado` (1 ocorrência), `Chuva` (1 ocorrência).
- **Subconjunto Sol**: 2 linhas (linhas 1 e 2). Ambas têm `Jogar` = **Nao**.
  - Entropia de Sol = 0 (100% puro)
- **Subconjunto Nublado**: 1 linha. Tem `Jogar` = **Sim**.
  - Entropia de Nublado = 0 (100% puro)
- **Subconjunto Chuva**: 1 linha. Tem `Jogar` = **Sim**.
  - Entropia de Chuva = 0 (100% puro)

Cálculo do Ganho para `Aparência`:
$$\text{Ganho}(S, \text{Aparência}) = 1.0 - \left( \frac{2}{4} \times 0 + \frac{1}{4} \times 0 + \frac{1}{4} \times 0 \right) = 1.0$$
*Temos um Ganho de Informação máximo de 1.0!*

#### B. Outros Atributos (`Temperatura`, `Umidade`, `Vento`)
Se calcularmos para qualquer um dos outros atributos, a divisão não será perfeita. Por exemplo, para `Vento`:
- **Subconjunto Fraco**: 3 ocorrências (2 "Sim", 1 "Nao"). Entropia $\approx 0.918$.
- **Subconjunto Forte**: 1 ocorrência (1 "Nao"). Entropia = 0.
- Ganho para `Vento`:
$$\text{Ganho}(S, \text{Vento}) = 1.0 - \left( \frac{3}{4} \times 0.918 + \frac{1}{4} \times 0 \right) \approx 1.0 - 0.688 \approx 0.312$$

### Passo 3: Criação da Árvore
Como o atributo `Aparência` tem o maior Ganho de Informação (1.0 vs 0.312 dos outros), ele é escolhido como o nó raiz da árvore:

1. Se `Aparência` for **Sol**, o subconjunto contém apenas a classe **Nao**. É uma folha.
2. Se `Aparência` for **Nublado**, o subconjunto contém apenas a classe **Sim**. É uma folha.
3. Se `Aparência` for **Chuva**, o subconjunto contém apenas a classe **Sim**. É uma folha.

A árvore de decisão gerada e exibida no console é:
```python
{
    'Aparência': {
        'Chuva': 'Sim', 
        'Nublado': 'Sim', 
        'Sol': 'Nao'
    }
}
```

Como todos os ramos levaram a folhas com classes puras (entropia zero), o algoritmo finaliza a recursão imediatamente e a árvore fica pronta com apenas 1 nível de decisão!

---

## 5. Como Executar o Script

1. Certifique-se de que o Python e os pacotes necessários estão instalados. Você pode instalar as dependências necessárias executando:
   ```bash
   pip install pandas openpyxl
   ```
2. Execute o arquivo:
   ```bash
   python ide3.py
   ```
3. O console exibirá o número de linhas carregadas do arquivo e a árvore formatada de forma hierárquica usando a biblioteca `pprint`.
