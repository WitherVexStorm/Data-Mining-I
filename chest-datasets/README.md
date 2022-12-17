# Chest Datasets

[Back to root folder](/../../)
## About
---
Fetch, clean, integrate and transform multiple datasets for mining.

Data sources:
- https://www.kaggle.com/datasets/nih-chest-xrays/data?select=Data_Entry_2017.csv
- https://github.com/ieee8023/covid-chestxray-dataset

## Tasks
---
Load covid dataset using `pandas`.

If covid dataset doesn't exist locally, load and save it from url to `data/covid_metadata.csv` and save date of download in `data/snapshots.json`.

If covid dataset updated after last download, load and save it from url to `data/covid_metadata.csv` and save new date of download in `data/snapshots.json`.

Output:

![](datasample.drawio.svg)