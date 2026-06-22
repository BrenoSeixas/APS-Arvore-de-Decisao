# Árvore de Decisão ID3 (Iterative Dichotomiser 3)

Este repositório contém uma implementação do algoritmo clássico de aprendizado de máquina supervisionado **ID3** para a construção de Árvores de Decisão, desenvolvido por Ross Quinlan em 1986. A implementação foi feita do zero (from scratch) utilizando Python e a biblioteca `pandas` para a manipulação dos dados.

## 📌 Autor
* **Nome:** Breno Olegário Seixas
* **Matrícula:** 2023101356

---

## 🚀 Funcionalidades

* **Cálculo de Entropia:** Mede a impureza ou desordem nos subconjuntos de dados.
* **Cálculo de Ganho de Informação:** Avalia a eficácia de cada atributo na divisão dos dados.
* **Construção Recursiva da Árvore:** Gera a árvore de decisão dinamicamente de acordo com as divisões com maior ganho de informação.
* **Suporte Multi-formato:** Suporta a leitura de datasets tanto no formato Excel (`.xlsx`) quanto CSV.
* **Saída Estruturada:** Retorna a árvore gerada formatada em uma estrutura JSON para fácil visualização.

---

## 📁 Estrutura do Projeto

* `APS.IA.py`: Script principal que contém a lógica do algoritmo ID3, leitura do dataset e geração da árvore de decisão.
* `dataset.xlsx`: Arquivo Excel de exemplo contendo o dataset clássico de decisão de jogo ("Jogar" Sim/Não) baseado nas condições climáticas.
* `explicacao_id3.md`: Explicação matemática detalhada sobre como o cálculo da Entropia e do Ganho de Informação é realizado no algoritmo.
* `README.md`: Este arquivo com as instruções de uso e informações do projeto.

---

## 🛠️ Requisitos e Dependências

Para executar este projeto, você precisará ter o **Python 3** instalado em sua máquina, além das seguintes bibliotecas:

* [pandas](https://pandas.pydata.org/) (para manipulação e leitura dos datasets)
* [openpyxl](https://openpyxl.readthedocs.io/en/stable/) (necessário para a leitura de arquivos Excel `.xlsx`)

### Instalação das dependências

Você pode instalar todas as dependências rodando o comando abaixo no seu terminal:

```bash
pip install pandas openpyxl
```

---

## 🏃 Como Executar

1. Coloque o seu conjunto de dados no diretório do projeto (ou utilize o `dataset.xlsx` já incluso).
2. Abra o arquivo [APS.IA.py](file:///c:/Users/Aluno/Desktop/Projetos/Arvore-de-Decisao/APS.IA.py) e configure as variáveis no final do arquivo com o nome do seu dataset e a coluna alvo:
   ```python
   CAMINHO_EXCEL = "dataset.xlsx"
   COLUNA_ALVO = "Jogar"
   ```
3. Execute o script utilizando o Python:
   ```bash
   python APS.IA.py
   ```

### Exemplo de Saída no Terminal

```text
Dataset carregado com 4 linhas.
Atributos analisados: ['Aparência', 'Temperatura', 'Umidade', 'Vento']

Árvore de Decisão:
{
  "Aparência": {
    "Sol": "Nao",
    "Nublado": "Sim",
    "Chuva": "Sim"
  }
}
```

---

## 📖 Como Funciona?

O ID3 baseia-se em dois conceitos fundamentais da Teoria da Informação:

### 1. Entropia
A entropia mede o grau de impureza de um conjunto de dados. Se os dados pertencem a uma única classe, a entropia é `0`. Se as classes estão distribuídas igualmente, a entropia é `1`.
$$\text{Entropia}(S) = - \sum p_i \log_2(p_i)$$

### 2. Ganho de Informação
O Ganho de Informação mede a redução da entropia que obtemos ao dividir o dataset por um determinado atributo.
$$\text{Ganho}(S, A) = \text{Entropia}(S) - \sum \frac{|S_v|}{|S|} \text{Entropia}(S_v)$$

A cada passo recursivo, o algoritmo ID3 escolhe o atributo com o **maior ganho de informação** para ser o nó de decisão, divide o dataset e repete o processo até que todas as folhas sejam puras ou não haja mais atributos disponíveis.

Para mais detalhes sobre as fórmulas e um passo a passo do cálculo manual, consulte o arquivo [explicacao_id3.md](file:///c:/Users/Aluno/Desktop/Projetos/Arvore-de-Decisao/explicacao_id3.md).
