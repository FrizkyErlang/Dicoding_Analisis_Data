# Dicoding Collection Dashboard ✨

## Setup Environment

```
conda create --name main-ds python=3.9
conda activate main-ds
pip install numpy pandas scipy matplotlib seaborn jupyter streamlit
```

## Run Streamlit App

Pastikan sudah berada di directory folder dashboard

```
streamlit run dashboard.py
```

## Deployment Streamlit App

url dashboard: https://fauzan-dicoding-dasboard.streamlit.app/

![Rentang data](image-4.png)

Pada bagian sidebar, dapat ditentukan rentang data yang akan dipakai

![tampilan timeseries](image.png)

Pada plot timeseries ada opsi harian dan bulanan

![tampilan barplot](image-1.png)

Pada barplot ada opsi untuk data berdasarkan cuaca pada hari itu atau status hari liburnya

![tampilan scatterplot](image-2.png)

Pada scatter plot ada opsi untuk tiap parameter cuacanya (temp, atemp, hum, dan windspeed)

![tampilan piechart](image-3.png)

Pada diagram Pie ditampilkan perbandingan pengguna teregistrasi dan casual
