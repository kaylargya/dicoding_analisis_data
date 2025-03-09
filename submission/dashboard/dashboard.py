import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

st.header("Bike Sharing Dashboard")

# FUNGSI FUNGSI FUNGSI
def create_rentals_data(df):
    return df[["Date", "Casual_Users", "Registered_Users"]]

def create_monthly_rentals(df):
    monthly_rentals_df = df.groupby(by=["Month", "Year"])["Total_Rentals"].sum().reset_index()
    monthly_rentals_df.rename(columns={"Total_Rentals": "rental_count"}, inplace=True)

    # Urutan bulan agar tampil rapi
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    monthly_rentals_df["Month"] = pd.Categorical(monthly_rentals_df["Month"], categories=month_order, ordered=True)

    # Gabungkan bulan & tahun untuk sumbu X
    monthly_rentals_df["Month_Year"] = monthly_rentals_df["Month"].astype(str) + " " + monthly_rentals_df["Year"].astype(str)
    
    return monthly_rentals_df


def create_time_of_day(df):
    time_of_day_df = df.copy()  # Membuat salinan agar tidak mengubah DataFrame asli

    conditions = [
        (time_of_day_df["Hour"].isin([3, 4, 5, 6, 7, 8, 9, 10])),
        (time_of_day_df["Hour"].isin([11, 12, 13, 14, 15])),
        (time_of_day_df["Hour"].isin([16, 17, 18])),
        (time_of_day_df["Hour"].isin([19, 20, 21, 22, 23, 0, 1, 2]))
    ]
    values = ["Morning", "Afternoon", "Late Afternoon", "Night"]

    time_of_day_df["Times_of_the_Day"] = np.select(conditions, values, default="Unknown")
    time_of_day_df["Times_of_the_Day"] = time_of_day_df["Times_of_the_Day"].astype("category")

    return time_of_day_df


def create_plot_time_of_day(df):
    daily_rentals = df.groupby("Times_of_the_Day").agg({"Total_Rentals": "mean"}).reset_index()

    daily_rentals["Times_of_the_Day"] = pd.Categorical(
        daily_rentals["Times_of_the_Day"], 
        categories=["Morning", "Afternoon", "Late Afternoon", "Night"],
        ordered=True
    )
    
    daily_rentals = daily_rentals.sort_values("Times_of_the_Day")
    
    colors = ["#CBDCEB", "#CBDCEB", "#133E87", "#CBDCEB"]

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=daily_rentals["Times_of_the_Day"], y=daily_rentals["Total_Rentals"], palette=colors, ax=ax)

    ax.set_xlabel("Waktu dalam Sehari", fontsize=12)
    ax.set_ylabel("Rata-rata Jumlah Penyewaan Sepeda", fontsize=12)

    ax.tick_params(axis="x", labelrotation=45, labelsize=10)
    ax.tick_params(axis="y", labelsize=10)

    return fig

def create_scatter_temp_rentals(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.regplot(x=df["Temperature"], y=df["Total_Rentals"], 
                scatter_kws={"color": "#133E87"}, 
                line_kws={"color": "#F14A00"}, 
                ax=ax)

    ax.set_title("Hubungan antara Suhu dan Jumlah Penyewaan Sepeda", fontsize=14, fontweight="bold")
    ax.set_xlabel("Suhu (°C)", fontsize=12)
    ax.set_ylabel("Jumlah Penyewaan Sepeda", fontsize=12)

    return fig

def create_day_type_df(input_df):
    def classify_day(Day_of_the_Week):
        return "Weekend" if Day_of_the_Week in ["Sat", "Sun"] else "Weekday"

    # Salin DataFrame untuk menghindari modifikasi langsung
    day_type_df = input_df.copy()
    
    # Terapkan fungsi untuk menentukan tipe hari
    day_type_df["day_type"] = day_type_df["Day_of_the_Week"].apply(classify_day)
    day_type_df["day_type"] = day_type_df["day_type"].astype("category")

    return day_type_df


def plot_rentals_by_day_type(df):
    rentals_by_day_type = df.groupby(["Hour", "day_type"])["Total_Rentals"].mean().unstack()

    fig, ax = plt.subplots(figsize=(10, 5))

    # Plot data Weekday
    ax.plot(rentals_by_day_type.index, rentals_by_day_type["Weekday"], label="Hari Kerja", marker="o", linestyle="-", color="#FFAB5B")

    # Plot data Weekend
    ax.plot(rentals_by_day_type.index, rentals_by_day_type["Weekend"], label="Akhir Pekan", marker="o", linestyle="--", color="#133E87")

    # Menambahkan label dan judul
    ax.set_xlabel("Waktu (Jam)", fontsize=12)
    ax.set_ylabel("Rata-rata Jumlah Penyewaan Sepeda", fontsize=12)
    ax.set_xticks(rentals_by_day_type.index)
    ax.tick_params(axis="x", labelsize=10)
    ax.tick_params(axis="y", labelsize=10)

    # Menambahkan legenda
    ax.legend()
    ax.grid(True)

    return fig

# Load Data
daily_data = pd.read_csv("daily_clean.csv")
hourly_data = pd.read_csv("hourly_clean.csv")

datetime_columns = ["Date"]
daily_data.sort_values(by="Date", inplace=True)
daily_data.reset_index(inplace=True) 

hourly_data.sort_values(by="Date", inplace=True)
hourly_data.reset_index(inplace=True)

for column in datetime_columns:
    daily_data[column] = pd.to_datetime(daily_data[column])
    hourly_data[column] = pd.to_datetime(hourly_data[column])

min_date_days = daily_data["Date"].min()
max_date_days = daily_data["Date"].max()

min_date_hour = hourly_data["Date"].min()
max_date_hour = hourly_data["Date"].max()

with st.sidebar:
    st.image("logo.png")
    start_date, end_date = st.date_input(
        label="Rentang Waktu",
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days]
    )

# Filter data berdasarkan rentang tanggal
main_df_days = daily_data[(daily_data["Date"] >= str(start_date)) & 
                          (daily_data["Date"] <= str(end_date))]
main_df_hour = hourly_data[(hourly_data["Date"] >= str(start_date)) & 
                           (hourly_data["Date"] <= str(end_date))]

### DATA DATA DATA
# Mengambil data rentals
rentals_data = create_rentals_data(main_df_days)
monthly_rentals_df = create_monthly_rentals(main_df_days)
main_df_hour = create_time_of_day(main_df_hour)

# GRAFIK 1
st.subheader("Tren Penyewaan Sepeda Berdasarkan Tipe Pengguna")

# Membuat plot tren Casual vs Registered Users
fig, ax = plt.subplots(figsize=(16, 8))

# Plot data Casual Users
ax.plot(
    rentals_data["Date"],
    rentals_data["Casual_Users"],
    marker="o",
    linewidth=2,
    color="#FFAB5B",
    label="Casual Users"
)

# Plot data Registered Users
ax.plot(
    rentals_data["Date"],
    rentals_data["Registered_Users"],
    marker="o",
    linewidth=2,
    color="#133E87",
    label="Registered Users"
)

# Menambahkan label dan judul
ax.set_xlabel("Tanggal", fontsize=12)
ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
ax.tick_params(axis="x", labelrotation=45, labelsize=10)
ax.tick_params(axis="y", labelsize=10)

# Menambahkan legenda
ax.legend()

# Menampilkan grid
ax.grid(True)

# Menampilkan plot dalam Streamlit
st.pyplot(fig)

# GRAFIK 2
st.subheader("Distribusi Penyewaan Sepeda Tiap Bulan")

# Cari nilai maksimum secara global untuk menentukan warna biru tua
max_month_year = monthly_rentals_df.loc[monthly_rentals_df["rental_count"].idxmax(), "Month_Year"]

# Urutkan berdasarkan bulan agar tampil berurutan
monthly_rentals_df = monthly_rentals_df.sort_values(by=["Year", "Month"])

# Warna untuk bar chart (biru tua untuk nilai tertinggi)
colors = ["#CBDCEB" if month_year != max_month_year else "#133E87" for month_year in monthly_rentals_df["Month_Year"]]

# Membuat bar chart tunggal
fig, ax = plt.subplots(figsize=(18, 6))

sns.barplot(x=monthly_rentals_df["Month_Year"], y=monthly_rentals_df["rental_count"], palette=colors, ax=ax)
ax.set_ylabel("Jumlah Penyewaan", fontsize=12)
ax.set_xlabel("Bulan", fontsize=12)
ax.tick_params(axis="x", labelrotation=45, labelsize=10)

# Menampilkan plot dalam Streamlit
st.pyplot(fig)

# GRAFIK 3 DAN 4
col1, col2 = st.columns([1, 1]) 

with col1:
    st.subheader("Distribusi Penyewaaan Sepeda")
    fig = create_plot_time_of_day(main_df_hour)
    st.pyplot(fig)

with col2:
    st.subheader("Hubungan antara Suhu dan Penyewaaan Sepeda")
    fig = create_scatter_temp_rentals(main_df_days)
    st.pyplot(fig)

# GRAFIK 5
st.subheader("Perbandingan Pola Penyewaan Sepeda: Hari Kerja vs Akhir Pekan")

# Pastikan data hourly sudah dikategorikan berdasarkan "Weekday" dan "Weekend"
main_df_hour = create_day_type_df(main_df_hour)

fig = plot_rentals_by_day_type(main_df_hour)
st.pyplot(fig)