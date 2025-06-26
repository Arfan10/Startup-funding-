import streamlit as st 
import pandas as pd 
import numpy as np
import plotly.express as px
from collections import  Counter


st.set_page_config(page_title="Indian startup Funding EDA",layout='wide')

#Title 
st.title("Indian Startup Funding Dashboard")

# Load data 
@st.cache_data
def load_data():
    df = pd.read_csv("startup_funding.csv")

    #renaming columns 
    df.rename(columns={
    'InvestmentnType': 'FundingType',
    'Amount in USD': 'Amount',
    'City  Location': 'City',
    'Investors Name': 'Investors',
    'Industry Vertical' :'Industry',
    'Startup Name': 'Startup',
    'Date dd/mm/yyyy': "Date"  
    }, inplace=True)

    df['Amount'] = df['Amount'].astype(str).str.replace(',', '').str.replace('$','').str.strip()
    df = df[df['Amount'].str.replace(' ','').str.isnumeric()]
    df['Amount'] = df['Amount'].astype(float)
    df['Date'] = pd.to_datetime(df['Date'], errors = 'coerce')
    df['Year'] = df['Date'].dt.year
    df['City'] = df ['City'].astype(str).str.strip()

    return df


df = load_data()
# Sidebar Filters 

year_options = df['Year'].dropna().sort_values().unique()
selected_year = st.sidebar.selectbox("Select Year", options=year_options[::-1], index= 0)
filtered_df = df[df['Year'] == selected_year]

st.subheader(f" Data for Year:{selected_year}")


# Top Cities

city_data = filtered_df['City'].value_counts().head(10).reset_index()
city_data.columns = ['City','Counts']
fig1 = px.bar(city_data, x='Counts', y= 'City', orientation='h', title="Top 10 cities by Number of Fundings")
st.plotly_chart(fig1,use_container_width=True)


# Top Industries 
industries_data = filtered_df.groupby('Industry')['Amount'].sum().sort_values(ascending = False).head(10).reset_index()
industries_data.columns = ['Industry','Total Fundings']
fig2 = px.bar(industries_data, x='Total Fundings', y='Industry',orientation='h',title='Top 10 Industries bu=y Funding')
st.plotly_chart(fig2,use_container_width=True)


# Funding Over years 
yearly_data = df.groupby('Year')['Amount'].sum().reset_index()
fig3 = px.line(yearly_data, x = 'Year', y = "Amount", markers= True, title='Total Fundings Over The Years')
st.plotly_chart(fig3, use_container_width=True)

# Top Investors 
investors = df['Investors'].dropna().str.split(', ')
flat = [i.strip() for sublist in investors for i in sublist]
top_investors = Counter(flat).most_common(10)
top_investors_df = pd.DataFrame(top_investors,columns=['Investor','Count'])
fig4 = px.bar(top_investors_df,x='Count',y='Investor', orientation='h', title='Top 10 Active Investors')
st.plotly_chart(fig4, use_container_width=True)

st.markdown("Made By Arfan")