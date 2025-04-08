import streamlit as st
# This must be the very first Streamlit command.
st.set_page_config(
    page_title="Military Decision-Making App",
    page_icon="🛡️",
    layout="centered"
)


st.markdown(
    """
    <style>
    * {
        font-size: 15px !important;
    }
    html, body {
        font-size: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

import random
import os
import logging
import time
import pandas as pd
import joblib
from google.oauth2.service_account import Credentials
import gspread
from io import BytesIO
from docx import Document
from docx.shared import RGBColor
from model_logic import convert_raw_to_scores, predict_scenario
from mappings_fixed import (
    Target_Category_Map, Target_Vulnerability_Map, Terrain_Type_Map,
    Civilian_Presence_Map, Damage_Assessment_Map, Time_Sensitivity_Map,
    Weaponeering_Map, Friendly_Fire_Map, Politically_Sensitive_Map,
    Legal_Advice_Map, Ethical_Concerns_Map, Collateral_Damage_Potential_Map,
    AI_Distinction_Map, AI_Proportionality_Map, AI_Military_Necessity_Map,
    Human_Distinction_Map, Human_Proportionality_Map, Human_Military_Necessity_Map
)
from app_main import (
    calculate_percentages,
    assign_final_decision,
)

# --- Google Sheets Functions ---

def get_google_sheet():
    try:
        creds_dict = dict(st.secrets["gcp_service_account"])
        # Replace any escaped newline characters with actual newlines
        creds_dict["private_key"] = creds_dict["private_key"].replace("\\n", "\n")
        creds = Credentials.from_service_account_info(
            creds_dict,
            scopes=[
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/drive"
            ]
        )
        client = gspread.authorize(creds)
        return client.open("Study_data").sheet1
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None

def save_data_to_google_sheet(data):
    sheet = get_google_sheet()
    if sheet:
        try:
            row = [
                str(data.get('scenario', '')),
                data.get('Participant Decision', ''),      
                data.get('Model Prediction', ''),           
                data.get('Decision Time (seconds)', ''),      
                data.get('Confirmation Feedback', ''),          
                data.get('Additional Feedback', '')           
            ]

            sheet.append_row(row)
            st.success("Feedback saved to Google Sheets!")
        except Exception as e:
            st.error(f"Error saving data to Google Sheets: {e}")


# --- Main App Code ---




st.title("Military Decision-Making App")
st.markdown("### Insert Scenario Parameters")


raw_input = {
    key: st.selectbox(key.replace('_', ' '), list(mapping.keys()))
    for key, mapping in [
        ("Target_Category", Target_Category_Map),
        ("Target_Vulnerability", Target_Vulnerability_Map),
        ("Terrain_Type", Terrain_Type_Map),
        ("Civilian_Presence", Civilian_Presence_Map),
        ("Damage_Assessment", Damage_Assessment_Map),
        ("Time_Sensitivity", Time_Sensitivity_Map),
        ("Weaponeering", Weaponeering_Map),
        ("Friendly_Fire", Friendly_Fire_Map),
        ("Politically_Sensitive", Politically_Sensitive_Map),
        ("Legal_Advice", Legal_Advice_Map),
        ("Ethical_Concerns", Ethical_Concerns_Map),
        ("Collateral_Damage_Potential", Collateral_Damage_Potential_Map),
        ("AI_Distinction (%)", AI_Distinction_Map),
        ("AI_Proportionality (%)", AI_Proportionality_Map),
        ("AI_Military_Necessity", AI_Military_Necessity_Map),
        ("Human_Distinction (%)", Human_Distinction_Map),
        ("Human_Proportionality (%)", Human_Proportionality_Map),
        ("Human_Military_Necessity", Human_Military_Necessity_Map),
    ]
}

if st.button("Predict"):
    numeric_data = convert_raw_to_scores(raw_input)
    numeric_df = pd.DataFrame([numeric_data], columns=[])  
    percentages = calculate_percentages(numeric_data)
    override_decision, override_reason = None, "No override rules applied."
    total_score = numeric_data["Total_Score"]

    for param, score in numeric_data.items():
        if param == "Total_Score":
            continue
        param_name = param.replace('_Score', '')
        pct = percentages.get(param, 0)
        color = "green" if score > 0 else "red" if score < 0 else "black"
        line = f"{param_name}: {raw_input[param_name]} | Score: <span style='color:{color}'>{score} ({pct}%)</span>"
        st.markdown(line, unsafe_allow_html=True)

    st.markdown(f"<div style='color: #CC0000; font-weight: bold;'>Total Score: {total_score}</div>", unsafe_allow_html=True)
    final_decision = override_decision if override_decision else assign_final_decision(total_score)
    st.markdown(f"### Model Decision: {final_decision}")
    st.markdown(f"**{override_reason}**")
    
    st.session_state.final_decision = final_decision
    st.session_state.scenario = raw_input

# Feedback section if a final decision has been made
if "final_decision" in st.session_state:
    st.markdown("### Your Feedback")
    feedback_text = st.text_area("Please share your thoughts about the prediction:", key="feedback_box")
    if st.button("Submit Feedback", key="feedback_submit"):
        data = {
            "scenario": st.session_state.get("scenario", {}),
            "Model Prediction": st.session_state.get("final_decision", ""),
            "Additional Feedback": feedback_text
        }
        save_data_to_google_sheet(data)

