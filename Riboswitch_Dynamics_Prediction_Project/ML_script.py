import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

from boruta import BorutaPy

from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.feature_selection import RFECV
from sklearn.metrics import f1_score, accuracy_score
from sklearn.cluster import KMeans
import seaborn as sns

np.int = int
np.float = float
np.bool = bool

dataset = pd.read_csv("/Volumes/Stewart_Lab_External_Drive_PK/MCDB_198/combined_data/combined_data.csv")

np.random.seed(1111)
train, test = train_test_split(dataset, test_size = 0.2)
print("☑️ CHECKPOINT: Data split into train and test sets")

def prep_data(df_data):
    
    #copying the data to avoid modifying original dataframe
    df = df_data.copy()

    #encoding the configuration labels to be used for classification
    le = preprocessing.LabelEncoder()
    df["Configuration"] = le.fit_transform(df["Configuration"])

    #dropping the simulation code column since it is not a feature that we want to use for classification
    df = df.drop(["Simulation Code"], axis = 1)

    #separating the features and labels for the data
    X = df.drop("Configuration", axis = 1)
    y = df["Configuration"]

    return X, y

dataset_new = dataset.copy()

print(dataset_new.columns.tolist())
print(dataset_new.shape)


# now applying the prep data function to the test and train datasets
Xtrain, ytrain = prep_data(train)
Xtest, ytest = prep_data(test)

print("☑️ CHECKPOINT: Data preprocessed and ready for training and testing")


# RF1 = RandomForestClassifier(n_estimators=100, random_state=1111)
# print("R1:", cross_val_score(RF1, Xtrain, ytrain, cv = 7).mean())
# # 1.0

# cols = ["Temperature Condition (°C)", "Salt Concentration (M)", "P1 stem NT distance (nm)"]
# RF2 = RandomForestClassifier(n_estimators=100, random_state=1111)
# print("R2:", cross_val_score(RF2, Xtrain[cols], ytrain, cv = 4).mean())
# # 0.937673611111111

# cols = ["Temperature Condition (°C)", "Salt Concentration (M)", "P1 stem NT distance (nm)", "anti-P1 stem NT distance (SU)"]
# RF3 = RandomForestClassifier(n_estimators=100, random_state=1111)
# print("R3:", cross_val_score(RF3, Xtrain[cols], ytrain, cv = 2).mean())
# # 0.9883854166666667

# cols = ["Temperature Condition (°C)", "Salt Concentration (M)", "P1 stem NT distance (nm)", "anti-P1 stem NT distance (SU)", "Potential Energy (SU)"]
# RF4 = RandomForestClassifier(n_estimators=100, random_state=1111)
# print("R4:", cross_val_score(RF4, Xtrain[cols], ytrain, cv = 3).mean())
# # 0.9936805555555556

cols = ["Temperature Condition (°C)", "Salt Concentration (M)", "P1 stem NT distance (nm)", "Potential Energy (SU)", "Average Contact Map"]
RF5 = RandomForestClassifier(n_estimators=100, random_state=1111)
print("R5:", cross_val_score(RF5, Xtrain[cols], ytrain, cv = 3).mean())
# 0.9999652777777778

# #USING R5 FEATURES FOR THE MODEL SINCE IT HAS THE HIGHEST CROSS-VALIDATION SCORE
train_score = RF5.fit(Xtrain[cols], ytrain).score(Xtrain[cols], ytrain)
test_score = RF5.score(Xtest[cols], ytest)

print(f"☑️ CHECKPOINT: Model trained. Train score: {train_score}, Test score: {test_score}")

#### CHECKING THE F1 SCORE OF THE MODEL ON THE TEST SET ####
y_pred = RF5.predict(Xtest[cols])
f1 = f1_score(ytest, y_pred)
accuracy = accuracy_score(ytest, y_pred)
print(f"☑️ CHECKPOINT: F1 score on test set: {f1}")


#### K-MEANS CLUSTERING ####
# kmeans1 = KMeans(n_clusters=2, random_state=1111)
# kmeans1.fit(dataset_new)
# plt.title("2 clusters")
# plt.scatter(X[:, 0], X[:, 1], c=y_pred)
# plt.savefig("2_clusters.png")

# kmeans2 = KMeans(n_clusters=4, random_state=1111)
# kmeans2.fit(dataset_new)
# plt.title("4 clusters")
# plt.savefig("4_clusters.png")

# kmeans3 = KMeans(n_clusters=8, random_state=1111)
# kmeans3.fit(dataset_new)
# plt.title("8 clusters")
# plt.savefig("8_clusters.png")

# kmeans4 = KMeans(n_clusters=10, random_state=1111)
# kmeans4.fit(dataset_new)
# plt.title("10 clusters")
# plt.savefig("10_clusters.png")

# kmeans5 = KMeans(n_clusters=20, random_state=1111)
# kmeans5.fit(dataset_new)
# plt.scatter(X[:, 0], X[:, 1], c=y_pred)
# plt.title("20 clusters")
# plt.savefig("20_clusters.png")

# print("☑️ CHECKPOINT: K-means clustering complete")


###################################################################################################
## CHECKING THE OOB ERROR TO DETERMINE THE OPTIMAL NUMBER OF TREES IN THE RANDOM FOREST CLASSIFIER
###################################################################################################

oob_errors = []
tree_range = range(10, 200, 5)


for n in tree_range:
    print("☑️ CHECKPOINT: trees: ", n)
    RF = RandomForestClassifier(n_estimators=n, random_state=0, oob_score=True)
    RF.fit(Xtrain, ytrain)
    oob_errors.append(1 - RF.oob_score_)

plt.rcParams['svg.fonttype'] = 'none'

plt.plot(tree_range, oob_errors, marker='o', linestyle='-')
plt.xlabel("Number of Trees")
plt.ylabel("OOB Error")
plt.title("OOB Error vs Number of Trees")
plt.savefig("OOB_Error_vs_Trees_2.svg")

##############################################################
## CHECKING FEATURE IMPORTANCE USING BORUTA
##############################################################

#initializing the model
RF = RandomForestClassifier(n_jobs=-1, class_weight="balanced", max_depth=5)

# initializing Boruta
feature_selector = BorutaPy(RF, n_estimators="auto", verbose=2, random_state=1)

#fit boruta to training data
feature_selector.fit(Xtrain.values, ytrain.values)


feature_names = Xtrain.columns
confirmed_features = feature_names[feature_selector.support_].tolist()
tentative_features = feature_names[feature_selector.support_weak_].tolist()


feature_importance = feature_selector.ranking_

features_df = pd.DataFrame({'Feature': feature_names, 
                            'Rank': feature_importance})

print(features_df.sort_values(by='Rank'))
#results:
print(f"Confirmed features: {feature_selector.support_}")
print(f"Feature ranking: {feature_selector.ranking_}")
print((f"Tentative features: {feature_selector.support_weak_}"))

ranking_df = pd.DataFrame({'Feature': feature_names, 'Rank': feature_selector.ranking_})
print("\nFull Feature Ranking:")
print(ranking_df.sort_values(by='Rank'))

# color_map = {
#     'Accepted': "blue",
#     'Tentative': 'white',
#     'Rejected': '#e74c3c'
# }

# plt.figure(figsize=(12, 6))
# plt.barh(features_df['Feature'], 
#          features_df['Rank'],
#            color=features_df['Rank'].apply(lambda x: color_map['Accepted'] if x == 1 else (color_map['Tentative'] if x == 2 else color_map['Rejected'])),
#            edgecolor='black',
#            linewidth=1)

# plt.xlabel('Boruta Ranking (lower = more important)', fontsize=12)
# plt.title('Boruta Feature Selection Rankings', fontsize=14)

# from matplotlib.patches import Patch
# legend_elements = [
#     Patch(facecolor='blue', label='Accepted'),
#     Patch(facecolor='white', label='Tentative'),
#     Patch(facecolor='#e74c3c', label='Rejected')
# ]
# plt.legend(handles=legend_elements)
# plt.tight_layout()
# plt.savefig("Boruta_Feature_Rankings.png", dpi=300, bbox_inches='tight')
# plt.show()

