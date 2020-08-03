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
    st.sidebar.title('Dado Fácil')

    data = pd.DataFrame()
    uploaded_file = st.sidebar.file_uploader('Importar planilha:', type=['xlsx'])

    if uploaded_file:
        data = pd.read_excel(uploaded_file)
        data = prepare_data_sheet(data)
    else:
        data = get_olist_data()

    return data

def get_indicators(data):
    ts_revenue = data.groupby(data['shipping_limit_date'])['price'].sum()
    ts_revenue = fill_date_range(ts_revenue)
    ts_revenue = ts_revenue.resample('M').sum()
    revenue_current_month = ts_revenue.iloc[-1]

    ts_orders = data.groupby('shipping_limit_date')['order_id'].nunique()
    ts_orders = fill_date_range(ts_orders)
    ts_orders_month = ts_orders.resample('M').sum()
    orders_current_month = ts_orders_month.iloc[-1]

    return revenue_current_month, orders_current_month 

def get_reviews(data, ascending=False):
    df_reviews = data.dropna(subset=['review_comment_title', 'review_comment_message']).sort_values(by=['review_score', 'shipping_limit_date'], ascending=ascending).iloc[:3]
    # title, comment = df_reviews.iloc[0]['review_comment_title'], df_reviews.iloc[0]['review_comment_message']
    reviews = df_reviews[['review_comment_title', 'review_comment_message', 'review_score']].values
    return reviews


def filter_home(data):
    products = data['product_id'].unique()
    products_filter = st.sidebar.multiselect('Filtrar produtos:', products)
    if products_filter:
        data = data[data['product_id'].isin(products_filter)]

    states = data['geolocation_state'].unique()
    states_filter = st.sidebar.multiselect('Filtrar estados:', states)
    if products_filter:
        data = data[data['geolocation_state'].isin(states_filter)]

    limits_price = (0.0, data['price'].max())
    price_filter = st.sidebar.slider(label='Limitar preço', min_value=0.0, max_value=data['price'].max(), value=limits_price)
    if price_filter != limits_price:
        data = data[(data['price'] >= limits_price[0]) & data['price'] <= limits_price[1]]
    
    return data

def load_home(data):
    st.write("## Informações sobre as vendas")
    data = filter_home(data)

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

    # st.sidebar.markdown("---")


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
    if 'review_id' in data.columns:
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
    else:
        st.info("Sem avaliações na base de dados")
    
def main():
    st.title('Dado Fácil')
    data = create_default_menu()

    st.sidebar.markdown('---')
    st.sidebar.markdown('Baixar template')
    download_button = st.sidebar.button('Download')
    if download_button:
        df_template = pd.read_excel('data/Planilha Template.xlsx')
        get_download_excel(df_template)
    st.sidebar.markdown('---')

    page = st.sidebar.radio('Selecionar página:', ['Vendas', 'Perfil dos Clientes', 'Avaliações'])
    
    if page == 'Vendas':
        load_home(data)
    elif page == 'Perfil dos Clientes':
        load_customers(data)
    elif page == 'Avaliações':
        load_reviews(data)
    

    
    


if __name__ == "__main__":
    main()