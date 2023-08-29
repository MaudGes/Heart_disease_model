
import pandas as pd

import sklearn
import joblib

from sklearn import neighbors
from sklearn.model_selection import train_test_split



#Importing dataset
heart_disease = pd.read_csv("heart_disease_health_indicators_BRFSS2015.csv")

#Split in features and labels ; X = independant variables ;  y = dependant variable
X = heart_disease[['HighBP','HighChol','CholCheck','BMI','Smoker','Stroke','Diabetes','PhysActivity','Fruits','Veggies','HvyAlcoholConsump','AnyHealthcare','NoDocbcCost','GenHlth','MentHlth','PhysHlth','DiffWalk','Sex','Age','Education','Income']]
y = heart_disease["HeartDiseaseorAttack"]
print(X.shape)
print(y.shape)



#Defining the proportion of data that will be used to verify the model = 30% of the data.
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size = 0.3)


#Defining the k value and selecting what weight will be given to close data points
knn = neighbors.KNeighborsClassifier(n_neighbors = 45, weights = 'uniform')


#Training the model
hda_model = knn.fit(X_train, y_train)


#Creating predictions 
prediction = knn.predict(X_test)


# Save the model
joblib.dump(knn, 'hda_model_knn.pkl')




