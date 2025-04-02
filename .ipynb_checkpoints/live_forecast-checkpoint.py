import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.dates as mdates

# === Config ===
file_id = "1Sp9vHcg60ThxQPhahr69QGWJdi3VopbU"
csv_url = f"https://drive.google.com/uc?id={file_id}"

# === Load data ===
@st.cache_data(ttl=300)
def load_data():
    df = pd.read_csv(csv_url, parse_dates=["time"])
    
    # Derived variables
    df["temp_C"] = df["t"] - 273.15
    return df

df = load_data()

# Convert time here to NPT
df["time"] = pd.to_datetime(df["time"]) + pd.Timedelta(hours=5, minutes=45)

# Convert VO2 max to % of max oxygenless ascents... 
# All taken from ISci reconstruction!
ltm_p=334.79086538461536 
ltm_vo2max=16.397887344862063
ltm_pio=56.977246222636495

lt_min_vo2max=15.686907307347052
lt_max_vo2max=16.990437986057785

df["vo2max_score"]=(df["vo2max"]/ltm_vo2max-1.)*100.
df["time"] = pd.to_datetime(df["time"]) + pd.Timedelta(hours=5, minutes=45)

# === Streamlit UI ===
st.title("🏔️ Everest Summit Forecast")

fig, (ax1, ax3) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# === Top subplot: Temperature and Wind ===
ax1.plot(df["time"], df["temp_C"], color="tab:blue", label="Temperature (°C)")
ax1.set_ylabel("Temperature [°C]", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")

ax2 = ax1.twinx()
ax2.plot(df["time"], df["w"], color="tab:red", label="Wind Speed (m/s)")
ax2.set_ylabel("Wind Speed [m/s]", color="tab:red")
ax2.tick_params(axis="y", labelcolor="tab:red")
ax2.axhline(20.0,linestyle='--',color='red')

ax1.set_title("Forecast: Temperature & Wind at Everest Summit")
ax1.grid(True)

# === Bottom subplot: VO2 max as score  ===
ax3.plot(df["time"], df["vo2max_score"], color="tab:green")
ax3.set_ylabel("$\Delta$ VO₂max [% of LTM]", color="tab:green")
ax3.tick_params(axis="y", color="tab:green")
ax3.axhline((lt_min_vo2max/ltm_vo2max-1)*100, color='tab:green',linestyle='--')
ax3.axhline((lt_max_vo2max/ltm_vo2max-1)*100, color='tab:green',linestyle='--')

# ax4 = ax3.twinx()
# ax4.plot(df["time"], df["vo2max"], color="tab:purple", label="VO₂max")
# ax4.set_ylabel("VO₂max (ml/min/kg"), color="tab:purple")
# ax4.tick_params(axis="y", labelcolor="tab:purple")

ax3.set_title("Forecast VO₂max @ Summit (% deviation from mean no-O ascents)")
ax3.grid(True)

# Final layout
for ax in [ax1, ax3]:
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    
ax3.set_ylim(-6.,6.)
ax.set_xlabel("Time [NPT]")
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Optional: Last update time
st.caption(f"⏱️ Forecast run: {df['time'].min().strftime('%Y-%m-%d %H:%M NPT')}")
