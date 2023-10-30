import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from babel import format_currency
sns.set(style='dark')

days_df = pd.read_csv('https://github.com/RayhanLup1n/submissions/blob/main/days_df.csv')
hours_df = pd.read_csv('https://github.com/RayhanLup1n/submissions/blob/main/hours_df.csv')

def create_monthly_df(df):
     monthly_df = df.resample(rule='M', on='dteday').agg({
          "registered": "sum",
          "casual": "sum",
          "cnt": "sum",
     })
     monthly_df.index = monthly_df.index.strftime('%Y-%m')
     monthly_df = monthly_df.reset_index()

     monthly_df.groupby(by='dteday').agg({
          "registered": "sum",
          "casual": "sum",
          "cnt": "sum",
     })

     return monthly_df

datetime_columns = ['dteday']
days_df.sort_values(by='dteday', inplace=True)
days_df.reset_index(inplace=True)

for column in datetime_columns:
     days_df[column] = pd.to_datetime(days_df[column])

min_date = days_df['dteday'].min()
max_date = days_df['dteday'].max()


monthly_df = create_monthly_df(days_df)

with st.sidebar:
     st.image("https://avatars.githubusercontent.com/u/22091590?s=280&v=4")

     start_date, end_date = st.date_input(
          label='Rentang Waktu', min_value=min_date,
          max_value=max_date,
          value=[min_date,max_date]
     )

st.title('Bike Sharing Dataset Interactive Dashboard :sparkles:')

st.write(
    """
    WELCOME TO MY WORKFRAME GUYS!
    Dashboard ini berisikan dataset dari Bike Sharing.
    Semoga kalian mendapatkan suatu pemahaman baru melalui dashboard ini.
    HAPPY READING GUYS!!!
    """
)

st.subheader('Monthly Bicycle Rental Reports From Various Types of Renters')
plt.figure(figsize=(50,15), facecolor='white')
plt.title("Total Monthly Bicycle Rentals by Renter Type in 2011-2012", loc='center', fontsize=30, fontweight='bold')
plt.plot(monthly_df['dteday'], monthly_df['registered'],
         color = "#00CED1",
         linewidth=5,
         label="Registered Renter",
         marker='o',
         markersize=12)
plt.plot(monthly_df['dteday'], monthly_df['casual'],
         color = "#8FBC8F",
         linewidth=5,
         label="Casual Renter",
         marker='o',
         markersize=12)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.xlabel("Month", loc='center', fontsize=25, fontweight='bold')
plt.ylabel("Total Renter (Millions)", loc='center', fontsize=25, fontweight='bold')
plt.legend(loc='upper left', fontsize=20)
plt.grid(color='grey', linestyle='--', linewidth=0.95)
st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()
with st.expander('See Explanation'):
    st.write(
        """Line Chart di atas berisikan Total penyewaan sepeda tiap bulannya,
        Dari chart tersebut, kita dapat mengetahui bahwa penyewaan tertinggi
        dari penyewa yang terdaftar terjadi pada september 2012 dan pada 
        mei 2012 untuk penyewa yang tidak terdaftar. Jumlah penyewa yang 
        terdaftar juga selalu berada di atas jumlah penyewa yang tidak terdaftar.
        Selain itu, kita juga bisa mengetahui bahwa penyewaan terendah terjadi
        pada bulan januari 2011 untuk penyewa yang terdaftar yang bulan januari
        2011 untuk penyewa yang tidak terdaftar.
        """
    )

st.subheader('Bicycle Rental Report for each Season')
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(30, 10))

colors = ["#12486B", "#419197", "#78D6C6", "#F5FCCD"]

sns.barplot(x=days_df['new_season'], y=days_df['registered'], data=days_df['cnt'], palette=colors, ax=ax[0])
ax[0].set_ylabel('Total Renters (Millions)', fontsize=18, fontweight='bold')
ax[0].set_xlabel('Season', fontsize=18, fontweight='bold')
ax[0].set_title("Total Rental by Registered Renters", loc='center', fontsize=15, fontweight='bold')
ax[0].tick_params(axis='x', labelsize=15)

sns.barplot(x=days_df['new_season'], y=days_df['casual'], data=days_df['cnt'], palette=colors, ax=ax[1])
ax[1].set_ylabel('Total Renters (Millions)', fontsize=18, fontweight='bold')
ax[1].set_xlabel('Season', fontsize=18, fontweight='bold')
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].set_title("Total Rental by Casual Renters", loc='center', fontsize=15, fontweight='bold')
ax[1].tick_params(axis='x', labelsize=15)
plt.suptitle("Total Bicycle Rentals per Season by Renter Type in 2011-2012", fontsize=30, fontweight='bold')
st.pyplot(fig)
with st.expander('See Explanation'):
    st.write(
        """Chart di atas berisikan jumalah penyewa baik penyewa yang terdaftar
        ataupun penyewa yang tidak terdaftar pada setiap musimnya. Dari chart
        tersebut, kita dapat mengetahui bahwasannya musim gugur merupakan musim
        dimana penyewaan sepeda paling banyak terjadi untuk setiap tipe penyewa.
        Dan juga, kita dapat mengetahui bahwa pada musim semi merupakan musim
        yang memiliki jumlah penyewaan paling sedikit untuk setiap tipe penyewanya.
        """
    )

st.subheader('Bicycle Rental Report on each Type of Day (Weekend, Weekday & Holiday)')
fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(40,15))

colors = ["#66CDAA", "#00FA9A"]

sns.barplot(y=days_df['registered'], x=days_df['new_workingday'], data=days_df['cnt'], palette=colors, ax=ax[0])
ax[0].set_ylabel('Total Registered Renters (Millions)', fontsize=15, fontweight='bold')
ax[0].set_xlabel(None)
ax[0].set_title("Type of Day by Registered Renters", loc='center', fontsize=18, fontweight='bold')
ax[0].tick_params(axis='x', labelsize=18)

sns.barplot(y=days_df['casual'], x=days_df['new_workingday'], data=days_df['cnt'], palette=colors, ax=ax[1])
ax[1].set_ylabel('Total Casual Renters (Millions)', fontsize=15, fontweight='bold')
ax[1].set_xlabel(None)
ax[1].set_title("Type of Days by Casual Renters", loc='center', fontsize=18, fontweight='bold')
ax[1].tick_params(axis='x', labelsize=18)

sns.barplot(y=days_df['cnt'], x=days_df['new_workingday'], data=days_df, palette=colors, ax=ax[2])
ax[2].set_ylabel('Total All Renters (Millions)', fontsize=15, fontweight='bold')
ax[2].set_xlabel(None)
ax[2].set_title("Type of Days by All Renters", loc='center', fontsize=18, fontweight='bold')
ax[2].tick_params(axis='x', labelsize=18)

plt.suptitle("Total Bicycle Rentals by Type of Day in 2011-2012 ", fontsize=40, fontweight='bold')
st.pyplot(fig)
with st.expander('See Explanation'):
    st.write(
        """Chart ini berisikan jumlah penyewaan sepeda yang terjadi pada setiap
        jenis harinya (Weekdays, weekend & Holiday). Dari chart tersebut, kita dapat
        mengetahui bahwasanya untuk penyewa yang terdaftar, penyewaan banyak terjadi
        pada hari libur (Weekends & Holiday). Sedangkan untuk penyewa yang tidak terdaftar,
        penyewaan lebih sering terjadi pada hari kerja (Weekdays). Akan tetapi, secara
        garis besar, penyewaan yang terjadi pada hari libur (Weekdends & Holidays) lebih
        banya dibandingkan jumlah penyewaan yang terjadi di hari kerja (Weekdays).
        """
    )

st.subheader('Bicycle Rental Reports on Hourly basis')
table_hours_df = hours_df.groupby(by='hr').agg({
     'registered': 'sum',
     'casual': 'sum',
     'cnt': 'sum',
})
st.table(data=table_hours_df)
with st.expander('See Explanation'):
    st.write(
        """Tabel tersebut berisikan distribusi penyewaan yang terjadi tiap-tiap jamnya.
        Dari tabel tersebut, kita dapat mengetahui bahwasanya jumlah penyewaan sepeda
        ter-rendah terjadi pada pukul 00.00 hingga 06.00. Sedangkan untuk penyewaan 
        tertinggi, terjadi pada pukul 17.00 dan 18.00 pada urutan ke dua.
        """
    )

name = st.text_input(label='Nama Lengkap', value='')
st.write('Nama: ', name)


text1 = st.text_area('Feedback')
text2 = st.text_area('Tuliskan Pemahamanmu Mengenai Dashboard ini!')
text3 = st.text_area('Pesan Untuk Saya Sebagai Pembuat Dashboard!')
st.write('Feedback', text1)
st.write('Tuliskan Pemahamanmu Mengenai Dashboard ini!', text2)
st.write('Pesan Untuk Saya Sebagai Pembuat Dashboard!', text3)


st.caption('Copyright (c) Dicoding 2023')
