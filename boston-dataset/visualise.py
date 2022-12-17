import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

full_df = pd.read_csv('boston.csv')
print(full_df.head(50))
print(full_df.shape)

features = full_df[full_df.columns[:-1]]
target = full_df[[full_df.columns[-1]]]
print(features.head())
print(features.shape)
print(target.head())
print(target.shape)

print(full_df.corr(numeric_only=True)['median-value-in-k'])
# sns.set(style='ticks', color_codes=True)
# g = sns.pairplot(full_df)
# plt.show()