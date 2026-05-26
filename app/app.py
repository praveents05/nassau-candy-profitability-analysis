import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Page Config
st.set_page_config(
    page_title="Nassau Candy Dashboard",
    layout="wide"
)

# Title
st.title("Product Line Profitability & Margin Performance Analysis")

# Load Dataset
import os

current_dir = os.path.dirname(__file__)

csv_path = os.path.join(current_dir, "cleaned_nassau_candy.csv")

df = pd.read_csv(csv_path)

# Sidebar Filters
st.sidebar.header("Filters")

product_search = st.sidebar.text_input(
    "Search Product"
)

division = st.sidebar.multiselect(
    "Select Division",
    options=df['Division'].unique(),
    default=df['Division'].unique()
)

# Filter Data
filtered_df = df[df['Division'].isin(division)]

if product_search:
    filtered_df = filtered_df[
        filtered_df['Product Name']
        .str.contains(product_search, case=False)
    ]

# KPI Section
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Gross Profit'].sum()
avg_margin = filtered_df['Gross Margin %'].mean()

col1, col2, col3 = st.columns(3)

col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Total Profit", f"${total_profit:,.2f}")
col3.metric("Average Margin %", f"{avg_margin:.2f}%")

# Top Profitable Products
st.subheader("Top Profitable Products")

top_products = (
    filtered_df.groupby('Product Name')['Gross Profit']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10,5))

top_products.plot(
    kind='bar',
    ax=ax
)

plt.xticks(rotation=45)

st.pyplot(fig)

st.subheader("Top 10 Products Table")

st.dataframe(
    top_products.reset_index()
)

# Division Analysis
st.subheader("Division Revenue vs Profit")

division_analysis = (
    filtered_df.groupby('Division')[['Sales', 'Gross Profit']]
    .sum()
)

fig2, ax2 = plt.subplots(figsize=(8,5))

division_analysis.plot(
    kind='bar',
    ax=ax2
)

plt.xticks(rotation=0)

st.pyplot(fig2)

st.subheader("Division Sales Contribution")

division_sales = (
    filtered_df.groupby('Division')['Sales']
    .sum()
)

fig_pie, ax_pie = plt.subplots()

ax_pie.pie(
    division_sales,
    labels=division_sales.index,
    autopct='%1.1f%%'
)

st.pyplot(fig_pie)

# Cost vs Sales Scatter Plot
st.subheader("Cost vs Sales Analysis")

fig3, ax3 = plt.subplots(figsize=(8,5))

sns.scatterplot(
    data=filtered_df,
    x='Cost',
    y='Sales',
    ax=ax3
)

st.pyplot(fig3)

# Pareto Analysis
st.subheader("Pareto Profit Analysis")

pareto = (
    filtered_df.groupby('Product Name')['Gross Profit']
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

pareto['Cumulative Profit'] = pareto['Gross Profit'].cumsum()

pareto['Cumulative %'] = (
    pareto['Cumulative Profit']
    / pareto['Gross Profit'].sum()
) * 100

fig4, ax4 = plt.subplots(figsize=(10,5))

ax4.plot(
    pareto['Cumulative %'],
    marker='o'
)

ax4.axhline(
    y=80,
    color='red',
    linestyle='--'
)

st.pyplot(fig4)

st.subheader("Business Recommendations")

st.download_button(
    label="Download Filtered Data",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_data.csv",
    mime="text/csv"
)