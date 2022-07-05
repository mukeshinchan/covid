import streamlit as st 
import pandas as pd 
import plotly.express as px
import datetime
confrimed_covid = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'

confrimed_df = pd.read_csv(confrimed_covid)

new_df = confrimed_df.melt(id_vars=['Country/Region','Province/State','Lat','Long'])

temp_val = 0
def dailyCaseClac(x):
    global temp_val
    currentVal = x - temp_val
    temp_val = x
    return int(currentVal)
page_value  = st.sidebar.radio('Select Page', ['Cases','Deaths'])
if page_value == 'Cases':
    country_list = list(new_df['Country/Region'].unique())
    selectedCountry  = st.sidebar.selectbox('Select Country', country_list)
    new_df['Daily_Case'] = new_df[new_df['Country/Region'] == selectedCountry]['value'].apply(lambda x: int(dailyCaseClac(x)))
    new_df['Daily_Case'] = new_df['Daily_Case'].fillna(0).astype(int)
    df_selectedCountry = new_df[new_df['Country/Region'] == selectedCountry]
    total=list(df_selectedCountry['value'])
    now=(list(df_selectedCountry['Daily_Case']))
    col1,col2= st.columns(2)
    with col1:
        st.header('Total Cases')
        st.subheader(total[-1])
    with col2:
        st.header('Active Cases') 
        st.subheader(now[-1])
    fig = px.line(df_selectedCountry,x = 'variable',y = 'Daily_Case',)
    fig.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
    st.plotly_chart(fig)
if page_value == 'Deaths':
    death_df=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
    death_pvt_df=death_df.melt(id_vars=['Province/State','Country/Region','Lat','Long'],var_name='Date',value_name='RUNNING_TOTAL')
    country_list = list(new_df['Country/Region'].unique())
    selectedCountry2 = st.sidebar.selectbox('Select Country', country_list)
    death_pvt_df['Daily_Case'] = death_pvt_df[death_pvt_df['Country/Region'] == selectedCountry2]['RUNNING_TOTAL'].apply(lambda x: int(dailyCaseClac(x)))
    death_pvt_df['Daily_Case'] = death_pvt_df['Daily_Case'].fillna(0).astype(int)
    df_selectedCountry2 = death_pvt_df[death_pvt_df['Country/Region'] == selectedCountry2]
    now=(list(df_selectedCountry2['RUNNING_TOTAL']))
    col1,col2= st.columns(2)
    with col1:
        st.header('Total Death')
        st.subheader(now[-1])
    fig2=px.line(df_selectedCountry2,x='Date',y='Daily_Case')
    fig2.update_layout(xaxis=dict(showgrid=False),yaxis=dict(showgrid=False))
    st.plotly_chart(fig2)
    
    
