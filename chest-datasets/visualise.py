import pandas
import json
import os
from urllib.request import urlopen
from datetime import datetime
import pathlib

DATE_TIME_PATTERN = '%Y-%m-%dT%H:%M:%SZ'

def load_covid_data():
    '''
    If dataset doesn't exist, load and save it and save date of download

    If dataset updated after last download, load and save it and save new date of download

    Return the dataset
    '''

    COVID_DATASET_URL = 'https://raw.githubusercontent.com/ieee8023/covid-chestxray-dataset/master/metadata.csv'
    COVID_DATASET_SAVE_NAME = 'data/covid_metadata.csv'
    COVID_SNAPSHOT_URL = 'https://api.github.com/repos/ieee8023/covid-chestxray-dataset/commits?path=metadata.csv&page=1&per_page=1'
    COVID_DATASET_IMAGE_BASE_URL = 'https://github.com/ieee8023/covid-chestxray-dataset/raw/master/images/'

    try:
        # Try to create file, if doesn't exist, init snapshot to empty dict
        os.mkdir('data')
        with open('data/snapshots.json', 'x') as read_file:
            snapshots = {}
    except FileExistsError:
        # File exists, init snapshot to file contents
        with open('data/snapshots.json', 'r') as read_file: 
            snapshots = json.load(read_file)

    print(snapshots)

    LAST_COVID_DATASET_UPDATE_DATE = json.loads(urlopen(COVID_SNAPSHOT_URL).read())[0]['commit']['author']['date']

    try:
        # If dataset doesn't exist (and snapshot doesn't exist), or dataset updated after snapshot taken, re download dataset
        if not pathlib.Path(COVID_DATASET_SAVE_NAME).is_file():
            raise KeyError
        if datetime.strptime(LAST_COVID_DATASET_UPDATE_DATE, DATE_TIME_PATTERN) > datetime.strptime(snapshots['covid_snapshot_date'], DATE_TIME_PATTERN):
            raise KeyError

        # Else normally read dataset
        full_df = pandas.read_csv(COVID_DATASET_SAVE_NAME)
    except KeyError:
        full_df = pandas.read_csv(COVID_DATASET_URL)
        full_df.to_csv(COVID_DATASET_SAVE_NAME, index=False)
        snapshots['covid_snapshot_date'] = datetime.today().strftime(DATE_TIME_PATTERN)
        with open('data/snapshots.json', 'w') as write_file:
            json.dump(snapshots, write_file)

    return full_df

full_df = load_covid_data()
print(full_df.head(50))
print(full_df.shape)
