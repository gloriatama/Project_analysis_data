import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency

sns.set(style='dark')

def create_daily_orders_df(df):
    daily_orders_df = df.resample(rule='D', on='order_date').agg({
        "order_id": "nunique",
        "order_purchase_timestamp": "sum"
    })
    daily_orders_df = daily_orders_df.reset_index()
    daily_orders_df.rename(columns={
        "order_id": "order_delivered_carrier_date",
        "order_purchase_timestamp": "revenue"
    }, inplace=True)
    
    return daily_orders_df

def create_bystatus_df(df):
    bystatus_df = df.groupby(by="order_status").order_id.nunique().reset_index()
    bystatus_df.rename(columns={
        "order_id": "order_purchase_timestamp"
    }, inplace=True)
    
    return bystatus_df

def create_bystate_df(df):
    bystate_df = df.groupby(by="customer_state").customer_id.nunique().reset_index()
    bystate_df.rename(columns={
        "customer_id": "customer_zip_code_prefix"
    }, inplace=True)
    
    return bystate_df

def create_bycity_df(df):
    bycity_df = df.groupby(by="customer_city").customer.nunique().reset_index()
    bycity_df.rename(columns={
        "customer_id": "customer_zip_code_prefix"
    }, inplace=True)
    
    return bycity_df

all_df = pd.read_csv("all_data.csv")

datetime_columns = ["order_delivered_carrier_date", "order_delivered_customer_date"]
all_df.sort_values(by="order_delivered_carrier_date", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])
    
    
min_date = all_df["order_delivered_carrier_date"].min()
max_date = all_df["order_delivered_carrier_datee"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://github.com/dicodingacademy/assets/raw/main/logo.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
main_df = all_df[(all_df["order_delivered_carrier_date"] >= str(start_date)) & 
                (all_df["order_delivered_carrier_date"] <= str(end_date))]
    
daily_orders_df = create_daily_orders_df(main_df)
bystatus_df = create_bystatus_df(main_df)
bystate_df = create_bystate_df(main_df)
bycity_df = create_bycity_df(main_df)

st.header('Dicoding Collection Dashboard :sparkles:')


st.subheader('Daily Orders')
 
col1, col2 = st.columns(2)
 
with col1:
    total_orders = daily_orders_df.order_delivered_carrier_date.sum()
    st.metric("Total order approved", value=total_orders)
 
with col2:
    total_revenue = format_currency(daily_orders_df.revenue.sum(), "AUD", locale='es_CO') 
    st.metric("Total Revenue", value=total_revenue)
 
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    daily_orders_df["order_delivered_carrier_date"],
    daily_orders_df["order_purchased_timestamp"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)



st.subheader("Customer Demographics")
 
col1, col2 = st.columns(2)
 
with col1:
    fig, ax = plt.subplots(figsize=(20, 10))
 
    sns.barplot(
        y="customer_count", 
        x="gender",
        data=bystatus_df.sort_values(by="order_status", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by Status", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
with col2:
    fig, ax = plt.subplots(figsize=(20, 10))
    
    colors = ["#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
 
    sns.barplot(
        y="customer_zip_code_prefix", 
        x="customer_state",
        data=bystate_df.sort_values(by="customer_state", ascending=False),
        palette=colors,
        ax=ax
    )
    ax.set_title("Number of Customer by State", loc="center", fontsize=50)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=35)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)
 
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_zip_code_prefix", 
    y="customer_city",
    data=bystate_df.sort_values(by="customer_city", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customer by City", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)