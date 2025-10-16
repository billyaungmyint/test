import unittest
import numpy as np
import os
from sklearn.datasets import make_blobs
from kmeans import KMeans

class TestKMeans(unittest.TestCase):

    def setUp(self):
        self.X, self.y = make_blobs(n_samples=300, centers=3, cluster_std=1.5, random_state=42)
        self.plot_filename = 'kmeans_scratch_plot.png'

    def tearDown(self):
        if os.path.exists(self.plot_filename):
            os.remove(self.plot_filename)

    def test_kmeans_fit_predict(self):
        kmeans = KMeans(n_clusters=3, random_state=42)
        kmeans.fit(self.X)
        labels = kmeans.predict(self.X)

        self.assertEqual(labels.shape[0], self.X.shape[0])
        self.assertEqual(len(np.unique(labels)), 3)
        self.assertIsNotNone(kmeans.centroids)
        self.assertEqual(kmeans.centroids.shape, (3, 2))

    def test_main_block(self):
        # This tests the main block in kmeans.py
        # It ensures the plot is created.
        if os.path.exists(self.plot_filename):
            os.remove(self.plot_filename)

        # Run the main block of kmeans.py as a script
        import subprocess
        result = subprocess.run(['python', 'kmeans.py'], capture_output=True, text=True)

        self.assertEqual(result.returncode, 0)
        self.assertTrue(os.path.exists(self.plot_filename))

if __name__ == '__main__':
    unittest.main()