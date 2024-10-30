import streamlit as st
import pandas as pd
import joblib
import random
import re

# -------------------------------
# Load the Model and Feature Columns
# -------------------------------

# Load the trained model
model_path = 'MDMP_model.joblib'
rf_model_loaded = joblib.load(model_path)

# Load the trained feature columns
features_path = 'MDMP_feature_columns.joblib'
trained_feature_columns = joblib.load(features_path)

# Load the dataset
csv_path = 'dataset_with_all_category_scores.csv'
df = pd.read_csv(csv_path)

# -------------------------------
# Define Functions
# -------------------------------

# Columns to shuffle in tandem (related features)
columns_to_shuffle = [
    ['Target_Category', 'Target_Category_Score'],
    ['Target_Vulnerability', 'Target_Vulnerability_Score'],
    ['Terrain_Type', 'Terrain_Type_Score'],
    ['Civilian_Presence', 'Civilian_Presence_Score'],
    ['Damage_Assessment', 'Damage_Assessment_Score'],
    ['Time_Sensitivity', 'Time_Sensitivity_Score'],
    ['Weaponeering', 'Weaponeering_Score'],
    ['Friendly_Fire', 'Friendly_Fire_Score'],
    ['Politically_Sensitive', 'Politically_Sensitive_Score'],
    ['Legal_Advice', 'Legal_Advice_Score'],
    ['Ethical_Concerns', 'Ethical_Concerns_Score'],
    ['Collateral_Damage_Potential', 'Collateral_Damage_Potential_Score'],
    ['AI_Distinction (%)', 'AI_Distinction (%)_Score'],
    ['AI_Proportionality (%)', 'AI_Proportionality (%)_Score'],
    ['AI_Military_Necessity', 'AI_Military_Necessity_Score'],
    ['Human_Distinction (%)', 'Human_Distinction (%)_Score'],
    ['Human_Proportionality (%)', 'Human_Proportionality (%)_Score'],
    ['Human_Military_Necessity', 'Human_Military_Necessity_Score']
]

# Label mapping for model predictions
label_mapping = {
    0: 'Do Not Engage',
    1: 'Ask Authorization',
    2: 'Do Not Know',
    3: 'Engage'
}

def shuffle_dataset(df):
    df_shuffled = df.copy()
    for related_columns in columns_to_shuffle:
        shuffled_subset = df[related_columns].sample(frac=1).reset_index(drop=True)
        df_shuffled[related_columns] = shuffled_subset
    return df_shuffled

def get_random_scenario(df):
    random_index = random.randint(0, len(df) - 1)
    scenario = df.iloc[random_index]
    return scenario

def display_scenario(scenario):
    st.header("Scenario")
    columns_to_display = [
        'Target_Category', 'Target_Vulnerability', 'Terrain_Type', 'Civilian_Presence',
        'Damage_Assessment', 'Time_Sensitivity', 'Weaponeering', 'Friendly_Fire',
        'Politically_Sensitive', 'Legal_Advice', 'Ethical_Concerns', 'Collateral_Damage_Potential',
        'AI_Distinction (%)', 'AI_Proportionality (%)', 'AI_Military_Necessity',
        'Human_Distinction (%)', 'Human_Proportionality (%)', 'Human_Military_Necessity'
    ]
    for column in columns_to_display:
        value = scenario[column] if pd.notna(scenario[column]) else "Unknown"
        st.write(f"**{column}:** {value}")
    decision_options = ["Engage", "Do Not Engage", "Ask Authorization", "Do Not Know"]
    decision = st.selectbox("What is your decision?", decision_options)
    return decision

def calculate_total_score(row, score_columns):
    total_score = 0
    for col in score_columns:
        if col in row and pd.notna(row[col]):
            try:
                value = float(row[col])
                total_score += value
            except ValueError:
                pass
    return total_score

def extract_average_from_range(value):
    if isinstance(value, str):
        match = re.match(r"(\d+)-(\d+)", value)
        if match:
            start, end = map(int, match.groups())
            return (start + end) / 2
        else:
            try:
                return float(value)
            except ValueError:
                return None
    elif isinstance(value, (int, float)):
        return value
    return None

def apply_override_rules(row):
    cp_value = extract_average_from_range(row['Civilian_Presence'])
    if cp_value is None:
        st.warning(f"Unable to convert Civilian_Presence '{row['Civilian_Presence']}' to a number.")
        return None, None

    # Rule 1: Do Not Engage Overrides
    if row['Target_Category'] in ["Chapel", "Medical Installation", "Medical Vehicle"]:
        return "Do Not Engage", f"Target_Category={row['Target_Category']}"
    if row['Terrain_Type'] in ["Urban Center", "Residential Area"] and row['Target_Category'] not in ["High-Value Target", "Battalion HQ", "Battlegroup HQ", "Brigade HQ", "Division HQ"]:
        return "Do Not Engage", f"Terrain_Type={row['Terrain_Type']}, Target_Category={row['Target_Category']}"
    if row['Weaponeering'] == "Torpedo" and row['Target_Category'] not in ["Ship Maintenance Facility", "Naval Base", "Frigate"]:
        return "Do Not Engage", f"Weaponeering={row['Weaponeering']}, Target_Category={row['Target_Category']}"
    if row['Ethical_Concerns'] == 'Immoral' and row['Total_Score'] >= 30:
        return "Do Not Engage", f"Ethical_Concerns={row['Ethical_Concerns']}, Total_Score={row['Total_Score']}"
    if cp_value == 100 and row['Friendly_Fire'] == "High":
        return "Do Not Engage", f"Civilian_Presence={cp_value}, Friendly_Fire={row['Friendly_Fire']}"
    if row['Collateral_Damage_Potential'] == 'Very_High' and cp_value >= 50:
        return "Do Not Engage", f"Collateral_Damage_Potential={row['Collateral_Damage_Potential']}"
    if row['Friendly_Fire'] == "Very_High" and row['Collateral_Damage_Potential'] == 'Very_High':
        return "Do Not Engage", f"Friendly_Fire={row['Friendly_Fire']}, Collateral_Damage_Potential={row['Collateral_Damage_Potential']}"

    # Rule 2: Ask Authorization Overrides
    if cp_value > 30 and row['Weaponeering'] in ["Incendiary Weapon", "Thermobaric Munition", "White Phosphorus Bomb"]:
        return "Ask Authorization", f"Civilian_Presence={cp_value}, Weaponeering={row['Weaponeering']}"
    if row['Legal_Advice'] in ['It depends', 'Questionable'] or (row['Ethical_Concerns'] == 'Immoral' and cp_value > 50):
        return "Ask Authorization", f"Legal_Advice={row['Legal_Advice']}, Ethical_Concerns={row['Ethical_Concerns']}, Civilian_Presence={cp_value}"
    if row['Politically_Sensitive'] == "High" and row['Terrain_Type'] == "Critical Infrastructure Area":
        return "Ask Authorization", f"Politically_Sensitive={row['Politically_Sensitive']}, Terrain_Type={row['Terrain_Type']}"

    # Rule 3: Do Not Know Overrides
    if row['Weaponeering'] == "Anti-Personnel Mine" and row['Target_Category'] in ["Fighter Aircraft", "Frigate", "Ship Maintenance Facility", "Naval Base"]:
        return "Do Not Know", f"Weaponeering={row['Weaponeering']}, Target_Category={row['Target_Category']}"

    try:
        hd_value = float(row['Human_Distinction (%)'])
        ad_value = float(row['AI_Distinction (%)'])
        hp_value = float(row['Human_Proportionality (%)'])
        ap_value = float(row['AI_Proportionality (%)'])
        if (hd_value < 60 and ad_value > 90) or (hd_value > 70 and ad_value < 10):
            return "Do Not Know", f"Human_Distinction (%)={hd_value}, AI_Distinction (%)={ad_value}"
        if (hp_value < 60 and ap_value > 90) or (hp_value > 70 and ap_value < 10):
            return "Do Not Know", f"Human_Proportionality (%)={hp_value}, AI_Proportionality (%)={ap_value}"
    except ValueError:
        st.warning(f"Unable to convert distinction or proportionality values.")

    return None, None

def explain_model_decision(scenario, model):
    feature_importances = model.feature_importances_
    reasoning = []
    for i, feature in enumerate(trained_feature_columns):
        if feature in scenario:
            importance = feature_importances[i]
            if importance > 0:
                reasoning.append(f"{feature}: {scenario[feature]} (Importance: {importance * 100:.2f}%)")
    return reasoning

def execute_decision_process(random_scenario, model, user_decision):
    # Step 1: Calculate Total Score if not already available
    score_columns = [col for col in trained_feature_columns if col.endswith('_Score')]
    if 'Total_Score' not in random_scenario.index:
        random_scenario = random_scenario.copy()
        random_scenario['Total_Score'] = calculate_total_score(random_scenario, score_columns)

    # Step 2: Convert the scenario to a DataFrame for model input consistency
    scenario_features_df = random_scenario.to_frame().T

    # Reindex to ensure the DataFrame matches the trained features
    scenario_features_df = scenario_features_df.reindex(columns=trained_feature_columns, fill_value=0)

    # Step 3: Apply override rules first
    override_decision, override_reason = apply_override_rules(random_scenario)

    # Step 4: Predict with model if no override rule applies
    if override_decision:
        model_prediction_label = override_decision
    else:
        model_prediction_num = model.predict(scenario_features_df)[0]
        model_prediction_label = label_mapping.get(model_prediction_num, "Unknown")

    # Display results
    st.subheader("Comparison of Your Decision and Model's Prediction")
    st.write(f"**Your Decision:** {user_decision}")
    st.write(f"**Model Prediction:** {model_prediction_label}")

    if override_decision:
        st.write(f"**Override Rule Applied:** {override_reason}")
    else:
        reasoning_explanation = explain_model_decision(random_scenario, model)
        if reasoning_explanation:
            st.write("**Reasoning Behind Model's Prediction:**")
            for reason in reasoning_explanation:
                st.write(f"- {reason}")
        else:
            st.write("No significant features contributed to the model's decision.")

# -------------------------------
# Main Function
# -------------------------------

def main():
    st.title("Decision-Making App")
    st.write("Please review the following scenario and make your decision.")

    # Shuffle the dataset
    df_shuffled = shuffle_dataset(df)

    # Get a random scenario
    scenario = get_random_scenario(df_shuffled)

    # Display the scenario and get user's decision
    user_decision = display_scenario(scenario)

    # When the user clicks the button, execute the decision process
    if st.button("Submit Decision"):
        execute_decision_process(scenario, rf_model_loaded, user_decision)

if __name__ == "__main__":
    main()
