"""
This module generates simulated engine test bench data (mimicking INCA/Matlab data acquisition logs) containing engine speed, load, spark timing, emissions (NOx, CO), and exhaust gas temperature (EGT).
"""
import pandas as pd
import numpy as np

def generate_simulated_test_bench_data(num_samples=500) -> pd.DataFrame:
    """Simulates raw engine calibration data from a test bench log."""
    np.random.seed(42)
    
    engine_speed = np.random.uniform(800, 6000, num_samples)  # RPM
    engine_load = np.random.uniform(10, 100, num_samples)     # % Load
    spark_timing = np.random.uniform(5, 40, num_samples)      # BTDC
    
    # Mathematical relationships mirroring real engine physics
    base_nox = (engine_load * 12) + (spark_timing * 8) + np.random.normal(0, 15, num_samples)
    nox_emissions = np.clip(base_nox, 20, None)
    
    base_co = (100 - engine_load) * 2.5 + (40 - spark_timing) * 1.2 + np.random.normal(0, 5, num_samples)
    co_emissions = np.clip(base_co, 5, None)
    
    egt = 300 + (engine_load * 4.5) + (engine_speed * 0.05) - (spark_timing * 2) + np.random.normal(0, 10, num_samples)
    
    # Introduce a simulated hardware anomaly/failure mode for 8D analysis (e.g., cooling system restriction)
    for i in range(len(egt)):
        if engine_speed[i] > 4500 and engine_load[i] > 80:
            egt[i] += 120  # Thermal anomaly baseline
            
    df = pd.DataFrame({
        'Engine_Speed_RPM': engine_speed,
        'Engine_Load_Pct': engine_load,
        'Spark_Timing_Deg': spark_timing,
        'NOx_Emissions_ppm': nox_emissions,
        'CO_Emissions_ppm': co_emissions,
        'EGT_Celsius': egt
    })
    return df

if __name__ == "__main__":
    df = generate_simulated_test_bench_data()
    df.to_csv("data/engine_test_bench_data.csv", index=False)
    print("Simulated engine test bench dataset successfully created in 'data/'.")
