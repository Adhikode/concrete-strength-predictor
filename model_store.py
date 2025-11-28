import joblib
import numpy as np
import pandas as pd

# Load saved objects
final_scaler = joblib.load("final_scaler.pkl")
final_ensemble_models = joblib.load("final_ensemble_models.pkl")
feature_columns = joblib.load("feature_columns.pkl")

# Mapping from UI column names → model column names
UI_TO_MODEL = {
    "Cement": "Cement",
    "BlastFurnaceSlag": "Blast_Furnace_Slag",
    "FlyAsh": "Fly_Ash",
    "Water": "Water",
    "Superplasticizer": "Superplasticizer",
    "CoarseAggregate": "Coarse_Aggregate",
    "FineAggregate": "Fine_Aggregate",
    "Age": "Age",
    "Slag": "Slag",
    "SilicaFume": "Silica_Fume",
    "LimestonePowder": "Limestone_Powder",
    "quartzPowder": "Quartz_Powder",
    "NanoSilica": "Nano_Silica",
    "Fiber": "Fiber",
    "TypeCode": "TypeCode",
    "Slag_Exists": "Slag_Exists",
    "Silica_Fume_Exists": "Silica_Fume_Exists",
    "Limestone_Powder_Exists": "Limestone_Powder_Exists",
    "Quartz_Powder_Exists": "Quartz_Powder_Exists",
    "Nano_Silica_Exists": "Nano_Silica_Exists",
    "Fiber_Exists": "Fiber_Exists",
    "Blast_Furnace_Slag_Exists": "Blast_Furnace_Slag_Exists"
}

def ensemble_predict(models, X_new):
    preds = [m.predict(X_new) for m in models]
    return np.mean(preds, axis=0)

def predict_strength(df_input):

    # Convert UI names → model names
    df_input = df_input.rename(columns=UI_TO_MODEL)

    # Ensure correct ordering
    df_input = df_input[feature_columns]

    # Scale
    scaled = final_scaler.transform(df_input)

    # Predict
    return ensemble_predict(final_ensemble_models, scaled)
