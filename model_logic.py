import joblib
import pandas as pd
from mappings_fixed import (
    Target_Category_Map, Target_Vulnerability_Map, Terrain_Type_Map, 
    Civilian_Presence_Map, Damage_Assessment_Map, Time_Sensitivity_Map, 
    Weaponeering_Map, Friendly_Fire_Map, Politically_Sensitive_Map, 
    Legal_Advice_Map, Ethical_Concerns_Map, Collateral_Damage_Potential_Map, 
    AI_Distinction_Map, AI_Proportionality_Map, AI_Military_Necessity_Map,
    Human_Distinction_Map, Human_Proportionality_Map, Human_Military_Necessity_Map
)

# File paths must match exactly your actual files:
MODEL_PATH = "MDMP_model.joblib"
FEATURES_PATH = "MDMP_feature_columns.joblib"

# Load the trained model and feature columns
model = joblib.load(MODEL_PATH)
trained_feature_columns = joblib.load(FEATURES_PATH)

def convert_raw_to_scores(raw_input):
    scores = {
        "Target_Category_Score": Target_Category_Map[raw_input["Target_Category"]],
        "Target_Vulnerability_Score": Target_Vulnerability_Map[raw_input["Target_Vulnerability"]],
        "Terrain_Type_Score": Terrain_Type_Map[raw_input["Terrain_Type"]],
        "Civilian_Presence_Score": Civilian_Presence_Map[raw_input["Civilian_Presence"]],
        "Damage_Assessment_Score": Damage_Assessment_Map[raw_input["Damage_Assessment"]],
        "Time_Sensitivity_Score": Time_Sensitivity_Map[raw_input["Time_Sensitivity"]],
        "Weaponeering_Score": Weaponeering_Map[raw_input["Weaponeering"]],
        "Friendly_Fire_Score": Friendly_Fire_Map[raw_input["Friendly_Fire"]],
        "Politically_Sensitive_Score": Politically_Sensitive_Map[raw_input["Politically_Sensitive"]],
        "Legal_Advice_Score": Legal_Advice_Map[raw_input["Legal_Advice"]],
        "Ethical_Concerns_Score": Ethical_Concerns_Map[raw_input["Ethical_Concerns"]],
        "Collateral_Damage_Potential_Score": Collateral_Damage_Potential_Map[raw_input["Collateral_Damage_Potential"]],
        "AI_Distinction (%)_Score": AI_Distinction_Map[raw_input["AI_Distinction (%)"]],
        "AI_Proportionality (%)_Score": AI_Proportionality_Map[raw_input["AI_Proportionality (%)"]],
        "AI_Military_Necessity_Score": AI_Military_Necessity_Map[raw_input["AI_Military_Necessity"]],
        "Human_Distinction (%)_Score": Human_Distinction_Map[raw_input["Human_Distinction (%)"]],
        "Human_Proportionality (%)_Score": Human_Proportionality_Map[raw_input["Human_Proportionality (%)"]],
        "Human_Military_Necessity_Score": Human_Military_Necessity_Map[raw_input["Human_Military_Necessity"]],
    }
    scores["Total_Score"] = sum(scores.values())
    return scores

def predict_scenario(numeric_data):
    input_df = pd.DataFrame([numeric_data], columns=trained_feature_columns)
    prediction_code = model.predict(input_df)[0]
    labels = {0: "Do Not Engage", 1: "Ask Authorization", 2: "Do Not Know", 3: "Engage"}
    return {
        "prediction_code": int(prediction_code),
        "prediction_label": labels[prediction_code]
    }
