# Introdução

Este repositório foi criado para armazenar os notebooks e scripts para o data challenge Santander segunda edição. A solução proposta conta com um storytelling com dados e um dashboard para análise de vendas de pequenas empresas. A partir de uma planilha template (definindo as colunas) e um a preparação de um formulário para levantar dados sobre o perfil do cliente, é possível iniciar o processo de analytics em algumas empresas. O dashboard utiliza dados de pequenas empresas da base de e-commerce da Olist.

## Descrição do projeto

O projeto foi desenvolvido em Python utilizando libs para análise de dados (pandas, matplotlib, plotly, etc). Além dessas, foi utilizado o framework Streamit para criar um dashboard  que permite o input de dados e gera gráficos interativos automaticamente.

## Dashbord na web

[site](https://business-data-analysis.herokuapp.com/)

## Technologies
* Python 3
* Plotly
* Jupyter Notebook
* Streamlit

## Datasets
1. Yahoo Finanças:
  * [BOVA11](https://br.financas.yahoo.com/quote/BOVA11.SA/history?p=BOVA11.SA). 
  * [BTOW3](https://br.financas.yahoo.com/quote/BTOW3.SA/history?p=BTOW3.SA&.tsrc=fin-srch).
  * [VVAR3](https://br.financas.yahoo.com/quote/VVAR3.SA/history?p=VVAR3.SA&.tsrc=fin-srch).
  * [MGLU3](https://br.financas.yahoo.com/quote/MGLU3.SA/history?p=MGLU3.SA&.tsrc=fin-srch).
2. [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/olistbr/brazilian-ecommerce)
3. [ONS UK](https://www.ons.gov.uk/businessindustryandtrade/retailindustry/timeseries/j4mc/drsi)

## Começando

1. Clone este repositório (para ajudar use esse [tutorial](https://help.github.com/articles/cloning-a-repository/)).
2. Os datasets brutos estão [aqui](https://github.com/miltongneto/Santander-Data-Challenge/tree/master/data). 
3. Jupyter notebooks contendo nosso storytelling [aqui](https://github.com/miltongneto/Santander-Data-Challenge/tree/master/notebooks).
4. O script para o Dashboard [aqui](https://github.com/miltongneto/Santander-Data-Challenge/tree/master/src).

## Instalação

Use [pip3](https://pip.pypa.io/en/stable/) para instalar as bibliotecas necessárias para rodar os notebooks e script.

```bash
pip3 install -r requirements.txt.
```
### Ordem de leitura dos notebooks
Os notebooks foram utilizados para análise exploratória dos dados. A pasta notebooks_storytelling apresenta um Storytelling com Dados, com a numeração no início do arquivo para indicar a ordem. A análise segue do contexto macro para o micro, saindo da econômia no nível nacional e de grandes empresas para pequenas empresas e descoberta de padrões e dentências.

### Rodar o Dashboard

Na pasta onde o app.py está, rodar comando abaixo no terminal

```bash
streamlit run app.py
```



