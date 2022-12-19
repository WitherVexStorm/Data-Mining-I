import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
import seaborn as sns
import sklearn.datasets
import matplotlib.pyplot as plt

def dataset_to_df(dataset):
    # print(dataset)
    df = pd.DataFrame(dataset['data'], columns=dataset['feature_names'])
    df['species'] = dataset['target']
    df['species'] = df['species'].replace(to_replace= [0, 1, 2], value = dataset['target_names'])
    return df, dataset['feature_names'], 'species', dataset['target_names']

df, features, target, target_names = dataset_to_df(sklearn.datasets.load_iris())
print(df.head(50))
print(df.shape)

figure, plots = plt.subplots(nrows=1, ncols=2)
plots[0].set_xlabel('sepal length (cm)')
plots[0].set_ylabel('sepal width (cm)')
plots[0].set_title('Sepal width vs height analysis of Iris')
plots[0].scatter(df['sepal length (cm)'].iloc[0:50], df['sepal width (cm)'].iloc[0:50], c='red', label='setosa')
plots[0].scatter(df['sepal length (cm)'].iloc[50:100], df['sepal width (cm)'].iloc[50:100], c='blue', label='versicolor')
plots[0].scatter(df['sepal length (cm)'].iloc[100:150], df['sepal width (cm)'].iloc[100:150], c='green', label='virginica')
plots[0].legend()
plots[1].set_xlabel('petal length (cm)')
plots[1].set_ylabel('petal width (cm)')
plots[1].set_title('Petal width vs height analysis of Iris')
plots[1].scatter(df['petal length (cm)'].iloc[0:50], df['petal width (cm)'].iloc[0:50], c='red', label='setosa')
plots[1].scatter(df['petal length (cm)'].iloc[50:100], df['petal width (cm)'].iloc[50:100], c='blue', label='versicolor')
plots[1].scatter(df['petal length (cm)'].iloc[100:150], df['petal width (cm)'].iloc[100:150], c='green', label='virginica')
plots[1].legend()
plt.show()

'''
Notes:
    Setosa petals are smallest in both width and height
    Versicolor petals are much bigger in comparision
    Virginica petals are even bigger in comparison
'''

X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=1)
figure, plots = plt.subplots(nrows=1, ncols=2)
plots[0].set_xlabel('sepal length (cm)')
plots[0].set_ylabel('sepal width (cm)')
plots[0].set_title('Train and Test data of Iris')
plots[0].scatter(X_train['sepal length (cm)'], X_train['sepal width (cm)'], c='red', label='train')
plots[0].scatter(X_test['sepal length (cm)'], X_test['sepal width (cm)'], c='blue', label='test')
plots[0].legend()
plots[1].set_xlabel('petal length (cm)')
plots[1].set_ylabel('petal width (cm)')
plots[1].set_title('Train and Test data of Iris')
plots[1].scatter(X_train['petal length (cm)'], X_train['petal width (cm)'], c='red', label='train')
plots[1].scatter(X_test['petal length (cm)'], X_test['petal width (cm)'], c='blue', label='test')
plots[1].legend()
plt.show()

'''
Notes:
    There is an even spread of training and testing data
    We will train model, predict test data and evaluate performance
    Performance metrics = confusion matrix, accuracy and classification report
'''

model = DecisionTreeClassifier(criterion='gini', random_state=1, max_depth=3)
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print('Prediction Results:')
for yp, yt in zip(y_pred, y_test):
    print('Predicted: "' + yp.ljust(15) + '" and Actual: "' + yt.ljust(15) + ('" correctly' if yp == yt else '" incorrectly'), 'classified' )
print('Overall:', sum([1 if yp == yt else 0 for yp, yt in zip(y_pred, y_test)]), '/', len(y_test))
print('')
print('Confusion Matrix:')
print(confusion_matrix(y_test, y_pred))
print('')
print('Accuracy:')
print(accuracy_score(y_test, y_pred) * 100)
print('')
print('Classification Report:')
print(classification_report(y_test, y_pred))
ConfusionMatrixDisplay(confusion_matrix = confusion_matrix(y_test, y_pred), display_labels = target_names).plot()
plt.show()
sns.heatmap(pd.DataFrame(classification_report(y_test, y_pred, target_names=target_names, output_dict=True)).iloc[:-1, :].T, annot=True)
plt.show()

'''
Notes:
    We get a high accuracy, 29/30 correctly classified = 96.66% accuracy
    Since the values of features for each target class is sufficiently distinct,
    a simple Decision Tree can give a great performance.
'''