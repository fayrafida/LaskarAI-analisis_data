import streamlit as st
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import numpy as np
import seaborn as sns


def st_normal():
    _, col, _ = st.columns([1, 2, 1])
    return col


def pm_groupby_station_df(df):
    pm_df = df.groupby(['station']).agg({
        'PM2.5' : 'mean',
        'PM10' : 'mean'
    })
    return pm_df
def pm_time_span_df(df):
    # Penentuan rentang waktu dari masing-masing jam
    df['time_span'] = df.hour.apply(lambda x: "Morning" if x >= 6 and x<=11
                                            else ("Afternoon" if x >= 12 and x<=16
                                                    else ("Evening" if x >=17 and x<=23 else "Night")))
    return df

def pm_groupby_station_timespan_df(df):
    # Penentuan rentang waktu dari masing-masing jam
    data['time_span'] = data.hour.apply(lambda x: "Morning" if x >= 6 and x<=11
                                            else ("Afternoon" if x >= 12 and x<=16
                                                    else ("Evening" if x >=17 and x<=23 else "Night")))
    # Penggabungan berdasarkan rentang waktu
    timespan_particle_df = data.groupby(by=["station", "time_span"]).agg({
            "hour" : "first",
            "PM2.5":"mean"
        })
    timespan_particle_df['index'] = timespan_particle_df.hour.apply(lambda x: 0 if x >= 6 and x<=11
                                            else (1 if x >= 12 and x<=16
                                                    else (2 if x >=17 and x<=23 else 3)))

    timespan_particle_df= timespan_particle_df.sort_values(by = ['index'], ascending =True)
    # timespan_particle_df = timespan_particle_df.reset_index()
    timespan_particle_df = timespan_particle_df.drop(columns={"hour"})
    timespan_particle_df = timespan_particle_df.reset_index()
    # timespan_particle_df
    station_df = timespan_particle_df.groupby('station')
    return station_df

def pm_groupby_station_year_df(df):
    yearly_df = df.groupby(by=["station", "year"]).agg({
        "PM2.5":"mean"
    })
    return yearly_df

def pm_groupby_station_month_df(df):
    monthly_df = df.groupby(by=["station", "month"]).agg({
        "PM2.5":"mean"
    })
    return monthly_df

def pm_groupby_station_day_df(df):
    daily_df = df.groupby(by=["station", "day"]).agg({
        "PM2.5":"mean"
    })
    return daily_df

def pm_groupby_station_hour_df(df):
    hourly_df = df.groupby(by=["station", "hour"]).agg({
        "PM2.5":"mean"
    })
    return hourly_df

def wd_groupby_station_month_df(df):
    wd_month_df = df.groupby(by=["station", 'month']).agg({
        "wd":"mean"
    })
    return wd_month_df

def wspm_groupby_station_month_df(df):
    wdsm_month_df = df.groupby(by=["station", 'month']).agg({
        "WSPM":"mean"
    })
    return wdsm_month_df

def rain_groupby_station_month_df(df):
    rain_month_df = df.groupby(by=["station", 'month']).agg({
        "RAIN":"mean"
    })
    return rain_month_df

# Konfigurasi halaman
st.set_page_config(
    page_title="Dicoding Air Quality Dashboard",
    layout="wide",
)

# Header
st.markdown("""
    <h1 style='text-align: center; color: #4CAF50;'>Dicoding Air Quality Dashboard</h1>
""", unsafe_allow_html=True)

# Membaca parent directory dari file dashboard
BASE_DIR = Path(__file__).resolve().parent.parent 
# Membaca semua file data
path = BASE_DIR/'data'
files = [f for f in listdir(path) if isfile(join(path, f))]
ls = []
for filename in files:
  df = pd.read_csv(join(path, filename), index_col=None, header=0)
  ls.append(df)

data = pd.concat(ls, axis=0, ignore_index=True)
data = data.drop('No', axis=1)

# Mengubah nilai Arah Angin menjadi numeric
data.loc[data['wd'] == 'N', 'wd'] = 0
data.loc[data['wd'] == 'E', 'wd'] = 90
data.loc[data['wd'] == 'S', 'wd'] = 180
data.loc[data['wd'] == 'W', 'wd'] = 270
data.loc[data['wd'] == 'WNW', 'wd'] = 292.5
data.loc[data['wd'] == 'NNW', 'wd'] = 337.5
data.loc[data['wd'] == 'NW', 'wd'] = 315
data.loc[data['wd'] == 'NNE', 'wd'] = 22.5
data.loc[data['wd'] == 'NE', 'wd'] = 45
data.loc[data['wd'] == 'ESE', 'wd'] = 112.5
data.loc[data['wd'] == 'SE', 'wd'] = 135
data.loc[data['wd'] == 'ENE', 'wd'] = 67.5
data.loc[data['wd'] == 'SSE', 'wd'] = 157.5
data.loc[data['wd'] == 'WSW', 'wd'] = 246.5
data.loc[data['wd'] == 'SW', 'wd'] = 225
data.loc[data['wd'] == 'SSW', 'wd'] = 205.5
data.loc[data['wd'] == 'WSW', 'wd'] = 247.5
data['wd'] = pd.to_numeric(data['wd'])

# Mengubah kolom year, month, day, hour menjadi date
data['date'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']], format='%Y-%m-%d %H')

min_date = data["date"].min()
max_date = data["date"].max()

# Sidebar - Filter
st.sidebar.header("Filter Data")
# Mengambil start_date & end_date dari date_input
start_date, end_date = st.sidebar.date_input(
    label='Rentang Waktu',min_value=min_date,
    max_value=max_date,
    value=[min_date, max_date]
)

station = st.sidebar.selectbox("Wilayah", np.concatenate([['All'], data['station'].unique()]))

# Filter by date
main_df = data[(data['date'] >= str(start_date)) & 
               (data["date"] <= str(end_date))]

# Filter by station
if station != 'All':
    main_df = main_df[(data['station'] == station)]

# Menampilkan nilai PM2.5
st.subheader("PM2.5", divider=True)
col1, col2 = st.columns(2)
with col1:
    lowest_pm25 = main_df.loc[main_df["PM2.5"].idxmin()]
    st.metric(label=f"Terendah: {lowest_pm25['station']}", value=lowest_pm25["PM2.5"])

with col2:
    highest_pm25 = main_df.loc[main_df["PM2.5"].idxmax()]
    st.metric(label=f"Tertinggi: {highest_pm25['station']}", value=highest_pm25["PM2.5"])

# Menampilkan nilai PM10
st.subheader("PM10", divider=True)
col3, col4 = st.columns(2)
with col3:
    lowest_pm10 = main_df.loc[main_df["PM10"].idxmin()]
    st.metric(label=f"Terendah: {lowest_pm10['station']}", value=lowest_pm10["PM10"])

with col4:
    highest_pm10 = main_df.loc[main_df["PM10"].idxmax()]
    st.metric(label=f"Tertinggi: {highest_pm10['station']}", value=highest_pm10["PM10"])

st.subheader("Diagram PM2.5", divider=True)
col5, col6 = st.columns(2)
with col5:
    # Diagram PM2.5 Semua Wilayah
    pm25_all_station = pm_groupby_station_df(main_df)

    X_axis = np.arange(len(pm25_all_station.index))
    plt.bar(X_axis - 0.2, pm25_all_station['PM2.5'], 0.4, label = 'PM2.5')
    plt.bar(X_axis + 0.2, pm25_all_station['PM10'], 0.4, label = 'PM10')

    plt.xticks(X_axis, pm25_all_station.index)
    plt.xlabel("Station")
    plt.ylabel("Value")
    plt.xticks(rotation=45)
    plt.title("PM2.5 and PM10 Values ​​for All Stations")
    plt.legend()
    st.pyplot(plt.gcf())
with col6:
    pm_timespan = pm_time_span_df(main_df)
    pm_timespan = pm_groupby_station_timespan_df(pm_timespan)
    
    fig0, ax0 = plt.subplots(figsize=(8, 6))
    for key, group in pm_timespan:
        ax0.plot(group['time_span'], group['PM2.5'], label=key)

    # Set axis labels and title
    ax0.set_xlabel('Time')
    ax0.set_ylabel('PM2.5')
    ax0.set_title('PM2.5 Values by Time Span')

    # Defining and displaying all time axis ticks
    ticks = ['Morning', 'Afternoon', 'Evening', 'Night']
    plt.xticks(ticks)

    # Add a legend
    ax0.legend()

    # Display the grid
    ax0.grid(True)

    # Show the plot
    st.pyplot(fig0)

# Diagram PM2.5 berdasarkan waktu
time_range = st_normal().selectbox("Pilih Jangka Waktu", ["Tahunan", "Bulanan", "Harian", 'Per Jam'])
if time_range == 'Tahunan':
    pm25_time = pm_groupby_station_year_df(main_df)
    pm25_time = pm25_time.reset_index()

    station_df = pm25_time.groupby('station')
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    for key, group in station_df:
        ax1.plot(group['year'], group['PM2.5'], label=key)
    # Set axis labels and title
    ax1.set_xlabel('Time')
    ax1.set_ylabel('PM2.5')
    ax1.set_title('Annual PM2.5 Values')

    # Defining and displaying all time axis ticks
    ticks = list(pm25_time['year'].unique())
elif time_range == 'Bulanan':
    pm25_time = pm_groupby_station_month_df(main_df)
    pm25_time = pm25_time.reset_index()

    station_df = pm25_time.groupby('station')
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    for key, group in station_df:
        ax1.plot(group['month'], group['PM2.5'], label=key)

    # Set axis labels and title
    ax1.set_xlabel('Time')
    ax1.set_ylabel('PM2.5')
    ax1.set_title('Monthly PM2.5 Values')

    # Defining and displaying all time axis ticks
    ticks = list(pm25_time['month'])
elif time_range == 'Harian':
    pm25_time = pm_groupby_station_day_df(main_df)
    pm25_time = pm25_time.reset_index()

    station_df = pm25_time.groupby('station')
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    for key, group in station_df:
        ax1.plot(group['day'], group['PM2.5'], label=key)

    # Set axis labels and title
    ax1.set_xlabel('Time')
    ax1.set_ylabel('PM2.5')
    ax1.set_title('Daily PM2.5 Values')

    # Defining and displaying all time axis ticks
    ticks = list(pm25_time['day'])
elif time_range == 'Per Jam':
    pm25_time = pm_groupby_station_hour_df(main_df)
    pm25_time = pm25_time.reset_index()

    station_df = pm25_time.groupby('station')
    fig1, ax1 = plt.subplots(figsize=(8, 6))
    for key, group in station_df:
        ax1.plot(group['hour'], group['PM2.5'], label=key)

    # Set axis labels and title
    ax1.set_xlabel('Time')
    ax1.set_ylabel('PM2.5')
    ax1.set_title('Hourly PM2.5 Values')

    # Defining and displaying all time axis ticks
    ticks = list(pm25_time['hour'])

plt.xticks(ticks)

# Add a legend
ax1.legend()

# Display the grid
ax1.grid(True)
st_normal().pyplot(fig1)


st.subheader("Diagram Arah Angin & Kecepatan Angin", divider=True)
col7, col8 = st.columns(2)
with col7:
    # Diagram Arah Angin
    wd_df = wd_groupby_station_month_df(main_df)
    wd_df = wd_df.reset_index()

    station_df = wd_df.groupby('station')

    fig2, ax2 = plt.subplots(figsize=(8, 6))
    for key, group in station_df:
        ax2.plot(group['month'], group['wd'], label=key)

    # Set axis labels and title
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Wind Direction')
    ax2.set_title('Monthly Wind Direction')

    # Defining and displaying all time axis ticks
    ticks = list(wd_df['month'])
    plt.xticks(ticks)

    # Add a legend
    ax2.legend()

    # Display the grid
    ax2.grid(True)
    st.pyplot(fig2)
with col8:
    # Diagram Kecepatan Angin
    wspm_df = wspm_groupby_station_month_df(main_df)
    wspm_df = wspm_df.reset_index()

    station_df = wspm_df.groupby('station')

    fig3, ax3 = plt.subplots(figsize=(8, 6))
    for key, group in station_df:
        ax3.plot(group['month'], group['WSPM'], label=key)

    # Set axis labels and title
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Wind Speed')
    ax3.set_title('Monthly Wind Speed Values')

    # Defining and displaying all time axis ticks
    ticks = list(wspm_df['month'])
    plt.xticks(ticks)

    # Add a legend
    ax3.legend()

    # Display the grid
    ax3.grid(True)

    st.pyplot(fig3)


# Diagram Curah Hujan
st.subheader("Diagram Curah Hujan", divider=True)
rain_df = rain_groupby_station_month_df(main_df)
rain_df = rain_df.reset_index()

station_df = rain_df.groupby('station')

fig4, ax4 = plt.subplots(figsize=(8, 6))
for key, group in station_df:
  ax4.plot(group['month'], group['RAIN'], label=key)

# Set axis labels and title
ax4.set_xlabel('Time')
ax4.set_ylabel('Rainfall')
ax4.set_title('Monthly Rainfall Values')

# Defining and displaying all time axis ticks
ticks = list(rain_df['month'])
plt.xticks(ticks)

# Add a legend
ax4.legend()

# Display the grid
ax4.grid(True)

# Show the plot
st_normal().pyplot(fig4)

# Footer
st.markdown("""
    <hr>
    <center>Developed by Fairuz Rafida</center>
    <center>To Complete LaskarAI by Dicoding</center>
""", unsafe_allow_html=True)
