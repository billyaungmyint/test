import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs

class KMeans:
    def __init__(self, n_clusters=3, max_iter=300, random_state=None):
        self.n_clusters = n_clusters
        self.max_iter = max_iter
        self.random_state = random_state
        self.centroids = None
        self.labels = None

    def fit(self, X):
        if self.random_state:
            np.random.seed(self.random_state)

        # Initialize centroids randomly
        initial_indices = np.random.choice(X.shape[0], self.n_clusters, replace=False)
        self.centroids = X[initial_indices]

        for _ in range(self.max_iter):
            # Assign labels
            self.labels = self._assign_labels(X)

            # Update centroids
            new_centroids = self._update_centroids(X)

            # Check for convergence
            if np.allclose(self.centroids, new_centroids):
                break

            self.centroids = new_centroids

    def predict(self, X):
        return self._assign_labels(X)

    def _assign_labels(self, X):
        distances = np.sqrt(((X[:, np.newaxis] - self.centroids) ** 2).sum(axis=2))
        return np.argmin(distances, axis=1)

    def _update_centroids(self, X):
        new_centroids = np.array([X[self.labels == i].mean(axis=0) for i in range(self.n_clusters)])
        return new_centroids

if __name__ == '__main__':
    # Generate sample data
    X, y = make_blobs(n_samples=300, centers=3, cluster_std=1.5, random_state=42)

    # Apply K-means from scratch
    kmeans = KMeans(n_clusters=3, random_state=42)
    kmeans.fit(X)
    labels = kmeans.predict(X)

    # Plotting the results
    plt.figure(figsize=(8, 6))
    plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', alpha=0.7, label='Data Points')
    plt.scatter(kmeans.centroids[:, 0], kmeans.centroids[:, 1], c='red', marker='x', s=200, linewidths=3, label='Centroids')
    plt.title('K-Means Clustering (from Scratch)')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.legend()
    plt.savefig('kmeans_scratch_plot.png')
    plt.close()

    print("K-Means from scratch complete. Plot saved to 'kmeans_scratch_plot.png'")