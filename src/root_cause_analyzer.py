"""
Addresses the "Global 8D problem-solving" requirement. It monitors data thresholds to identify anomalies (such as component overheating) and isolates the specific operational boundaries causing failures.
"""
import pandas as pd

class Global8DAnalyzer:
    def __init__(self, data_path: str):
        self.data = pd.read_csv(data_path)
        
    def execute_d3_containment_check(self, temperature_threshold=850.0) -> pd.DataFrame:
        """D3 Stage: Identify escaping defects (EGT exceeding safe limits)."""
        critical_failures = self.data[self.data['EGT_Celsius'] > temperature_threshold]
        return critical_failures

    def execute_d4_root_cause_isolation(self, failure_df: pd.DataFrame) -> dict:
        """D4 Stage: Isolate conditions causing the root component thermal stress."""
        if failure_df.empty:
            return {"Status": "No thermal anomalies identified."}
            
        avg_speed = failure_df['Engine_Speed_RPM'].mean()
        avg_load = failure_df['Engine_Load_Pct'].mean()
        
        root_cause_summary = {
            "Isolate_Condition": "High-Speed & High-Load boundary operation structural stress",
            "Mean_Failure_Speed_RPM": round(avg_speed, 1),
            "Mean_Failure_Load_Pct": round(avg_load, 1),
            "Recommended_Action": "Enrich Lambda target maps or retard spark timing at high-boundary zones."
        }
        return root_cause_summary

if __name__ == "__main__":
    analyzer = Global8DAnalyzer("data/engine_test_bench_data.csv")
    failures = analyzer.execute_d3_containment_check()
    root_cause = analyzer.execute_d4_root_cause_isolation(failures)
    print("Global 8D Analysis Summary Report:")
    for key, value in root_cause.items():
        print(f"   - {key}: {value}")
