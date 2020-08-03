import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
from plotly.subplots import make_subplots
from src.utils import fill_date_range, dict_dayofweek, load_stopwords
from wordcloud import WordCloud


def plot_indicators(x, y):
    x_max = x*1.1
    y_max = y*1.2

    fig = go.Figure()

    fig.add_trace(
        go.Indicator(
            value=x,
            mode='gauge+number',
            number=dict(prefix='R$ '),
            title=dict(text='<b>Receita (R$)</b>'),
            gauge=dict(axis=dict(range=[None, x_max]), bar=dict(color='#3366CC')),
            domain=dict(x=[0,0.4])
        )
    )

    fig.add_trace(
        go.Indicator(
            value=y,
            mode='gauge+number',
            title=dict(text='<b>Quantidade de ordens</b>'),
            gauge=dict(axis=dict(range=[None, y_max]), bar=dict(color='#3366CC')),
            domain=dict(x=[0.5,0.9])
        )
    )

    fig.update_layout(height=200, margin=dict(t=20, b=0))

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


def plot_review_count(data):
    reviews_count = data.drop_duplicates(subset=['order_id'])['price'].notnull().sum()
    reviews_percentage = reviews_count / data.drop_duplicates(subset=['order_id']).shape[0]
    reviews_percentage = reviews_percentage * 100

    labels = ['Avaliados','Não avaliados']
    values = [reviews_percentage, 100 - reviews_percentage]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values)])

    return fig

def plot_review_count_details(data):
    df_reviews_count = data.drop_duplicates(subset=['order_id'])[['review_score', 'review_id', 'review_comment_message']].groupby('review_score').count()
    
    fig = go.Figure()

    fig.add_trace(
        go.Bar(x=df_reviews_count.index, y=df_reviews_count['review_id'], name='Avaliações')
    )

    fig.add_trace(
        go.Bar(x=df_reviews_count.index, y=df_reviews_count['review_comment_message'], name='Avaliações com mensagens')
    )

    # margin=dict(l=0,r=0), legend=dict(x=-1.2, y=1.2), legend_orientation='h'
    fig.update_layout(height=500, width=700, barmode='overlay', yaxis=dict(title='Quantidade'), xaxis=dict(title='Nota da avaliação'))
    
    return fig

def plot_wordcloud(data, score_level='bad'):
    stopwords = load_stopwords()
    
    if score_level == 'bad':
        companies_filtered_type = data[data["review_score"] <= 3].dropna(subset=['review_comment_message'])
    else:
        companies_filtered_type = data[data["review_score"] > 3].dropna(subset=['review_comment_message'])

    wordcloud = WordCloud(stopwords = stopwords).generate(' '.join(companies_filtered_type['review_comment_message']))
    
    plt.imshow(wordcloud)
    plt.axis("off")


def plot_genre(data):
    print(data)
    df_sex_count = data['sex'].value_counts()

    fig = go.Figure(data=[go.Pie(labels=df_sex_count.index, values=df_sex_count)])
    return fig

def plot_age(data):
    df_age_count = data['age'].value_counts()
    df_age_count = df_age_count.loc[['Até 17 anos', 'De 18 a 24 anos', 'De 25 a 35 anos', 'De 36 a 50 anos', 'A partir de 51 anos']]

    fig = go.Figure(
            go.Bar(y=df_age_count.index, x=df_age_count, text=df_age_count, textposition='outside', orientation='h')
                
    )
    return fig

def plot_channel_purchase(data):
    df_social_media_count = data['channel'].value_counts()
    df_social_media_percent = df_social_media_count / data.shape[0]
    df_social_media_percent = (df_social_media_percent * 100).round(2)

    fig = go.Figure(
            go.Bar(
                y=df_social_media_percent.index, x=df_social_media_percent,
                texttemplate='%{text}%', text=df_social_media_percent,
                textposition='outside', orientation='h'
            )
    )

    fig.update_layout(
        height=500, yaxis=dict(title='Canais de compra'), 
        xaxis=dict(title='Percentual de utilização', range=[0, df_social_media_percent.max() + 5]))

    return fig

def plot_social_media_usage(data):
    df_media = pd.Series(data['social_media'].apply(lambda x: x.split(', ')).sum()).value_counts()
    
    fig = go.Figure(
            go.Bar(x=df_media.index, y=df_media, text=df_media, textposition='outside')
                
    )

    fig.update_layout(yaxis=dict(title='Quantidade de usuários'), xaxis=dict(title='Rede Social'))
    return fig

def plot_genre_age(data):
    df_genre_age = data.groupby(['age'])['sex'].value_counts(normalize=True).unstack()
    df_genre_age = (df_genre_age * 100).round(2)

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df_genre_age.index, y=df_genre_age['Masculino'], name='Masculino'
        )
    )

    fig.add_trace(
        go.Bar(
            x=df_genre_age.index, y=df_genre_age['Feminino'], name='Feminino'
        )
    )

    fig.update_layout(yaxis=dict(title='Percentual de clientes', ticksuffix='%'), xaxis=dict(title='Faixa etária'), legend_title_text='Sexo')
    return fig