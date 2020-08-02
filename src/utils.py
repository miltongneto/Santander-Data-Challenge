import pandas as pd
import base64
from io import BytesIO
import streamlit as st

dict_columns = {
    'código da venda': 'order_id',
    'código do produto': 'product_id',
    'preço': 'price',
    'data/hora da compra': 'shipping_limit_date',
    'código do cliente': 'customer_unique_id',
    'cidade do cliente': 'geolocation_city',
    'estado do cliente': 'geolocation_state',
    'latitude': 'geolocation_lat',
    'longitude': 'geolocation_lng'
}

dict_dayofweek = {
    0: 'Domingo',
    1: 'Segunda',
    2: 'Terça',
    3: 'Quarta',
    4: 'Quinta',
    5: 'Sexta',
    6: 'Sábado',
}

def fill_date_range(ts, add_delay=True):
    if add_delay:
        start_ts = ts.index[0] - pd.to_timedelta('1 day')
    else:
        start_ts = ts.index[0]

    ts = ts.reindex(pd.date_range(start=start_ts, end=ts.index[-1]))
    ts.fillna(0,inplace=True)
    return ts

def get_download_excel(data):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    data.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    excel = output.getvalue()
    b64 = base64.b64encode(excel).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="Template.xlsx">Download XLSX File</a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)
