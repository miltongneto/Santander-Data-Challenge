import pandas as pd
import streamlit as st

st.cache
def get_olist_data():
    df_products = pd.read_csv('../data/olist/olist_products_dataset.csv')
    df_orders_items = pd.read_csv('../data/olist/olist_order_items_dataset.csv')
    df_orders_dataset = pd.read_csv('../data/olist/olist_orders_dataset.csv')
    df_customers = pd.read_csv('../data/olist/olist_customers_dataset.csv')
    df_geolocation = pd.read_csv('../data/olist/olist_geolocation_dataset.csv')


    df_prod_filtered = df_products[df_products['product_category_name'] == 'beleza_saude']

    df_orders_items_filtered = df_orders_items[df_orders_items['product_id'].isin(df_prod_filtered['product_id'].unique())]

    df_orders_items_seller = df_orders_items_filtered[df_orders_items_filtered['seller_id'] == '42b729f859728f5079499127a9c2ef37']

    df_oders_filtered = pd.merge(df_orders_items_seller, df_orders_dataset[['order_id','customer_id', 'order_purchase_timestamp']], on='order_id')
    df_oders_filtered = pd.merge(df_oders_filtered, df_customers, on='customer_id')

    df_geolocation = df_geolocation.drop_duplicates(subset=['geolocation_lat', 'geolocation_lng'])
    df_geolocation = df_geolocation.drop_duplicates(subset=['geolocation_zip_code_prefix'])

    df_oders_filtered = pd.merge(df_oders_filtered, df_geolocation, left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix')


    df_oders_filtered['shipping_limit_date'] = pd.to_datetime(df_oders_filtered['shipping_limit_date'])
    df_oders_filtered['shipping_limit_date'] = df_oders_filtered['shipping_limit_date'].dt.to_period('D').dt.to_timestamp()

    return df_oders_filtered