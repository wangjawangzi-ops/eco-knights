import streamlit as st
import pandas as pd
import os

# --- Title ---
st.set_page_config(page_title="Eco-Audit Campus Calculator", layout="wide")
st.title("🌱 Eco-Audit Campus Calculator")

# --- Input Form ---
st.header("Enter Your Daily Usage")

with st.form(key="usage_form"):
    department = st.selectbox("Department", ["Mechanical", "Computer Science", "Arts"])
    plastic_bottles = st.number_input("Number of plastic bottles used", min_value=0)
    ac_hours = st.number_input("Hours AC was on", min_value=0.0)
    pages_printed = st.number_input("Pages printed", min_value=0)
    submit_button = st.form_submit_button(label="Submit")

# --- CO2 Calculation ---
def calculate_co2(plastic, ac, pages):
    return plastic*0.05 + ac*1.2 + pages*0.01

if submit_button:
    co2 = calculate_co2(plastic_bottles, ac_hours, pages_printed)
    
    # Save data to CSV
    new_data = pd.DataFrame({
        "Department": [department],
        "Plastic Bottles": [plastic_bottles],
        "AC Hours": [ac_hours],
        "Pages Printed": [pages_printed],
        "CO2 (kg)": [co2]
    })

    file = "data.csv"
    if os.path.exists(file):
        df = pd.read_csv(file)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data

    df.to_csv(file, index=False)
    st.success(f"Data submitted! Your CO₂ footprint: {co2:.2f} kg")

# --- Leaderboard ---
if os.path.exists("data.csv"):
    df = pd.read_csv("data.csv")
    leaderboard = df.groupby("Department")["CO2 (kg)"].sum().sort_values()
    
    st.header("🏆 Department Leaderboard (Lower CO₂ is Better)")
    st.bar_chart(leaderboard)

    st.table(leaderboard.reset_index().rename(columns={"CO2 (kg)": "Total CO₂ (kg)"}))
