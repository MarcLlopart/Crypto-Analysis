import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from datetime import datetime
from matplotlib.ticker import FuncFormatter

plt.style.use('ggplot')

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
    st.metric("Total Transaction Value", f"${filtered_df[filtered_df['Status'] == 'Completed']['Total_Value'].sum():,.2f}")

with col2:
    st.metric("Total Transactions", f"{len(filtered_df):,}")

with col3:
    st.metric("Unique Users", f"{filtered_df['User_ID'].nunique():,}")

with col4:
    success_rate = len(filtered_df[filtered_df['Status'] == 'Completed']) / len(filtered_df) * 100 if len(filtered_df) > 0 else 0
    st.metric("Success Rate", f"{success_rate:.1f}%")

# Helper function for formatting large numbers
def format_with_units(x, pos):
    if x >= 1e9:
        return f'{x*1e-9:.1f}B'
    elif x >= 1e6:
        return f'{x*1e-6:.1f}M'
    elif x >= 1e3:
        return f'{x*1e-3:.1f}K'
    else:
        return f'{x:.1f}'

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
    bars = ax.bar(monthly_volume.index, monthly_volume['Total_Value'], color='steelblue', label='Total Value')
    ax.set_ylabel('Total Value ($)')
    ax.set_xlabel('Month')
    ax.yaxis.set_major_formatter(FuncFormatter(format_with_units))
    plt.xticks(rotation=45)
    
    ax2 = ax.twinx()
    line = ax2.plot(monthly_volume.index, monthly_volume['Count'], color='navy', marker='o', linewidth=2, label='Transaction Count')
    ax2.set_ylabel('Transaction Count')
    ax2.yaxis.set_major_formatter(FuncFormatter(format_with_units))
    
    # Combine legends from both axes
    lines, labels = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc='upper left')
    
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("Transaction Type Distribution")
    type_counts = filtered_df['Transaction_Type'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = sns.color_palette('Blues', len(type_counts))
    wedges, texts, autotexts = ax.pie(
        type_counts, 
        labels=None,
        autopct='%1.1f%%', 
        startangle=90, 
        colors=colors,
        wedgeprops={'edgecolor': 'w'}
    )
    
    # Enhance the text visibility
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
    
    ax.axis('equal')
    
    # Add a legend outside the pie
    ax.legend(
        wedges, 
        type_counts.index, 
        title="Transaction Types",
        loc="center left",
        bbox_to_anchor=(1, 0, 0.5, 1)
    )
    
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
    colors = sns.color_palette('Blues', len(crypto_data))
    bars = ax.bar(crypto_data.index, crypto_data['Total_Value'], color=colors)
    ax.set_ylabel('Total Value ($)')
    ax.set_xlabel('Cryptocurrency')
    ax.yaxis.set_major_formatter(FuncFormatter(format_with_units))
    plt.xticks(rotation=45)
    
    # Add transaction count labels
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 5,
                f"{format_with_units(crypto_data['Count'].iloc[i], None)}", 
                ha='center', va='bottom', rotation=0)
    
    # Create a color gradient legend
    sm = plt.cm.ScalarMappable(cmap=plt.cm.Blues, norm=plt.Normalize(0, len(crypto_data)-1))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Popularity (Transaction Count)')
    
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("Transaction Status")
    status_counts = filtered_df['Status'].value_counts()
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = sns.color_palette('Blues', len(status_counts))
    bars = sns.barplot(x=status_counts.index, y=status_counts.values, palette=colors, ax=ax)
    
    # Add count labels on top of each bar
    for i, bar in enumerate(ax.patches):
        ax.text(
            bar.get_x() + bar.get_width()/2.,
            bar.get_height() + 5,
            format_with_units(status_counts.values[i], None),
            ha='center', va='bottom'
        )
    
    ax.set_ylabel('Count')
    ax.set_xlabel('Status')
    ax.yaxis.set_major_formatter(FuncFormatter(format_with_units))
    
    # Add a legend
    handles = [plt.Rectangle((0,0),1,1, color=colors[i]) for i in range(len(status_counts))]
    plt.legend(handles, status_counts.index, title="Transaction Status")
    
    plt.tight_layout()
    st.pyplot(fig)

# Row 3: Platform analysis
st.subheader("Platform Performance Analysis")
platform_analysis = filtered_df[filtered_df['Status'] == 'Completed'].groupby('Platform').agg({
    'Total_Value': 'sum',
    'Transaction_ID': 'count',
    'User_ID': pd.Series.nunique,
    'Transaction_Fee': 'sum'
}).rename(columns={
    'Transaction_ID': 'Transaction_Count',
    'User_ID': 'Unique_Users'
})

# Format the values in the dataframe for better readability
for col in ['Total_Value', 'Transaction_Fee']:
    platform_analysis[col] = platform_analysis[col].map('${:,.2f}'.format)

for col in ['Transaction_Count', 'Unique_Users']:
    platform_analysis[col] = platform_analysis[col].map('{:,}'.format)

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
    colors = sns.color_palette('Blues_r', len(fee_by_crypto))  # Reversed blues for emphasis on higher values
    bars = sns.barplot(x=fee_by_crypto.index, y=fee_by_crypto['Fee_Percentage'], palette=colors, ax=ax)
    
    # Add percentage labels on top of each bar
    for i, bar in enumerate(ax.patches):
        ax.text(
            bar.get_x() + bar.get_width()/2.,
            bar.get_height() + 0.1,
            f"{fee_by_crypto['Fee_Percentage'].iloc[i]:.2f}%",
            ha='center', va='bottom'
        )
    
    ax.set_ylabel('Fee Percentage (%)')
    ax.set_xlabel('Cryptocurrency')
    plt.xticks(rotation=45)
    
    # Add a legend
    handles = [plt.Rectangle((0,0),1,1, color=colors[i]) for i in range(len(fee_by_crypto))]
    plt.legend(handles, fee_by_crypto.index, title="Cryptocurrencies")
    
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    fee_by_type = filtered_df.groupby('Transaction_Type').agg({
        'Transaction_Fee': 'mean',
        'Total_Value': 'mean'
    })
    fee_by_type['Avg_Fee'] = fee_by_type['Transaction_Fee']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    colors = sns.color_palette('Blues', len(fee_by_type))
    bars = sns.barplot(x=fee_by_type.index, y=fee_by_type['Avg_Fee'], palette=colors, ax=ax)
    
    # Add fee amount labels on top of each bar
    for i, bar in enumerate(ax.patches):
        ax.text(
            bar.get_x() + bar.get_width()/2.,
            bar.get_height() + 0.2,
            f"${fee_by_type['Avg_Fee'].iloc[i]:.2f}",
            ha='center', va='bottom'
        )
    
    ax.set_ylabel('Average Fee ($)')
    ax.set_xlabel('Transaction Type')
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'${x:.2f}'))
    
    # Add a legend
    handles = [plt.Rectangle((0,0),1,1, color=colors[i]) for i in range(len(fee_by_type))]
    plt.legend(handles, fee_by_type.index, title="Transaction Types")
    
    plt.tight_layout()
    st.pyplot(fig)

# Raw data
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Transaction Data")
    st.dataframe(filtered_df)