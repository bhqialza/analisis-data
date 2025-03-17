import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi Halaman
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# Load Data dengan Cache
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv", parse_dates=["order_purchase_timestamp"])
    return df

df = load_data()

# Header Dashboard
st.title("📊 E-Commerce Sales Dashboard")
st.markdown("---")

# Sidebar - Filter Data
st.sidebar.header("📌 Filter Data")

# Filter Tanggal
start_date = st.sidebar.date_input("Start Date", df["order_purchase_timestamp"].min())
end_date = st.sidebar.date_input("End Date", df["order_purchase_timestamp"].max())

df_filtered = df[(df["order_purchase_timestamp"] >= pd.to_datetime(start_date)) & 
                 (df["order_purchase_timestamp"] <= pd.to_datetime(end_date))]

# Jika data kosong setelah filter
if df_filtered.empty:
    st.warning("⚠️ Tidak ada data yang tersedia untuk rentang waktu ini. Silakan pilih rentang waktu lain.")
    st.stop()

# Ringkasan Penjualan
total_orders = df_filtered["order_id"].nunique()
total_customers = df_filtered["customer_unique_id"].nunique()
total_sales = df_filtered["payment_value"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("🛒 Total Orders", total_orders)
col2.metric("👥 Unique Customers", total_customers)
col3.metric("💰 Total Sales", f"Rp {total_sales:,.2f}")

# 🔥 Produk Paling Banyak Dibeli
st.subheader("🔥 Produk Paling Banyak Dibeli dalam 6 Bulan Terakhir")
top_products = df_filtered.groupby("product_id")["order_item_id"].count().sort_values(ascending=False).head(10).reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=top_products, x="product_id", y="order_item_id", color="royalblue", ax=ax)
ax.set_xlabel("Product ID")
ax.set_ylabel("Jumlah Pembelian")
ax.set_title("Top 10 Produk Paling Banyak Dibeli dalam 6 Bulan Terakhir")
plt.xticks(rotation=45)
st.pyplot(fig)

# 📈 Tren Pembelian dalam 6 Bulan Terakhir
st.subheader("📈 Tren Pembelian dalam 6 Bulan Terakhir")
df_filtered["purchase_month"] = df_filtered["order_purchase_timestamp"].dt.to_period("M").astype(str)
monthly_trend = df_filtered.groupby("purchase_month")["order_id"].count().reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=monthly_trend, x="purchase_month", y="order_id", marker="o", linewidth=2, color="b", ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Pembelian")
ax.set_title("Tren Pembelian dalam 6 Bulan Terakhir")
plt.xticks(rotation=45)
st.pyplot(fig)

# 🏷️ Pola Pembelian Berdasarkan Kategori
st.subheader("🏷️ Pola Pembelian Berdasarkan Kategori")
category_trend = df_filtered.groupby("product_category_name")["order_item_id"].count().sort_values(ascending=False).head(10).reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=category_trend, x="product_category_name", y="order_item_id", hue="product_category_name", dodge=False, palette="coolwarm", ax=ax)
ax.set_xlabel("Kategori Produk")
ax.set_ylabel("Jumlah Pembelian")
ax.set_title("Top 10 Kategori Produk Paling Banyak Dibeli")
plt.xticks(rotation=45)
st.pyplot(fig)

# 🔄 Retensi Pelanggan Berdasarkan Kategori Produk
st.subheader("🔄 Kategori Produk dengan Tingkat Retensi Pelanggan Tertinggi")
customer_retention = df_filtered.groupby("product_category_name")["customer_unique_id"].nunique().sort_values(ascending=False).head(10).reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=customer_retention, x="product_category_name", y="customer_unique_id", hue="product_category_name", dodge=False, palette="viridis", ax=ax)
ax.set_xlabel("Kategori Produk")
ax.set_ylabel("Jumlah Pelanggan Unik")
ax.set_title("Kategori Produk dengan Tingkat Retensi Pelanggan Tertinggi")
plt.xticks(rotation=45)
st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("**Copyright © 2025 M. Baihaqi Alza**")
