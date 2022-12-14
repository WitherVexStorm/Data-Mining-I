import pandas as pd
import sklearn.datasets
import matplotlib.pyplot as plt

def dataset_to_df(dataset):
    # print(dataset)
    df = pd.DataFrame(dataset['data'], columns=dataset['feature_names'])
    df['species'] = dataset['target']
    df['species'] = df['species'].replace(to_replace= [0, 1, 2], value = dataset['target_names'])
    return df

df = dataset_to_df(sklearn.datasets.load_iris())
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