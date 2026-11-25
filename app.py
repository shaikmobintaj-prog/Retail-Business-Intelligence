import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------
# PAGE SETTINGS
# -----------------------------------
st.set_page_config(
    page_title="Retail BI Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------------
# TITLE
# -----------------------------------
st.title("📊 Retail Business Intelligence Dashboard")
st.write("Retail Sales, Profit and Business Performance Analysis")

# -----------------------------------
# LOAD DATA
# -----------------------------------
df = pd.read_csv("retail_data_30.csv")

# -----------------------------------
# DATA CALCULATIONS
# -----------------------------------
df["Sales"] = df["Quantity"] * df["Price"]

df["Profit"] = df["Quantity"] * (df["Price"] - df["Cost"])

df["Profit_Margin"] = np.where(
    df["Sales"] != 0,
    (df["Profit"] / df["Sales"]) * 100,
    0
)

# -----------------------------------
# OOP CLASS
# -----------------------------------
class RetailBusiness:

    def __init__(self, data):
        self.data = data

    def total_sales(self):
        return self.data["Sales"].sum()

    def total_profit(self):
        return self.data["Profit"].sum()

    def total_orders(self):
        return len(self.data)

    def total_quantity(self):
        return self.data["Quantity"].sum()

    def average_sales(self):
        return self.data["Sales"].mean()

    def best_product(self):
        return self.data.groupby("Product")["Sales"].sum().idxmax()

    def best_region(self):
        return self.data.groupby("Region")["Sales"].sum().idxmax()


retail = RetailBusiness(df)

# -----------------------------------
# SIDEBAR FILTERS
# -----------------------------------
st.sidebar.header("🔎 Dashboard Filters")

selected_region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + list(df["Region"].unique())
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + list(df["Category"].unique())
)

# -----------------------------------
# FILTER DATA
# -----------------------------------
filtered_df = df.copy()

if selected_region != "All":
    filtered_df = filtered_df[
        filtered_df["Region"] == selected_region
    ]

if selected_category != "All":
    filtered_df = filtered_df[
        filtered_df["Category"] == selected_category
    ]

# -----------------------------------
# BUSINESS SUMMARY
# -----------------------------------
st.subheader("📈 Business Summary")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"₹{filtered_df['Sales'].sum():,.0f}"
)

col2.metric(
    "Total Profit",
    f"₹{filtered_df['Profit'].sum():,.0f}"
)

col3.metric(
    "Total Orders",
    len(filtered_df)
)

col4.metric(
    "Quantity Sold",
    int(filtered_df["Quantity"].sum())
)

col5, col6 = st.columns(2)

col5.metric(
    "Average Sales",
    f"₹{filtered_df['Sales'].mean():,.2f}"
)

col6.metric(
    "Profit Margin",
    f"{filtered_df['Profit_Margin'].mean():.2f}%"
)

st.divider()

# -----------------------------------
# PRODUCT SALES ANALYSIS
# -----------------------------------
st.subheader("🛍️ Product Sales Analysis")

product_sales = (
    filtered_df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(product_sales)

# -----------------------------------
# CATEGORY ANALYSIS
# -----------------------------------
st.subheader("📦 Category Sales Analysis")

category_sales = filtered_df.groupby("Category")["Sales"].sum()

if not category_sales.empty:

    fig1, ax1 = plt.subplots()

    ax1.pie(
        category_sales,
        labels=category_sales.index,
        autopct="%1.1f%%"
    )

    ax1.set_title("Category Sales Distribution")

    st.pyplot(fig1)

# -----------------------------------
# REGION ANALYSIS
# -----------------------------------
st.subheader("🌍 Region Wise Sales")

region_sales = filtered_df.groupby("Region")["Sales"].sum()

st.bar_chart(region_sales)

# -----------------------------------
# PROFIT ANALYSIS
# -----------------------------------
st.subheader("💰 Product Wise Profit")

profit_data = (
    filtered_df.groupby("Product")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(profit_data)

# -----------------------------------
# SALES VS PROFIT
# -----------------------------------
st.subheader("📊 Sales vs Profit Analysis")

if not filtered_df.empty:

    fig2, ax2 = plt.subplots()

    sns.scatterplot(
        data=filtered_df,
        x="Sales",
        y="Profit",
        ax=ax2
    )

    ax2.set_title("Sales vs Profit")

    st.pyplot(fig2)

# -----------------------------------
# DATA TABLE
# -----------------------------------
st.subheader("📋 Retail Dataset")

st.dataframe(
    filtered_df,
    use_container_width=True
)

# -----------------------------------
# DOWNLOAD CSV
# -----------------------------------
csv_data = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Analysis CSV",
    data=csv_data,
    file_name="retail_analysis_results.csv",
    mime="text/csv"
)

# -----------------------------------
# BUSINESS INSIGHTS
# -----------------------------------
st.subheader("💡 Business Insights")

if not filtered_df.empty:

    best_product = (
        filtered_df.groupby("Product")["Sales"]
        .sum()
        .idxmax()
    )

    best_region = (
        filtered_df.groupby("Region")["Sales"]
        .sum()
        .idxmax()
    )

    best_category = (
        filtered_df.groupby("Category")["Sales"]
        .sum()
        .idxmax()
    )

    st.write("🏆 Best Selling Product:", best_product)

    st.write("🌍 Best Performing Region:", best_region)

    st.write("📦 Best Selling Category:", best_category)

    st.write(
        "💰 Total Business Profit:",
        f"₹{filtered_df['Profit'].sum():,.2f}"
    )

else:

    st.warning("No data available for the selected filters.")

# -----------------------------------
# SUCCESS MESSAGE
# -----------------------------------
st.success("Retail BI Dashboard Loaded Successfully! 🎉")