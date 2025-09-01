from pathlib import Path
import pandas as pd

DATA_DIR = Path(__file__).parent / "datasets"

def load_datasets():
    factors = pd.read_csv(DATA_DIR / "factors.csv")
    limits = pd.read_csv(DATA_DIR / "limits.csv").set_index("Pollutant")["Limit"].to_dict()
    return factors, limits


def calculate_emissions(fuel_type: str, hours: float, power: float) -> dict:
    factors_df, _ = load_datasets()
    row = factors_df[factors_df["FuelType"].str.lower() == fuel_type.lower()]
    if row.empty:
        raise ValueError(f"Fuel type '{fuel_type}' not found in dataset.")

    results = {}
    for pollutant in ["CO", "NOx", "PM", "HC"]:
        factor = float(row[pollutant].values[0])  # g/kWh (measured value)
        results[pollutant] = round(factor, 3)  # keep measured as is
    return results

def check_compliance(emissions: dict) -> dict:
    _, limits = load_datasets()
    return {p: emissions[p] <= limits[p] for p in emissions}
