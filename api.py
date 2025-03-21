from fastapi import FastAPI
from pydantic import BaseModel, Field
from model_logic import convert_raw_to_scores, predict_scenario
import traceback

app = FastAPI()

class ScenarioInput(BaseModel):
    Target_Category: str
    Target_Vulnerability: str
    Terrain_Type: str
    Civilian_Presence: str
    Damage_Assessment: str
    Time_Sensitivity: str
    Weaponeering: str
    Friendly_Fire: str
    Politically_Sensitive: str
    Legal_Advice: str
    Ethical_Concerns: str
    Collateral_Damage_Potential: str
    AI_Distinction: str = Field(alias='AI_Distinction (%)')
    AI_Proportionality: str = Field(alias='AI_Proportionality (%)')
    AI_Military_Necessity: str
    Human_Distinction: str = Field(alias='Human_Distinction (%)')
    Human_Proportionality: str = Field(alias='Human_Proportionality (%)')
    Human_Military_Necessity: str

@app.post("/predict")
def predict(input: ScenarioInput):
    try:
        numeric_data = convert_raw_to_scores(input.dict(by_alias=True))
        result = predict_scenario(numeric_data)
        return {"result": result}
    except Exception as e:
        traceback.print_exc()
        return {"error": str(e)}
