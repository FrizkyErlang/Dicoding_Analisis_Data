import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# Membuat fungsi untuk menyiapkan datafram

def create_monthly_df(df: pd.DataFrame) -> pd.DataFrame:
    """    
    Menkonversi dataframe harian untuk total pengguna (casual, registered,
    dan cnt) ke total pengguna dalam satu bulan.
    """

    monthly_df = df.resample(rule="M", on="dteday").agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum"
    })
    monthly_df['label'] = monthly_df.index.strftime('%b-%Y')
    monthly_df.reset_index(inplace=True)

    return monthly_df


def categorize(workday: int, holiday: int) -> str:
    """    
    Bikin kategorisasi buat create_status_day_df
    """

    if workday == 1:
        return "hari_kerja"
    elif holiday == 1:
        return "hari_libur"
    else:
        return "akhir_pekan"


def create_status_day_df(df: pd.DataFrame) -> pd.DataFrame:
    """    
    Melakukan grouping rata2 total pengguna untuk hari libur, akhir pekan,
    dan hari kerja sesuai pada kolom status_day
    """

    daily_df_status_day = df[["workingday", "holiday",
                              "casual", "registered", "cnt"]].copy(deep=True)
    daily_df_status_day["status_day"] = daily_df_status_day.apply(
        lambda x: categorize(x["workingday"], x["holiday"]), axis=1)

    status_day_df = daily_df_status_day.groupby("status_day").agg({
        "casual": "mean",
        "registered": "mean",
        "cnt": "mean",
    })
    status_day_df.sort_values(
        by="cnt",
        ascending=False,
        inplace=True,
    )
    status_day_df.reset_index(inplace=True)

    return status_day_df


def create_status_weather_df(df: pd.DataFrame) -> pd.DataFrame:
    """    
    Melakukan grouping rata2 total pengguna untuk setiap kondisi cuaca
    sesuai pada kolom weathersit
    """

    status_weather_df = df.groupby(by="weathersit").agg({
        "casual": "mean",
        "registered": "mean",
        "cnt": "mean",
    })
    status_weather_df.sort_values(
        by="cnt",
        ascending=False,
        inplace=True,
    )
    status_weather_df.reset_index(inplace=True)

    return status_weather_df


def create_status_user(df: pd.DataFrame) -> pd.DataFrame:
    """    
    Melakukan grouping total untuk setiap tipe pengguna (casual dan
    registered)
    """

    status_user_df = df.agg({
        "casual": "sum",
        "registered": "sum",
    })
    status_user_df = pd.DataFrame(status_user_df)
    status_user_df.reset_index(inplace=True, names="user")
    status_user_df.columns.values[1] = "total"

    return status_user_df


# Membaca data dari csv dan memastikan kolom yang bertipe datetime memiliki
# tipe data yang benar

all_df = pd.read_csv(filepath_or_buffer="./main_data.csv")
all_df["dteday"] = pd.to_datetime(all_df["dteday"])


# Mensetting page config
st.set_page_config(
    page_title="Final Project Fauzan",
    page_icon=":bike:",
    layout="wide",

)


# Membuat filter untuk rentang data

min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()

with st.sidebar:
    # Menulis nama
    st.title('Oleh M Fauzan Rizky AE')
    st.text('(Id Dicoding: frizky12)')

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label="Rentang Waktu Data Bike Sharing",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) &
                 (all_df["dteday"] <= str(end_date))]


# Menyiapkan setiap dataframe yang dibutuhkan

monthly_df = create_monthly_df(main_df)
status_day_df = create_status_day_df(main_df)
status_weather_df = create_status_weather_df(main_df)
status_user_df = create_status_user(main_df)


# Membuat komponen dashboard yang lain

# Judul dashboard
st.header("Tugas Akhir Dicoding Proyek Analisis Data", divider="blue")

# Plot Timeseries dari total harian dan total bulanan peminjaman sepeda
st.subheader("Timeseries dari bike sharing")

bulan_hari = st.radio(
    label="Jenis timeseries:",
    options=("Per-hari", "Per-bulan"),
    horizontal=True,
)
if bulan_hari == "Per-hari":
    plot_df = main_df
else:
    plot_df = monthly_df

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(plot_df["dteday"], plot_df["cnt"],
        linewidth=1.5, color="b", label="Total pengguna")
ax.plot(plot_df["dteday"], plot_df["casual"],
        linewidth=1.5, color="r", label="Pengguna casual")
ax.plot(plot_df["dteday"], plot_df["registered"],
        linewidth=1.5, color="g", label="Pengguna terregistrasi")
ax.legend(loc="upper left")
ax.set_title(
    label=f"Jumlah Peminjaman Sepeda {bulan_hari} (2011 - 2012)", fontsize=20)
ax.set_ylabel(ylabel="Jumlah Peminjaman")
ax.set_xlabel(xlabel="Waktu")
ax.set_xlim(np.min(plot_df["dteday"]), np.max(plot_df["dteday"]))
st.pyplot(fig)

# Plot Bar untuk rata2 total pengguna per-hari
st.subheader("Perbandingan rata-rata total harian peminjaman sepeda")

dasar_perbandingan = st.radio(
    label="Perbandingan berdasarkan:",
    options=("Hari libur", "Kondisi cuaca"),
    horizontal=True,
)
if dasar_perbandingan == "Hari libur":
    bar_df = status_day_df
    xnya = "status_day"
else:
    bar_df = status_weather_df
    xnya = "weathersit"

fig, ax = plt.subplots(figsize=(35, 15))
bar_df.plot(
    kind="bar",
    x=xnya,
    figsize=(15, 10),
    ax=ax,
)
ax.set_ylabel(ylabel="Rata-rata peminjaman per-hari")
ax.set_xlabel(xlabel=None)
ax.tick_params(labelrotation=0)
ax.legend(
    labels=["Pengguna casual", "Pengguna Terregistrasi", "Total Pengguna"],
    loc="upper right",
)
st.pyplot(fig)

# Plot Scatter untuk kondisi parameter cuaca vs total pengguna
st.subheader("Hubungan kondisi cuaca terhadap jumlah peminjaman sepeda perhari")

col1, col2 = st.columns(2)

with col1:
    parameternya = st.radio(
        label="Parameter cuaca:",
        options=("Suhu udara", "Suhu yang dirasa",
                 "Kelembapan udara", "Kecepatan angin")
    )
    if parameternya == "Suhu udara":
        kolom = "temp"
        ylabel = "Suhu Udara (°C)"
    elif parameternya == "Suhu yang dirasa":
        kolom = "atemp"
        ylabel = "Suhu Udara (°C)"
    elif parameternya == "Suhu yang dirasa":
        kolom = "hum"
        ylabel = "Kelembapan Udara"
    else:
        kolom = "windspeed"
        ylabel = "Kecepatan Angin"

with col2:
    st.metric(
        "Korelasi",
        value=str(round(main_df["cnt"].corr(main_df[kolom]), 3)),
    )

fig, ax = plt.subplots(figsize=(20, 15))
sns.regplot(
    x="cnt",
    y=kolom,
    data=main_df,
    ax=ax,
)
ax.set_xlabel("Total Peminjaman Perhari")
ax.set_ylabel(ylabel=ylabel)
st.pyplot(fig)

# Plot Pie untuk status pengguna
st.subheader("Persentase status pengguna")

fig, ax = plt.subplots(figsize=(15, 15))
ax.pie(
    x=status_user_df["total"],
    labels=status_user_df["user"],
    autopct='%1.1f%%',
    pctdistance=.4,
    labeldistance=.7,
)
st.pyplot(fig)
