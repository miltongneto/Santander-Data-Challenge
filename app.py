import streamlit as st
import pandas as pd
import numpy as np

from src.preprocess_olist import get_olist_data
from src.plots import *
from src.utils import dict_columns
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

def load_home(data):

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


def main():
    st.title('Santander Data Challenge')
    data = create_default_menu()

    page = st.sidebar.radio('Selecionar página:', ['Vendas', 'Perfil dos Clientes', 'Avaliações'])
    
    if page == 'Vendas':
        load_home(data)
    


if __name__ == "__main__":
    main()