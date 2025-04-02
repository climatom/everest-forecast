import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.dates as mdates

# === Config ===
gfs_file_id = "1Sp9vHcg60ThxQPhahr69QGWJdi3VopbU"
ecmwf_file_id = "1Pl-kR2ngv9vQ2z7PymUdQU3jiMD0njXx"

def gdrive_csv_url(file_id):
    return f"https://drive.google.com/uc?id={file_id}"

# === Load data ===
@st.cache_data(ttl=300)
def load_csv(url):
    df = pd.read_csv(url, parse_dates=["time"])
    df["temp_C"] = df["t"] - 273.15
    df["time"] = pd.to_datetime(df["time"]) + pd.Timedelta(hours=5, minutes=45)
    return df

df_gfs = load_csv(gdrive_csv_url(gfs_file_id))
df_ecmwf = load_csv(gdrive_csv_url(ecmwf_file_id))

# === Constants for VO₂max normalization ===
ltm_vo2max = 16.397887344862063
lt_min_vo2max = 15.686907307347052
lt_max_vo2max = 16.990437986057785

# === Derived VO2max scores ===
df_gfs["vo2max_score"] = (df_gfs["vo2max"] / ltm_vo2max - 1.) * 100.
df_ecmwf["vo2max_score"] = (df_ecmwf["vo2max"] / ltm_vo2max - 1.) * 100.

# === Streamlit UI ===
st.title("🏔️ Everest Summit Forecast (GFS vs ECMWF)")

fig, axs = plt.subplots(2, 2, figsize=(14, 8), sharex='row')

# === GFS (Left Column) ===
ax1, ax3 = axs[0, 0], axs[1, 0]

# Top: Temp + Wind
ax1.plot(df_gfs["time"], df_gfs["temp_C"], color="tab:blue", label="Temp (°C)")
ax1.set_ylabel("Temp [°C]", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")
ax2 = ax1.twinx()
ax2.plot(df_gfs["time"], df_gfs["w"], color="tab:red", label="Wind")
ax2.set_ylabel("Wind [m/s]", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")
ax2.axhline(20.0, linestyle='--', color='red')
ax1.set_title("GFS: Temperature & Wind")
ax1.grid(True)

# Bottom: VO₂max score
ax3.plot(df_gfs["time"], df_gfs["vo2max_score"], color="tab:green")
ax3.set_ylabel("ΔVO₂max [%]", color="tab:green")
ax3.axhline((lt_min_vo2max/ltm_vo2max - 1)*100, color='tab:green', linestyle='--')
ax3.axhline((lt_max_vo2max/ltm_vo2max - 1)*100, color='tab:green', linestyle='--')
ax3.set_title("GFS: VO₂max Deviation (LTM, no-O₂ summits)")
ax3.grid(True)

# === ECMWF (Right Column) ===
ax1r, ax3r = axs[0, 1], axs[1, 1]

# Top: Temp + Wind
ax1r.plot(df_ecmwf["time"], df_ecmwf["temp_C"], color="tab:blue", label="Temp (°C)")
ax1r.set_ylabel("Temp [°C]", color="tab:blue")
ax1r.tick_params(axis="y", labelcolor="tab:blue")
ax2r = ax1r.twinx()
ax2r.plot(df_ecmwf["time"], df_ecmwf["w"], color="tab:red", label="Wind")
ax2r.set_ylabel("Wind [m/s]", color="tab:red")
ax2r.tick_params(axis="y", labelcolor="tab:red")
ax2r.axhline(20.0, linestyle='--', color='red')
ax1r.set_title("ECMWF: Temperature & Wind")
ax1r.grid(True)

# Bottom: VO₂max score
ax3r.plot(df_ecmwf["time"], df_ecmwf["vo2max_score"], color="tab:green")
ax3r.set_ylabel("ΔVO₂max [%]", color="tab:green")
ax3r.axhline((lt_min_vo2max/ltm_vo2max - 1)*100, color='tab:green', linestyle='--')
ax3r.axhline((lt_max_vo2max/ltm_vo2max - 1)*100, color='tab:green', linestyle='--')
ax3r.set_title("ECMWF: VO₂max Deviation (LTM, no-O₂ summits)")
ax3r.grid(True)

# === Format X axis ===
for ax in [ax1, ax1r, ax3, ax3r]:
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.tick_params(axis="x", rotation=45)

ax3.set_xlabel("Time [NPT]")
ax3r.set_xlabel("Time [NPT]")
plt.tight_layout()

# Show plot
st.pyplot(fig)

# Caption: forecast timing
st.caption(f"🕒 GFS forecast from: {df_gfs['time'].min().strftime('%Y-%m-%d %H:%M NPT')}")
st.caption(f"🕒 ECMWF forecast from: {df_ecmwf['time'].min().strftime('%Y-%m-%d %H:%M NPT')}")
