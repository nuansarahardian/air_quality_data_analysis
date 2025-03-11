import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Judul Aplikasi
st.title("Dasbor Polusi Udara (Data Nongzhanguan)")

# Memuat dataset
file_path = "C:\\Users\\Nuansa Rahardian\\Downloads\\data_cleaned.csv"
df = pd.read_csv(file_path)

# Konversi kolom datetime ke format datetime
df['datetime'] = pd.to_datetime(df['datetime'])

# Sidebar - Pilih rentang tanggal
st.sidebar.header("Pilih Rentang Tanggal")
start_date = st.sidebar.date_input("Tanggal Mulai", df['datetime'].min().date())
end_date = st.sidebar.date_input("Tanggal Akhir", df['datetime'].max().date())

# Filter dataset berdasarkan rentang tanggal yang dipilih
df_filtered = df[(df['datetime'].dt.date >= start_date) & (df['datetime'].dt.date <= end_date)]

df_filtered["year"] = df_filtered["datetime"].dt.year
# 1️⃣ **Visualisasi Tren Polusi dari Waktu ke Waktu**
st.subheader("\U0001F4C8 Tren Polusi Udara dari Waktu ke Waktu")

pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
# Pilihan polutan
selected_pollutants = st.multiselect("Pilih Jenis Polutan:", pollutants, default=['PM2.5', 'PM10'])

#
# Hitung rata-rata per tahun
df_yearly = df_filtered.groupby("year")[selected_pollutants].mean().reset_index()

# Plot dengan matplotlib
plt.figure(figsize=(10, 5))
for pollutant in selected_pollutants:
    plt.plot(df_yearly["year"], df_yearly[pollutant], marker='o', label=pollutant)

plt.xticks(df_yearly["year"])  # Menampilkan hanya tahun pada sumbu X
plt.xlabel("Tahun")
plt.ylabel("Rata-rata Konsentrasi Polutan")
plt.legend()
plt.grid(True)

# Tampilkan di Streamlit
st.pyplot(plt)
# Tambahkan penjelasan
st.markdown("📌 **Penjelasan:** Grafik ini menunjukkan perubahan konsentrasi polutan yang dipilih dari waktu ke waktu. Tren ini dapat membantu memahami pola polusi udara dalam periode tertentu.")

# 2️⃣ **Analisis Polusi Berdasarkan Musim dan Tahun**
st.subheader("\U0001F342 Rata-rata Polusi Berdasarkan Musim dan Tahun")

selected_polutan = st.selectbox("Pilih Polutan untuk Analisis Musim:", pollutants)

heatmap_data = df_filtered.groupby(["year", "season"])[selected_polutan].mean().unstack()

fig, ax = plt.subplots(figsize=(8, 5))
sns.heatmap(heatmap_data, annot=True, cmap="coolwarm", linewidths=0.5, fmt=".1f")
plt.xlabel("Musim")
plt.ylabel("Tahun")
plt.title(f"Rata-rata {selected_polutan} per Musim dan Tahun")
st.pyplot(fig)

# 3️⃣ **Heatmap Korelasi antara Polutan dan Faktor Cuaca**
st.subheader("\U0001F321 Heatmap Korelasi antara Polutan dan Faktor Cuaca")

columns = ["PM2.5", "PM10", "SO2", "NO2", "CO", "O3", "TEMP", "WSPM"]
df_corr = df_filtered[columns].corr()

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(df_corr, annot=True, cmap="coolwarm", linewidths=0.5, ax=ax)
st.pyplot(fig)



with st.expander("Lihat Konklusi"):
    st.write(
        "Berdasarkan analisis data polusi udara, tren polusi udara dari waktu ke waktu menunjukkan fluktuasi yang signifikan, dengan beberapa tahun mengalami peningkatan konsentrasi polutan tertentu. Pada musim dingin cenderung memiliki tingkat polusi udara tertinggi dibandingkan musim lainnya, kemungkinan akibat peningkatan emisi dari pemanasan seperti penggunaan pemanas ruangan atau pembakaran serta kondisi atmosfer yang memperburuk penyebaran polutan. Selain itu, terdapat korelasi antara faktor meteorologi dan berbagai jenis polutan, di mana suhu, kelembaban, kecepatan angin, dan tekanan udara mempengaruhi konsentrasi polusi. Misalnya, angin kencang dapat membantu mengurangi polutan, sementara suhu rendah cenderung meningkatkan akumulasi polutan di atmosfer."
    )
