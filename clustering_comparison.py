import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score, adjusted_rand_score
import matplotlib.pyplot as plt

def perform_clustering_comparison():
    # Generate sample data suitable for clustering
    # Create 3 clusters with 100 samples each
    X, true_labels = make_blobs(n_samples=300, centers=3, cluster_std=1.5, 
                               random_state=42, center_box=(-10.0, 10.0))
    
    # Apply K-means clustering
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    kmeans_labels = kmeans.fit_predict(X)
    
    # Apply DBSCAN clustering
    dbscan = DBSCAN(eps=1.5, min_samples=5)
    dbscan_labels = dbscan.fit_predict(X)
    
    # Calculate evaluation metrics
    # Silhouette Score (higher is better, range -1 to 1)
    kmeans_silhouette = silhouette_score(X, kmeans_labels)
    dbscan_silhouette = silhouette_score(X, dbscan_labels) if len(set(dbscan_labels)) > 1 else -1
    
    # Adjusted Rand Index compared to true labels (higher is better, range -1 to 1)
    kmeans_ari = adjusted_rand_score(true_labels, kmeans_labels)
    dbscan_ari = adjusted_rand_score(true_labels, dbscan_labels)
    
    # Count clusters found
    kmeans_n_clusters = len(set(kmeans_labels))
    dbscan_n_clusters = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)  # Exclude noise
    dbscan_n_noise = list(dbscan_labels).count(-1)
    
    # Create visualization
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    
    # Plot true clusters
    axes[0].scatter(X[:, 0], X[:, 1], c=true_labels, cmap='viridis', alpha=0.7)
    axes[0].set_title('True Clusters')
    axes[0].set_xlabel('Feature 1')
    axes[0].set_ylabel('Feature 2')
    
    # Plot K-means results
    axes[1].scatter(X[:, 0], X[:, 1], c=kmeans_labels, cmap='viridis', alpha=0.7)
    axes[1].scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], 
                   c='red', marker='x', s=200, linewidths=3, label='Centroids')
    axes[1].set_title(f'K-means Clustering (k={kmeans_n_clusters})')
    axes[1].set_xlabel('Feature 1')
    axes[1].set_ylabel('Feature 2')
    axes[1].legend()
    
    # Plot DBSCAN results
    axes[2].scatter(X[:, 0], X[:, 1], c=dbscan_labels, cmap='viridis', alpha=0.7)
    axes[2].set_title(f'DBSCAN Clustering ({dbscan_n_clusters} clusters, {dbscan_n_noise} noise)')
    axes[2].set_xlabel('Feature 1')
    axes[2].set_ylabel('Feature 2')
    
    plt.tight_layout()
    plt.savefig('clustering_comparison_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    return (kmeans_silhouette, kmeans_ari, kmeans_n_clusters,
            dbscan_silhouette, dbscan_ari, dbscan_n_clusters, dbscan_n_noise)

if __name__ == '__main__':
    results = perform_clustering_comparison()
    kmeans_sil, kmeans_ari, kmeans_n, dbscan_sil, dbscan_ari, dbscan_n, dbscan_noise = results
    
    print("Clustering Comparison Results:")
    print("=" * 50)
    print(f"K-means Clustering:")
    print(f"  - Clusters found: {kmeans_n}")
    print(f"  - Silhouette Score: {kmeans_sil:.4f}")
    print(f"  - Adjusted Rand Index: {kmeans_ari:.4f}")
    print()
    print(f"DBSCAN Clustering:")
    print(f"  - Clusters found: {dbscan_n}")
    print(f"  - Noise points: {dbscan_noise}")
    print(f"  - Silhouette Score: {dbscan_sil:.4f}")
    print(f"  - Adjusted Rand Index: {dbscan_ari:.4f}")
    print()
    print("Plot saved to clustering_comparison_plot.png")
    
    # Determine which algorithm performed better
    print("\nPerformance Comparison:")
    print("-" * 30)
    if kmeans_ari > dbscan_ari:
        print("K-means achieved better Adjusted Rand Index")
    elif dbscan_ari > kmeans_ari:
        print("DBSCAN achieved better Adjusted Rand Index")
    else:
        print("Both algorithms achieved similar Adjusted Rand Index")
        
    if kmeans_sil > dbscan_sil:
        print("K-means achieved better Silhouette Score")
    elif dbscan_sil > kmeans_sil:
        print("DBSCAN achieved better Silhouette Score")
    else:
        print("Both algorithms achieved similar Silhouette Score")