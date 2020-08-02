import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from src.utils import fill_date_range, dict_dayofweek

def plot_indicators(x, y):
    x_max = x*1.2
    y_max = y*1.4

    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=x,
            mode='gauge+number',
            title=dict(text='Indicador 1'),
            gauge=dict(axis=dict(range=[None, x_max])),
            domain=dict(x=[0,0.4])
        )
    )

    fig.add_trace(
        go.Indicator(
            value=y,
            mode='gauge+number',
            title=dict(text='Indicador 2'),
            gauge=dict(axis=dict(range=[None, y_max])),
            domain=dict(x=[0.5,1])
        )
    )

    fig.update_layout(height=250)

    return fig

def plot_map(data):
    fig = px.scatter_mapbox(
        data, lat="geolocation_lat", lon="geolocation_lng", hover_name="customer_unique_id",
        color_discrete_sequence=["darkred"], size="price", opacity=0.5, zoom=3, height=300
    )
    
    fig.update_layout(height=600, mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def plot_density_map(data):
    fig = go.Figure(
        go.Densitymapbox(
            lat=data['geolocation_lat'], lon=data['geolocation_lng'],
            radius=10
        )
    )

    fig.update_layout(mapbox_style="carto-positron", mapbox_zoom=3,
                    mapbox_center_lat=-14.003231,
                    mapbox_center_lon=-59.1690272)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

def plot_revenue_monthly(data):
    ts_revenue = data.groupby(data['shipping_limit_date'])['price'].sum()
    
    ts_revenue = fill_date_range(ts_revenue)

    ts_revenue = ts_revenue.resample('M').sum()
    fig = go.Figure(
        go.Bar(x=ts_revenue.index, y=ts_revenue, text=ts_revenue, 
            texttemplate='R$ %{text:.2f}', textposition='outside')

    )
    fig.update_layout(height=500, yaxis=dict(title='Receita (R$)'), xaxis=dict(title='Mês'))

    return fig

def plot_orders_period(ts_orders, period='M'):
    if period == 'M':
        period_name = 'Mês'
    elif period == 'W':
        period_name = 'Semana'
    else:
        period_name = 'Dia'

    ts_orders_month = ts_orders.resample(period).sum()

    fig = go.Figure(
        go.Bar(x=ts_orders_month.index, y=ts_orders_month, text=ts_orders_month, textposition='outside')

    )
    fig.update_layout(height=500, yaxis=dict(title='Pedidos'), xaxis=dict(title=period_name))

    return fig

def plot_orders_dayofweek(ts_orders):
    df_dayofweek = ts_orders.reset_index()
    df_dayofweek.columns = ['data', 'vendas']
    df_dayofweek['data'] = df_dayofweek['data'].dt.dayofweek
    df_dayofweek.sort_values('data', inplace=True)
    df_dayofweek['data'] = df_dayofweek['data'].replace(dict_dayofweek)
    df_dayofweek = df_dayofweek.groupby('data', sort=False)['vendas'].sum()

    fig = go.Figure(
        go.Bar(x=df_dayofweek.index, y=df_dayofweek, text=df_dayofweek, textposition='outside')
    )

    fig.update_layout(height=500, yaxis=dict(title='Pedidos'), xaxis=dict(title='Dia da semana'))

    return fig

def plot_products_sold(data):
    df_product_sold_count = data['product_id'].value_counts(ascending=True)

    fig = go.Figure(
        go.Bar(y=df_product_sold_count.index, x=df_product_sold_count, text=df_product_sold_count, textposition='outside', orientation='h')

    )

    fig.update_layout(height=500, yaxis=dict(title='Produto'), xaxis=dict(title='Quantidade vendida'))
    return fig

def plot_hist_products_orders(data):
    df_order_products_count = data['order_id'].value_counts()

    fig = px.histogram(df_order_products_count)

    fig.update_layout(yaxis=dict(title='Contagem de ordens'), xaxis=dict(title='Quantidade de produtos'), showlegend=False)

    return fig

def plot_sales_location(data):
    df_state_count = data.groupby('geolocation_state')['order_id'].nunique()
    df_state_count.sort_values(inplace=True)
    
    fig = go.Figure(
        go.Bar(y=df_state_count.index, x=df_state_count, text=df_state_count, textposition='outside', orientation='h')
            
    )
    fig.update_layout(height=500, yaxis=dict(title='Estado'), xaxis=dict(title='Pedidos'), showlegend=False)

    return fig