import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Trust Wallet - Crypto Transaction Analysis",
    page_icon="💰",
    layout="wide"
)

st.title("Trust Wallet - Crypto Transaction Analysis Dashboard")
st.write("Analysis of cryptocurrency transactions from Trust Wallet")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/updated_crypto_transactions.csv')
    df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'])
    df['Month'] = df['Transaction_Date'].dt.strftime('%Y-%m')
    df['Day'] = df['Transaction_Date'].dt.date
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

# Date range filter
min_date = df['Transaction_Date'].min().date()
max_date = df['Transaction_Date'].max().date()
date_range = st.sidebar.date_input(
    "Date Range",
    [min_date, max_date],
    min_value=min_date,
    max_value=max_date
)

if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = df[(df['Transaction_Date'].dt.date >= start_date) & 
                     (df['Transaction_Date'].dt.date <= end_date)]
else:
    filtered_df = df

# Crypto filter
crypto_options = ['All'] + list(df['Crypto'].unique())
selected_crypto = st.sidebar.selectbox("Cryptocurrency", crypto_options)

if selected_crypto != 'All':
    filtered_df = filtered_df[filtered_df['Crypto'] == selected_crypto]

# Platform filter
platform_options = ['All'] + list(df['Platform'].unique())
selected_platform = st.sidebar.selectbox("Platform", platform_options)

if selected_platform != 'All':
    filtered_df = filtered_df[filtered_df['Platform'] == selected_platform]

# KPI Metrics
st.header("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Transaction Value", f"${filtered_df['Total_Value'].sum():,.2f}")

with col2:
    st.metric("Total Transactions", f"{len(filtered_df):,}")

with col3:
    st.metric("Unique Users", f"{filtered_df['User_ID'].nunique():,}")

with col4:
    success_rate = len(filtered_df[filtered_df['Status'] == 'Completed']) / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
    st.metric("Success Rate", f"{success_rate:.1f}%")

# Visualizations
st.header("Transaction Analysis")

# Row 1: Transaction volume and distribution
col1, col2 = st.columns(2)

with col1:
    st.subheader("Transaction Volume Over Time")
    monthly_volume = filtered_df.groupby('Month').agg({
        'Total_Value': 'sum',
        'Transaction_ID': 'count'
    }).rename(columns={'Transaction_ID': 'Count'})
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(monthly_volume.index, monthly_volume['Total_Value'], color='skyblue')
    ax.set_ylabel('Total Value ($)')
    ax.set_xlabel('Month')
    plt.xticks(rotation=45)
    ax2 = ax.twinx()
    ax2.plot(monthly_volume.index, monthly_volume['Count'], color='red', marker='o')
    ax2.set_ylabel('Transaction Count')
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("Transaction Type Distribution")
    type_counts = filtered_df['Transaction_Type'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', 
           startangle=90, colors=sns.color_palette('viridis', len(type_counts)))
    ax.axis('equal')
    plt.tight_layout()
    st.pyplot(fig)

# Row 2: Crypto comparison and Status
col1, col2 = st.columns(2)

with col1:
    st.subheader("Cryptocurrency Comparison")
    crypto_data = filtered_df.groupby('Crypto').agg({
        'Total_Value': 'sum',
        'Transaction_ID': 'count'
    }).rename(columns={'Transaction_ID': 'Count'}).sort_values('Count', ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(crypto_data.index, crypto_data['Total_Value'], color=sns.color_palette('muted', len(crypto_data)))
    ax.set_ylabel('Total Value ($)')
    ax.set_xlabel('Cryptocurrency')
    plt.xticks(rotation=45)
    
    # Add transaction count labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                f"{crypto_data['Count'].iloc[i]}", 
                ha='center', va='bottom', rotation=0)
    
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("Transaction Status")
    status_counts = filtered_df['Status'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=status_counts.index, y=status_counts.values, palette='viridis', ax=ax)
    ax.set_ylabel('Count')
    ax.set_xlabel('Status')
    plt.tight_layout()
    st.pyplot(fig)

# Row 3: Platform analysis
st.subheader("Platform Performance Analysis")
platform_analysis = filtered_df.groupby('Platform').agg({
    'Total_Value': 'sum',
    'Transaction_ID': 'count',
    'User_ID': pd.Series.nunique,
    'Transaction_Fee': 'sum'
}).rename(columns={
    'Transaction_ID': 'Transaction_Count',
    'User_ID': 'Unique_Users'
})

st.dataframe(platform_analysis)

# Row 4: Fee analysis
st.subheader("Fee Analysis")
col1, col2 = st.columns(2)

with col1:
    fee_by_crypto = filtered_df.groupby('Crypto').agg({
        'Transaction_Fee': 'sum',
        'Total_Value': 'sum'
    })
    fee_by_crypto['Fee_Percentage'] = (fee_by_crypto['Transaction_Fee'] / fee_by_crypto['Total_Value']) * 100
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=fee_by_crypto.index, y=fee_by_crypto['Fee_Percentage'], palette='coolwarm', ax=ax)
    ax.set_ylabel('Fee Percentage (%)')
    ax.set_xlabel('Cryptocurrency')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    fee_by_type = filtered_df.groupby('Transaction_Type').agg({
        'Transaction_Fee': 'mean',
        'Total_Value': 'mean'
    })
    fee_by_type['Avg_Fee'] = fee_by_type['Transaction_Fee']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=fee_by_type.index, y=fee_by_type['Avg_Fee'], palette='muted', ax=ax)
    ax.set_ylabel('Average Fee ($)')
    ax.set_xlabel('Transaction Type')
    plt.tight_layout()
    st.pyplot(fig)

# Raw data
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Transaction Data")
    st.dataframe(filtered_df)