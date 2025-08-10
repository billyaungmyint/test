import unittest
import os
from linear_regression import perform_linear_regression

class TestLinearRegression(unittest.TestCase):

    def test_regression_output(self):
        # Run the function
        slope, intercept, prediction, r2 = perform_linear_regression()

        # Check if the plot file was created
        self.assertTrue(os.path.exists('regression_plot.png'))

        # Check if the returned values are within a reasonable range
        self.assertAlmostEqual(slope, 0.9524, places=4)
        self.assertAlmostEqual(intercept, 1.2143, places=4)
        self.assertAlmostEqual(prediction, 9.7857, places=4)
        self.assertAlmostEqual(r2, 0.9070, places=4)

    @classmethod
    def tearDownClass(cls):
        # Clean up the created file
        if os.path.exists('regression_plot.png'):
            os.remove('regression_plot.png')

if __name__ == '__main__':
    unittest.main()
