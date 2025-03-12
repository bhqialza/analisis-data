import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import locale

# Konfigurasi Locale untuk Rupiah
locale.setlocale(locale.LC_ALL, 'id_ID.utf8')  # Format Indonesia

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

# Ringkasan Penjualan
total_orders = df_filtered["order_id"].nunique()
total_customers = df_filtered["customer_unique_id"].nunique()
total_sales = df_filtered["payment_value"].sum()

col1, col2, col3 = st.columns(3)
col1.metric("🛒 Total Orders", total_orders)
col2.metric("👥 Unique Customers", total_customers)
col3.metric("💰 Total Sales", locale.currency(total_sales, grouping=True))

# Produk Paling Laris
st.subheader("🔥 Produk Paling Banyak Dibeli")
top_products = df_filtered.groupby("product_category_name_english")["order_item_id"].count().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(y=top_products.index, x=top_products.values, palette="Blues_r", ax=ax)
ax.set_xlabel("Jumlah Pembelian")
ax.set_ylabel("Kategori Produk")
st.pyplot(fig)

# Tren Pembelian dalam 6 Bulan Terakhir
st.subheader("📈 Tren Penjualan")
df_filtered["month"] = df_filtered["order_purchase_timestamp"].dt.to_period("M").astype(str)  # Konversi ke string
monthly_sales = df_filtered.groupby("month")["order_id"].count().reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=monthly_sales, x="month", y="order_id", marker="o", ax=ax)
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah Pesanan")
ax.set_title("Tren Penjualan")
plt.xticks(rotation=45)  # Supaya lebih rapi jika banyak bulan
st.pyplot(fig)

# Kota dengan Pelanggan Terbanyak
st.subheader("🏙️ Kota dengan Pelanggan Terbanyak")
num_cities = st.sidebar.slider("Tampilkan Berapa Kota Teratas?", 5, 20, 10)  # Pilihan jumlah kota
top_cities = df_filtered["customer_city"].value_counts().head(num_cities)

fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(y=top_cities.index, x=top_cities.values, palette="coolwarm", ax=ax)
ax.set_xlabel("Jumlah Pelanggan")
ax.set_ylabel("Kota")
st.pyplot(fig)

# Footer
st.markdown("---")
st.markdown("**Copyright © 2025 M. Baihaqi Alza**")