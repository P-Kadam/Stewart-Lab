from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn import metrics
from scipy.spatial.distance import cdist
from sklearn.preprocessing import LabelEncoder, StandardScaler
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
 

# Load the dataset
dataset = pd.read_csv("/Volumes/Pradnya_Research_Data/Stewart_Lab_Data/combined_data/combined_data.csv")
dataset_new = dataset.copy()

# Encode the 'Configuration' column
le = LabelEncoder()
dataset_new["Configuration"] = le.fit_transform(dataset_new["Configuration"])
dataset_new = dataset_new.drop(["Simulation Code"], axis = 1)

#scaling the features
scaler = StandardScaler()
dataset_arr = scaler.fit_transform(dataset_new)

# ── PCA: reduce to 2D for visualization ──────────────────────────────────────

pca        = PCA(n_components=2)
pca_coords = pca.fit_transform(dataset_arr)

print(f"Variance explained by PC1 + PC2: "
      f"{pca.explained_variance_ratio_.sum() * 100:.1f}%\n")


# Convert to numpy array before indexing
dataset_new_array = dataset_new.values  # or np.array(dataset_new)

##################
# Elbow method to determine optimal number of clusters
##################

# distortions = []
# inertias = []
# mapping1 = {}
# mapping2 = {}

# K = range(1, 10)

# for k in K:
#     kmeanModel = KMeans(n_clusters=k, random_state=1111).fit(dataset_new)

#     distortions.append(sum(np.min(cdist(dataset_new, kmeanModel.cluster_centers_, 'euclidean'),
#                                    axis=1)**2) / dataset_new.shape[0])
    
#     inertias.append(kmeanModel.inertia_)

#     mapping1[k] = distortions[-1]
#     mapping2[k] = inertias[-1]

#     best_k_distortion = max(mapping1, key=mapping1.get)
#     best_k_inertia = max(mapping2, key=mapping2.get)


# print("Distortion values:")
# for key, val in mapping1.items():
#     print(f'{key} : {val}')

# plt.plot(K, distortions, 'bx-')
# plt.xlabel('Number of Clusters (k)')
# plt.ylabel('Distortion')
# plt.title('The Elbow Method using Distortion')
# plt.savefig("Elbow_Distortion.png")
# plt.savefig("Elbow_Distortion.svg")
# plt.clf()

# print("Inertia values:")
# for key, val in mapping2.items():
#     print(f'{key} : {val}')

# plt.plot(K, inertias, 'bx-')
# plt.xlabel('Number of Clusters (k)')
# plt.ylabel('Inertia')
# plt.title('The Elbow Method using Inertia')
# plt.savefig("Elbow_Inertia.png")
# plt.savefig("Elbow_Inertia.svg")
# plt.clf()

# k_range = range(1, 5)

# for k in k_range:
#     kmeans = KMeans(n_clusters=k, init='k-means++', random_state=42)
#     y_kmeans = kmeans.fit_predict(dataset_new_array)
    
#     plt.scatter(dataset_new_array[:, 0], dataset_new_array[:, 1], c=y_kmeans, cmap='viridis', marker='o', edgecolor='k', s=100)
#     plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
#                 s=300, c='red', label='Centroids', edgecolor='k')
#     plt.title(f'K-means Clustering (k={k})')
#     plt.xlabel('Feature 1')
#     plt.ylabel('Feature 2')
#     plt.legend()
#     plt.grid()
#     plt.savefig(f'kmeans_k_{k}.png')
#     plt.savefig(f'kmeans_k_{k}.svg')

# ks_to_plot = sorted(set(range(2, 6)) | {best_k_distortion, best_k_inertia})

# for k in ks_to_plot:
#     km     = KMeans(n_clusters=k, init="k-means++", random_state=1111, n_init=10)
#     labels = km.fit_predict(dataset_arr)

#     # Project centroids into PCA space for plotting
#     centers_pca = pca.transform(km.cluster_centers_)

#     plt.figure(figsize=(7, 5))
#     scatter = plt.scatter(
#         pca_coords[:, 0], pca_coords[:, 1],
#         c=labels, cmap="viridis", marker="o", edgecolor="k", s=80, alpha=0.8,
#     )
#     plt.scatter(
#         centers_pca[:, 0], centers_pca[:, 1],
#         s=300, c="red", marker="X", label="Centroids", edgecolor="k", zorder=5,
#     )
#     plt.colorbar(scatter, label="Cluster")
#     plt.title(
#         f"K-means (k={k})  —  PCA projection\n"
#         f"PC1 {pca.explained_variance_ratio_[0]*100:.1f}%  |  "
#         f"PC2 {pca.explained_variance_ratio_[1]*100:.1f}%"
#         + ("  ★ best k" if k == best_k_distortion else "")
#         + ("  ★ best k" if k == best_k_inertia else "")
#     )
#     plt.xlabel("Principal Component 1")
#     plt.ylabel("Principal Component 2")
#     plt.legend()
#     plt.tight_layout()
#     plt.savefig(f"kmeans_pca_k{k}.png")
#     plt.savefig(f"kmeans_pca_k{k}.svg")
#     plt.clf()

#     # ── Save cluster labels for best k back to original dataset ─────────────────

# km_best_dist          = KMeans(n_clusters=best_k_distortion, init="k-means++", random_state=1111, n_init=10)
# km_best_inertia       = KMeans(n_clusters=best_k_inertia, init="k-means++", random_state=1111, n_init=10)
# dataset["Cluster_distortion"] = km_best_dist.fit_predict(dataset_arr)
# dataset["Cluster_inertia"] = km_best_inertia.fit_predict(dataset_arr)
# dataset.to_csv("combined_data_clustered.csv", index=False)
# print(f"\nCluster labels saved to combined_data_clustered.csv")
# print(dataset["Cluster_distortion"].value_counts().sort_index())
# print(dataset["Cluster_inertia"].value_counts().sort_index())

km4 = KMeans(n_clusters=4, init="k-means++", random_state=1111, n_init=10)
labels4 = km4.fit_predict(dataset_arr)

km5 = KMeans(n_clusters=5, init="k-means++", random_state=1111, n_init=10)
labels5 = km5.fit_predict(dataset_arr)

#Assign labels BEFORE the loop
dataset["Clusters_4"] = labels4
dataset["Clusters_5"] = labels5

# Project centroids into PCA space for plotting
centers_pca_4 = pca.transform(km4.cluster_centers_)
centers_pca_5 = pca.transform(km5.cluster_centers_)

features = [col for col in dataset.columns if col not in ["Cluster", "Clusters_4", "Clusters_5", "Simulation Code", "Configuration"]]

import matplotlib.pyplot as plt

features = [col for col in dataset.columns if col not in ["Cluster", "Clusters_4", "Clusters_5"]]

# Plot distributions for k=4
# for feature in features:
#     plt.figure()
#     for cluster in sorted(dataset["Clusters_4"].unique()):
#         subset = dataset[dataset["Clusters_4"] == cluster][feature]
#         subset.hist(alpha=0.5, label=f"Cluster {cluster}", bins=20)
#     plt.title(f"Distribution of {feature} — k=4")
#     plt.xlabel(feature)
#     plt.ylabel("Count")
#     plt.legend()
#     plt.tight_layout()
#     plt.savefig(f"distribution_k4_{feature}.png")
#     plt.clf()

# # Plot distributions for k=5
# for feature in features:
#     plt.figure()
#     for cluster in sorted(dataset["Clusters_5"].unique()):
#         subset = dataset[dataset["Clusters_5"] == cluster][feature]
#         subset.hist(alpha=0.5, label=f"Cluster {cluster}", bins=20)
#     plt.title(f"Distribution of {feature} — k=5")
#     plt.xlabel(feature)
#     plt.ylabel("Count")
#     plt.legend()
#     plt.tight_layout()
#     plt.savefig(f"distribution_k5_{feature}.png")
#     plt.clf()


# See how Simulation Code, Temperature, and Salt Concentration map to each cluster
cols_of_interest = ["Simulation Code"]

# for cluster_col in ["Clusters_4", "Clusters_5"]:
#     k = cluster_col.split("_")[1]
#     for col in cols_of_interest:
#         ct = pd.crosstab(dataset[col], dataset[cluster_col])
#         ct.to_csv(f"crosstab_k{k}_{col.replace(' ', '_')}.csv")

from sklearn.metrics import silhouette_score

for k, cluster_col in [(4, "Clusters_4"), (5, "Clusters_5")]:
    score = silhouette_score(dataset_arr, dataset[cluster_col])
    print(f"k={k}  overall silhouette={score:.4f}")











##################################################################################

# import matplotlib.pyplot as plt
# import pandas as pd
# import numpy as np
# import seaborn as sns

# from sklearn.preprocessing import StandardScaler
# from sklearn.cluster import KMeans
# from sklearn.metrics import silhouette_score
# from  sklearn.decomposition import PCA

# dataset = pd.read_csv("/Volumes/Pradnya_Research_Data/Stewart_Lab_Data/combined_data/combined_data.csv")

# metadata =["Simulation Code", "Configuration", "Temperature Condition (°C)", 
#                     "Salt Condition (M)", "Arms"]

# features = ["P1 stem NT distance (nm)",
#             "anti-P1 stem NT distance (SU)",
#             "Potential Energy (SU)",
#             "Kinetic Energy (SU)",
#             "Total Energy (SU)",
#             "Average Contact Map",
#             "Standard Rg (nm)",
#             "Rg_X (nm)",
#             "Rg_Y (nm)",
#             "Rg_Z (nm)",
#             "RMSD (Å)"]

# # Scale the data
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(dataset[features])

# #finding the optimal number of clusters using the elbow method
# silhouette_scores = []

# k_range = range(2, 11)

# print("\nTesting different values of k...")
# for k in k_range:
#     kmeans = KMeans(n_clusters=k, random_state=1111, n_init=10)
#     labels = kmeans.fit_predict(X_scaled)

#     silhouette_scores.append(silhouette_score(X_scaled, labels))
#     print(f"k={k}: silhouette={silhouette_scores[-1]:.3f}")

# best_silhouette_k = k_range[silhouette_scores.index(max(silhouette_scores))]

# # Plotting the silhouette scores
# plt.figure(figsize=(8, 5))
# plt.plot(k_range, silhouette_scores, marker='o')
# plt.title("Silhouette Scores for KMeans Clustering")
# plt.xlabel("Number of Clusters (k)")
# plt.ylabel("Silhouette Score")
# plt.xticks(k_range)
# plt.grid()
# plt.savefig("silhouette_scores.png")

# print(f"\nBest k by silhouette score: {best_silhouette_k}")

# #fitting kmeans with the optimal number of clusters
# kmeans_optimal = KMeans(n_clusters=best_silhouette_k, random_state=1111, n_init=10)
# y_pred = kmeans_optimal.fit_predict(X_scaled)
# optimal_k = best_silhouette_k

# #PCA for visualization
# pca = PCA(n_components=2)
# X_pca = pca.fit_transform(X_scaled)

# dataset['PCA1'] = X_pca[:, 0]
# dataset['PCA2'] = X_pca[:, 1]

# print(f"\nVariance explained:")
# print(f"  PC1: {pca.explained_variance_ratio_[0]:.1%}")
# print(f"  PC2: {pca.explained_variance_ratio_[1]:.1%}")
# print(f"  Total: {sum(pca.explained_variance_ratio_[:2]):.1%}")

# fig, ax = plt.subplots(figsize=(8, 6))
# sns.scatterplot(data=dataset, x='PCA1', y='PCA2', hue=y_pred, palette='Set2', ax=ax)
# ax.set_title(f"KMeans Clustering with k={optimal_k}")
# ax.legend(title='Cluster')
# plt.savefig("kmeans_clusters.png")

# cluster_colors = ['#e74c3c', '#3498db', '#2ecc71', '#f39c12',
#                   '#9b59b6', '#1abc9c', '#e67e22', '#34495e']

# fig, axes = plt.subplots(2, 2, figsize=(16, 12))
# axes = axes.flatten()

# # Panel 1: Colored by cluster
# for cluster in range(optimal_k):
#     mask = dataset['Cluster'] == cluster
#     axes[0].scatter(
#         dataset.loc[mask, 'PCA1'],
#         dataset.loc[mask, 'PCA2'],
#         c=cluster_colors[cluster],
#         label=f'Cluster {cluster} (n={mask.sum():,})',
#         alpha=0.3,
#         s=2
#     )
# axes[0].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)", fontsize=11)
# axes[0].set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)", fontsize=11)
# axes[0].set_title('K-Means Clusters', fontsize=13)
# axes[0].legend(markerscale=4, fontsize=9)

# # Panel 2: Colored by ON/OFF configuration
# conf_colors = {'ON': '#2ecc71', 'OFF': '#e74c3c'}
# for conf in ['ON', 'OFF']:
#     mask = dataset['Configuration'] == conf
#     axes[1].scatter(
#         dataset.loc[mask, 'PCA1'],
#         dataset.loc[mask, 'PCA2'],
#         c=conf_colors[conf],
#         label=f'{conf} (n={mask.sum():,})',
#         alpha=0.3,
#         s=2
#     )
# axes[1].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)", fontsize=11)
# axes[1].set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)", fontsize=11)
# axes[1].set_title('ON/OFF Configuration', fontsize=13)
# axes[1].legend(markerscale=4, fontsize=9)

# # Panel 3: Colored by temperature
# temps = sorted(dataset['Temperature Condition (°C)'].unique())
# temp_colors = ['#f39c12', '#e74c3c', '#9b59b6']
# for i, temp in enumerate(temps):
#     mask = dataset['Temperature Condition (°C)'] == temp
#     axes[2].scatter(
#         dataset.loc[mask, 'PCA1'],
#         dataset.loc[mask, 'PCA2'],
#         c=temp_colors[i],
#         label=f'{temp}°C (n={mask.sum():,})',
#         alpha=0.3,
#         s=2
#     )
# axes[2].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)", fontsize=11)
# axes[2].set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)", fontsize=11)
# axes[2].set_title('Temperature Condition', fontsize=13)
# axes[2].legend(markerscale=4, fontsize=9)

# # Panel 4: Colored by salt concentration
# salts = sorted(dataset['Salt Concentration (M)'].unique())
# salt_colors = ['#1abc9c', '#3498db', '#2c3e50']
# for i, salt in enumerate(salts):
#     mask = dataset['Salt Concentration (M)'] == salt
#     axes[3].scatter(
#         dataset.loc[mask, 'PCA1'],
#         dataset.loc[mask, 'PCA2'],
#         c=salt_colors[i],
#         label=f'{salt}M (n={mask.sum():,})',
#         alpha=0.3,
#         s=2
#     )
# axes[3].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)", fontsize=11)
# axes[3].set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)", fontsize=11)
# axes[3].set_title('Salt Concentration', fontsize=13)
# axes[3].legend(markerscale=4, fontsize=9)

# plt.suptitle(f'K-Means Clustering (k={optimal_k}) — PCA Projection', fontsize=16)
# plt.tight_layout()
# plt.savefig('kmeans_clusters.png', dpi=300, bbox_inches='tight')
# plt.show()
