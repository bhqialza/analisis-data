import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi halaman Streamlit
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# Tambahkan sidebar dengan logo & informasi tambahan
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/1177/1177568.png", width=100)
st.sidebar.title("📊 E-Commerce Dashboard")
st.sidebar.write("Dibuat oleh **M. Baihaqi Alza**")
st.sidebar.markdown("---")

# Load Data
df = pd.read_csv("dashboard/main_data.csv")

# Sidebar Filter
st.sidebar.header("🔍 Filter Data")
status_filter = st.sidebar.multiselect(
    "Pilih Status Pesanan", 
    options=df["order_status"].unique(), 
    default=df["order_status"].unique()
)

# Terapkan Filter
df_filtered = df[df["order_status"].isin(status_filter)]

#  Header Dashboard**
st.markdown("<h1 style='text-align: center; color: #FF5733;'>📦 E-Commerce Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: gray;'>Analisis Pesanan & Pelanggan</h3>", unsafe_allow_html=True)

#  Ringkasan Data dalam Card Metrics**
col1, col2, col3 = st.columns(3)
col1.metric("📌 Total Pesanan", f"{len(df_filtered):,}")
col2.metric("⏳ Rata-rata Waktu Pengiriman", f"{df_filtered['delivery_time'].mean():.2f} hari")
col3.metric("✅ Pesanan Terkirim Tepat Waktu", f"{df_filtered['delivery_time'][df_filtered['delivery_time'] <= df_filtered['delivery_time'].median()].count()}")

st.markdown("---")

#  Visualisasi Status Pesanan**
st.subheader("📦 Distribusi Status Pesanan")
fig_status = px.pie(df_filtered, names="order_status", title="Distribusi Status Pesanan", color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig_status, use_container_width=True)

#  Visualisasi Waktu Pengiriman**
st.subheader("⏳ Distribusi Waktu Pengiriman")
fig_delivery = px.histogram(df_filtered, x="delivery_time", nbins=30, title="Distribusi Waktu Pengiriman", color_discrete_sequence=["#FF5733"])
st.plotly_chart(fig_delivery, use_container_width=True)

#  Tren Pesanan per Bulan**
st.subheader("📅 Tren Jumlah Pesanan per Bulan")
df_filtered["order_month"] = pd.to_datetime(df_filtered["order_purchase_timestamp"]).dt.strftime('%Y-%m')
orders_per_month = df_filtered.groupby("order_month").size().reset_index(name="count")

fig_trend = px.line(orders_per_month, x="order_month", y="count", markers=True, title="Tren Jumlah Pesanan per Bulan", color_discrete_sequence=["#36A2EB"])
st.plotly_chart(fig_trend, use_container_width=True)

#  Distribusi Pelanggan Berdasarkan Kota**
st.subheader("🌍 Sebaran Pelanggan per Kota")
top_cities = df_filtered["customer_city"].value_counts().head(10)
fig_cities = px.bar(
    x=top_cities.index, 
    y=top_cities.values, 
    labels={"x": "Kota", "y": "Jumlah Pesanan"},
    title="10 Kota dengan Jumlah Pesanan Terbanyak",
    color_discrete_sequence=["#2ECC71"]
)
st.plotly_chart(fig_cities, use_container_width=True)

#  Menampilkan Data dalam Tabel**
with st.expander("📋 Lihat Data Mentah"):
    st.write(df_filtered.head(20))

st.markdown("---")
st.write("---")
st.write("© 2025 M. Baihaqi Alza. All rights reserved.")
# st.markdown("<h4 style='text-align: center;'>🚀 Dibuat oleh <span style='color:#FF5733;'>M. Baihaqi Alza</span></h4>", unsafe_allow_html=True)
# st.markdown("<h5 style='text-align: center;'>📅 Tahun 2025 | 🌎 E-Commerce Data Analysis</h5>", unsafe_allow_html=True)