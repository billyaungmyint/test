import unittest
import os
from clustering_comparison import perform_clustering_comparison

class TestClusteringComparison(unittest.TestCase):

    def test_clustering_comparison_output(self):
        # Run the function
        results = perform_clustering_comparison()
        kmeans_sil, kmeans_ari, kmeans_n, dbscan_sil, dbscan_ari, dbscan_n, dbscan_noise = results

        # Check if the plot file was created
        self.assertTrue(os.path.exists('clustering_comparison_plot.png'))

        # Check if the returned values are within reasonable ranges
        # Silhouette scores should be between -1 and 1
        self.assertGreaterEqual(kmeans_sil, -1)
        self.assertLessEqual(kmeans_sil, 1)
        if dbscan_sil != -1:  # -1 indicates no clusters found
            self.assertGreaterEqual(dbscan_sil, -1)
            self.assertLessEqual(dbscan_sil, 1)

        # Adjusted Rand Index should be between -1 and 1
        self.assertGreaterEqual(kmeans_ari, -1)
        self.assertLessEqual(kmeans_ari, 1)
        self.assertGreaterEqual(dbscan_ari, -1)
        self.assertLessEqual(dbscan_ari, 1)

        # Number of clusters should be positive integers
        self.assertIsInstance(kmeans_n, int)
        self.assertGreater(kmeans_n, 0)
        self.assertIsInstance(dbscan_n, int)
        self.assertGreaterEqual(dbscan_n, 0)  # DBSCAN can find 0 clusters if all points are noise

        # Number of noise points should be non-negative
        self.assertIsInstance(dbscan_noise, int)
        self.assertGreaterEqual(dbscan_noise, 0)

        # Test that K-means finds the expected number of clusters (3)
        self.assertEqual(kmeans_n, 3)

        # Test that metrics are reasonable for this dataset
        # With good synthetic data, we expect decent silhouette scores
        self.assertGreater(kmeans_sil, 0.3)  # K-means should perform reasonably well

        # ARI should be reasonably good since we're using synthetic data with known clusters
        self.assertGreater(kmeans_ari, 0.5)

    @classmethod
    def tearDownClass(cls):
        # Clean up the created file
        if os.path.exists('clustering_comparison_plot.png'):
            os.remove('clustering_comparison_plot.png')

if __name__ == '__main__':
    unittest.main()