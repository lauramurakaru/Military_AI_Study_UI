
import streamlit as st
import pandas as pd
import joblib
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
    get_score_display,
    assign_final_decision,
    trained_feature_columns,
    rf_model_loaded,
)

def apply_override_rules(categories, numeric_data):
    try:
        total_score = numeric_data.get('Total_Score', sum(numeric_data.values()))
        civilian_presence = categories['Civilian_Presence']
        civilian_presence_num = int(civilian_presence.split('-')[0]) if '-' in civilian_presence else int(civilian_presence)

        rules = [
            (categories['Target_Category'] in ["Chapel", "Medical Installation", "Medical Vehicle"], "Do Not Engage", f"Protected Target_Category '{categories['Target_Category']}'"),
            ((categories['Terrain_Type'] in ["Urban Center", "Residential Area"]) and (categories['Target_Category'] not in ["High-Value Target", "Battalion HQ", "Battlegroup HQ", "Brigade HQ", "Division HQ"]), "Do Not Engage", f"Non-priority target in {categories['Terrain_Type']}"),
            (categories['Ethical_Concerns'] == 'Immoral' and total_score >= 30, "Do Not Engage", "Ethical concerns override high score"),
            (civilian_presence_num >= 100, "Do Not Engage", f"High civilian presence: {categories['Civilian_Presence']}"),
            (categories['Collateral_Damage_Potential'] == 'Very_High' and civilian_presence_num >= 50, "Do Not Engage", "High collateral damage risk with significant civilian presence"),
            (categories['Friendly_Fire'] == "Very_High" and categories['Collateral_Damage_Potential'] == 'Very_High', "Do Not Engage", "Multiple high-risk factors present"),
            (civilian_presence_num > 30 and categories['Weaponeering'] in ["Incendiary Weapon", "Thermobaric Munition", "White Phosphorus Bomb"], "Ask Authorization", "Special weapons with civilian presence > 30"),
            (categories['Legal_Advice'] in ['It depends', 'Questionable'] or (categories['Ethical_Concerns'] == 'Immoral' and civilian_presence_num > 50), "Ask Authorization", "Legal/ethical concerns require authorization"),
            (categories['Politically_Sensitive'] == "High" and categories['Terrain_Type'] == "Critical Infrastructure Area", "Ask Authorization", "Sensitive infrastructure engagement"),
            (categories['Weaponeering'] == "Anti-Personnel Mine" and categories['Target_Category'] in ["Fighter Aircraft", "Frigate", "Ship Maintenance Facility", "Naval Base"], "Do Not Know", "Inappropriate weapon for target type"),
            (categories['Weaponeering'] == "Torpedo" and categories['Target_Category'] not in ["Ship Maintenance Facility", "Naval Base", "Frigate"], "Do Not Know", "Torpedo inappropriate for non-naval target")
        ]

        for condition, decision, reason in rules:
            if condition:
                return decision, reason
        return None, "No override rules applied."

    except Exception as e:
        return None, f"Error applying override rules: {str(e)}"

st.title("Military Decision-Making App")

st.markdown("### Insert Scenario Parameters")

raw_input = {key: st.selectbox(key.replace('_', ' '), list(mapping.keys())) for key, mapping in [
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
]}

if st.button("Predict"):
    numeric_data = convert_raw_to_scores(raw_input)
    numeric_df = pd.DataFrame([numeric_data], columns=trained_feature_columns)

    override_decision, override_reason = apply_override_rules(raw_input, numeric_data)

    percentages = calculate_percentages(numeric_data)
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
