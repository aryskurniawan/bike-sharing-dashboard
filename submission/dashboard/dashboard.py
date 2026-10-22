import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Set konfigurasi halaman Streamlit
st.set_page_config(page_title="Bike Sharing Dashboard (2011-2012)", layout="wide")

# Fungsi untuk memuat data
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

day_df = load_data()

# Sidebar filter tanggal
st.sidebar.header("Filter Data")
min_date = day_df['dteday'].min()
max_date = day_df['dteday'].max()

start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',
    min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

main_df = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & 
                 (day_df['dteday'] <= pd.to_datetime(end_date))]

# Header Dashboard
st.title("🚲 Bike Sharing Data Dashboard")
st.markdown("Dashboard interaktif untuk menganalisis penyewaan sepeda berdasarkan kondisi lingkungan dan tipe pengguna **periode 2011–2012**.")

# Row 1: Key Metrics
col1, col2, col3 = st.columns(3)
with col1:
    total_rentals = main_df['cnt'].sum()
    st.metric("Total Penyewaan", value=f"{total_rentals:,}")
with col2:
    total_registered = main_df['registered'].sum()
    st.metric("Pengguna Registered", value=f"{total_registered:,}")
with col3:
    total_casual = main_df['casual'].sum()
    st.metric("Pengguna Casual", value=f"{total_casual:,}")

st.divider()

# Visualisasi 1: Pengaruh Musim dan Cuaca (2011-2012)
st.subheader("Pengaruh Musim dan Cuaca Terhadap Penyewaan Sepeda (2011–2012)")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))
colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

# Barplot Musim
season_df = main_df.groupby("season")["cnt"].mean().reset_index().sort_values(by="cnt", ascending=False)
sns.barplot(x="cnt", y="season", data=season_df, hue="season", palette=colors, legend=False, ax=ax[0])
ax[0].set_title("Rata-rata Penyewaan Berdasarkan Musim (2011–2012)")
ax[0].set_xlabel("Rata-rata Penyewaan")
ax[0].set_ylabel(None)

# Barplot Cuaca
weather_df = main_df.groupby("weathersit")["cnt"].mean().reset_index().sort_values(by="cnt", ascending=False)
sns.barplot(x="cnt", y="weathersit", data=weather_df, hue="weathersit", palette=colors[:len(weather_df)], legend=False, ax=ax[1])
ax[1].set_title("Rata-rata Penyewaan Berdasarkan Cuaca (2011–2012)")
ax[1].set_xlabel("Rata-rata Penyewaan")
ax[1].set_ylabel(None)

st.pyplot(fig)

st.divider()

# Visualisasi 2: Perilaku Pengguna (Hari Kerja vs Hari Libur 2011-2012)
st.subheader("Perilaku Pengguna Casual vs Registered (Hari Kerja vs Hari Libur 2011–2012)")
workingday_df = main_df.groupby("workingday")[["casual", "registered"]].mean().reset_index()
workingday_melted = pd.melt(workingday_df, id_vars=['workingday'], value_vars=['casual', 'registered'], var_name='user_type', value_name='avg_count')
workingday_melted['workingday'] = workingday_melted['workingday'].map({0: 'Hari Libur/Akhir Pekan', 1: 'Hari Kerja'})

fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(x="workingday", y="avg_count", hue="user_type", data=workingday_melted, palette=["#D3D3D3", "#72BCD4"], ax=ax2)
ax2.set_title("Perbandingan Pola Penggunaan Sepeda (2011–2012)")
ax2.set_ylabel("Rata-rata Pengguna")
ax2.set_xlabel(None)
ax2.legend(title="Tipe Pengguna")

st.pyplot(fig2)