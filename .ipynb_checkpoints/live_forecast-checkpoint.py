import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

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

# === Streamlit UI ===
st.title("🏔️ Everest Summit Forecast")

fig, (ax1, ax3) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# === Top subplot: Temperature and Wind ===
ax1.plot(df["time"], df["temp_C"], color="tab:red", label="Temperature (°C)")
ax1.set_ylabel("Temperature (°C)", color="tab:red")
ax1.tick_params(axis="y", labelcolor="tab:red")

ax2 = ax1.twinx()
ax2.plot(df["time"], df["w"], color="tab:blue", label="Wind Speed (m/s)")
ax2.set_ylabel("Wind Speed (m/s)", color="tab:blue")
ax2.tick_params(axis="y", labelcolor="tab:blue")

ax1.set_title("Forecast: Temperature & Wind at Everest Summit")
ax1.grid(True)

# === Bottom subplot: PIO₂ and VO2max ===
ax3.plot(df["time"], df["pio"], color="tab:green", label="PIO₂ (hPa)")
ax3.set_ylabel("PIO₂ (hPa)", color="tab:green")
ax3.tick_params(axis="y", labelcolor="tab:green")

ax4 = ax3.twinx()
ax4.plot(df["time"], df["vo2max"], color="tab:purple", label="VO₂max")
ax4.set_ylabel("VO₂max (", color="tab:purple")
ax4.tick_params(axis="y", labelcolor="tab:purple")

ax3.set_title("Oxygen Availability & VO₂max")
ax3.grid(True)

# Final layout
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(fig)

# Optional: Last update time
st.caption(f"⏱️ Last updated: {df['time'].min().strftime('%Y-%m-%d %H:%M UTC')}")
