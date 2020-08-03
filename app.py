import streamlit as st
import pandas as pd
import numpy as np

from src.preprocess_olist import get_olist_data
from src.plots import *
from src.utils import dict_columns, get_download_excel, get_customers_data
import os


def prepare_data_sheet(data):
    data = data.rename(columns=dict_columns)
    return data

def create_default_menu():
    data = pd.DataFrame()
    uploaded_file = st.sidebar.file_uploader('Importar planilha:', type=['xlsx'])

    if uploaded_file:
        data = pd.read_excel(uploaded_file)
        data = prepare_data_sheet(data)
    else:
        data = get_olist_data()

    return data

def get_indicators(data):
    return 12, 10 

def get_reviews(data, ascending=False):
    df_reviews = data.dropna(subset=['review_comment_title', 'review_comment_message']).sort_values(by=['review_score', 'shipping_limit_date'], ascending=ascending).iloc[:3]
    # title, comment = df_reviews.iloc[0]['review_comment_title'], df_reviews.iloc[0]['review_comment_message']
    reviews = df_reviews[['review_comment_title', 'review_comment_message', 'review_score']].values
    return reviews

def load_home(data):
    st.write("## Informações sobre as vendas")

    x, y = get_indicators(data)
    st.plotly_chart(plot_indicators(x, y))

    st.write('## Receita mensal')
    st.plotly_chart(plot_revenue_monthly(data))

    ts_orders = data.groupby('shipping_limit_date')['order_id'].nunique()
    ts_orders = fill_date_range(ts_orders)
    
    st.write('## Pedidos mensais')
    st.plotly_chart(plot_orders_period(ts_orders, 'M'))

    st.write('## Pedidos semanais')
    st.plotly_chart(plot_orders_period(ts_orders, 'W'))

    st.write('## Pedidos por dia da semana')
    st.plotly_chart(plot_orders_dayofweek(ts_orders))

    st.write('## Produtos vendidos')
    st.plotly_chart(plot_products_sold(data))
    
    st.write('## Distribuição da quantidade de produtos por ordem')
    st.plotly_chart(plot_hist_products_orders(data))
    

    st.write('## Localização dos clientes')
    st.plotly_chart(plot_map(data))

    st.plotly_chart(plot_density_map(data))

    st.write('### Quantidade de pedidos por localização')
    st.plotly_chart(plot_sales_location(data))


def load_customers(data):
    st.write("## Informações dos perfis dos clientes")
    df = get_customers_data()
    print(df.head())

    st.write("### Sexo dos clientes")
    st.plotly_chart(plot_genre(df))

    st.write("### Faixa etária dos clientes")
    st.plotly_chart(plot_age(df))

    st.write("### Distribuição do sexo por faixa etária")
    st.plotly_chart(plot_genre_age(df))

    st.write("### Formas de compra")
    st.plotly_chart(plot_channel_purchase(df))

    st.write("### Redes sociais utilizadas")
    st.plotly_chart(plot_social_media_usage(df))
    


def load_reviews(data):
    st.write("## Informações das avaliações dos clientes")

    st.write("## Porcentagem de produtos avaliados")
    st.plotly_chart(plot_review_count(data))

    st.write("## Avaliação dos produtos por nota")
    st.plotly_chart(plot_review_count_details(data))

    st.write("## Nuvem de Palavras")
    
    st.write("## Palavras para avaliações boas")
    plot_wordcloud(data, 'good')
    st.pyplot()

    st.write("## Palavras para avaliações ruins")
    plot_wordcloud(data, 'bad')
    st.pyplot()

    st.write("## Principais comentários")

    st.write("### Comentários positivos")
    best_reviews = get_reviews(data, False)
    for review in best_reviews:
        st.markdown('#### "{}" - {}'.format(review[0], review[2]))
        st.text('"{}"'.format(review[1]))
        
    st.write("### Comentários negativos")
    worse_reviews = get_reviews(data, True)
    for review in worse_reviews:
        st.markdown('#### "{}" - {}'.format(review[0], review[2]))
        st.text('"{}"'.format(review[1]))
    
def main():
    st.title('Santander Data Challenge')
    data = create_default_menu()

    page = st.sidebar.radio('Selecionar página:', ['Vendas', 'Perfil dos Clientes', 'Avaliações'])
    
    if page == 'Vendas':
        load_home(data)
    elif page == 'Perfil dos Clientes':
        load_customers(data)
    elif page == 'Avaliações':
        load_reviews(data)
    

    st.sidebar.markdown('Baixar template')
    download_button = st.sidebar.button('Download')
    if download_button:
        df_template = pd.read_excel('data/Planilha Template.xlsx')
        get_download_excel(df_template)
    


if __name__ == "__main__":
    main()