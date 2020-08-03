# Introdução

Este repositório foi criado para armazenar os notebooks e scripts para o data challend Santander segunda edição. Neste 

## Descrição do projeto

Fizemos analise de tal e tal e criamos um dashboard para isso e isso

## Dashbord na web

[site](https://business-data-analysis.herokuapp.com/)

## Technologies
* Python 3
* Plotly
* Jupyter Notebook
* Aquela ferramenta para fazer o dashboard

## Datasets
1. Yahoo Finanças:
  * [BOVA11](https://br.financas.yahoo.com/quote/BOVA11.SA/history?p=BOVA11.SA). 
  * [BTOW3](https://br.financas.yahoo.com/quote/BTOW3.SA/history?p=BTOW3.SA&.tsrc=fin-srch).
  * [VVAR3](https://br.financas.yahoo.com/quote/VVAR3.SA/history?p=VVAR3.SA&.tsrc=fin-srch).
  * [MGLU3](https://br.financas.yahoo.com/quote/MGLU3.SA/history?p=MGLU3.SA&.tsrc=fin-srch).
2. [Brazilian E-Commerce Public Dataset by Olist](https://www.kaggle.com/olistbr/brazilian-ecommerce)
3. 

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



