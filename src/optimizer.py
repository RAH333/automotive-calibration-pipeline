"""
This module models the tradeoff between performance parameters and emissions boundaries using multi-variable optimization strategies to calculate optimized calibration targets.
"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize

class CalibrationOptimizer:
    def __init__(self, data_path: str):
        self.data = pd.read_csv(data_path)
        
    def fit_emissions_model(self):
        """Fits a polynomial response surface for NOx based on load and spark timing."""
        X = self.data[['Engine_Load_Pct', 'Spark_Timing_Deg']].values
        y = self.data['NOx_Emissions_ppm'].values
        # Simple linear-quadratic regression coefficients representation
        self.coeffs = np.linalg.lstsq(np.hstack([X, X**2, np.ones((X.shape[0], 1))]), y, rcond=None)[0]

    def optimize_spark_timing(self, target_load: float, nox_limit: float) -> float:
        """Finds optimum spark timing to limit emissions while keeping timing advanced."""
        def objective(spark):
            # Maximize advance (minimize negative spark value)
            return -spark[0]

        def constraint_nox(spark):
            # NOx must be below safety limit
            X_input = np.array([target_load, spark[0], target_load**2, spark[0]**2, 1])
            predicted_nox = np.dot(X_input, self.coeffs)
            return nox_limit - predicted_nox

        cons = {'type': 'ineq', 'fun': constraint_nox}
        bounds = [(5, 45)]
        
        res = minimize(objective, x0=[20.0], bounds=bounds, constraints=cons)
        return float(res.x[0]) if res.success else 20.0

if __name__ == "__main__":
    optimizer = CalibrationOptimizer("data/engine_test_bench_data.csv")
    optimizer.fit_emissions_model()
    opt_spark = optimizer.optimize_spark_timing(target_load=75.0, nox_limit=700.0)
    print(f"Optimized Spark Advance at 75% load with <700ppm NOx constraint: {opt_spark:.2f}° BTDC")
  
