# Ensures software robustness using standard testing suites.
import unittest
import os
from src.data_processor import generate_simulated_test_bench_data
from src.optimizer import CalibrationOptimizer

class TestCalibrationPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_data_path = "data/test_engine_data.csv"
        df = generate_simulated_test_bench_data(num_samples=50)
        os.makedirs("data", exist_ok=True)
        df.to_csv(cls.test_data_path, index=False)

    def test_data_generation_columns(self):
        self.assertTrue(os.path.exists(self.test_data_path))

    def test_optimizer_execution(self):
        opt = CalibrationOptimizer(self.test_data_path)
        opt.fit_emissions_model()
        spark = opt.optimize_spark_timing(50.0, 500.0)
        self.assertGreaterEqual(spark, 5.0)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.test_data_path):
            os.remove(cls.test_data_path)

if __name__ == "__main__":
    unittest.main()
