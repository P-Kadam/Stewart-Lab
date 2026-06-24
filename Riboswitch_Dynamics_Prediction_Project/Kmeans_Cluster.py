import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Load the dataset
dataset = pd.read_csv("/Volumes/Stewart_Lab_External_Drive_PK/MCDB_198/combined_data/combined_data.csv")
dataset_new = dataset.copy()

# Encode the 'Configuration' column
le = LabelEncoder()
dataset_new["Configuration"] = le.fit_transform(dataset_new["Configuration"])
dataset_new = dataset_new.drop(["Simulation Code"], axis = 1)

#scale the features
scaler = StandardScaler()
features = ["Arms",
            "Temperature Condition (°C)",
            "Salt Concentration (M)",
            "P1 stem NT distance (nm)",
            "anti-P1 stem NT distance (SU)",
            "Potential Energy (SU)",
            "Kinetic Energy (SU)",
            "Total Energy (SU)",
            "Standard Rg (nm)",
            "Rg_X (nm)",
            "Rg_Y (nm)",
            "Rg_Z (nm)",
            "RMSD (Å)"]

X = dataset_new[features]
X_scaled = scaler.fit_transform(X)

#kmeans
kmeans = KMeans(n_clusters=4, n_init =10, random_state=1111)
cluster_labels = kmeans.fit_predict(X_scaled)

dataset_new['Cluster'] = cluster_labels

# PCA to reduce dimensionality for visualization
pca = PCA(n_components=2, random_state=1111)
X_pca = pca.fit_transform(X_scaled)

# Also reduce the cluster centroids to the same 2D PCA space
centroids_pca = pca.transform(kmeans.cluster_centers_)

# Store the 2D coordinates back into our DataFrame for plotting
dataset_new["PC1"] = X_pca[:, 0]
dataset_new["PC2"] = X_pca[:, 1]


#plot
# Set up the visualization style
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))

# Plot the 2D PCA points, color-coded by the K-means clusters
sns.scatterplot(
    data=dataset_new,
    x="PC1",
    y="PC2",
    hue="Cluster",
    palette="viridis",
    s=60,
    alpha=0.8
)

# Plot the centroids (which are now also transformed into 2D)
plt.scatter(
    centroids_pca[:, 0],
    centroids_pca[:, 1],
    s=250,
    c="red",
    marker="X",
    label="Centroids",
    edgecolors="black"
)

# Final plot adjustments
plt.title("K-Means Clustering: 2D PCA Projection", fontsize=14, fontweight="bold")
plt.xlabel("Principal Component 1")
plt.ylabel("Principal Component 2")
plt.legend(title="Clusters")

plt.savefig("kmeans_pca_plot_k=4.png")

plt.figure(figsize=(10, 5))

#interpreting the clusters

# 1. Combine your original feature data with the new cluster IDs
df_profiles = dataset_new[features].copy()
df_profiles["cluster_id"] = cluster_labels

# 2. Group by cluster and calculate the mean for each feature
cluster_summary = df_profiles.groupby("cluster_id").mean()

# 3. Display the table
print("=== CLUSTER FEATURE MEANS ===")
print(cluster_summary)

# Plot a heatmap of the averages (transposed so features run down the side)
sns.heatmap(
    cluster_summary.T, 
    annot=True,          # Show the actual numbers inside the boxes
    fmt=".2f",          # Limit decimals to 2 places
    cmap="YlGnBu",      # Clear color gradient
    linewidths=0.5
)

plt.title("Feature Profiles by Cluster (Averages)", fontsize=14, fontweight="bold")
plt.xlabel("Cluster ID")
plt.ylabel("Features")

plt.savefig("cluster_feature_profiles.png")