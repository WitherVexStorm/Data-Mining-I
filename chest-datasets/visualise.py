import pandas
import json
import os
from urllib.request import urlopen
from datetime import datetime
import pathlib
import kaggle

COVID_DATE_TIME_PATTERN = '%Y-%m-%dT%H:%M:%SZ'
NIH_DATE_TIME_PATTERN = '%Y-%m-%d %H:%M:%S'

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
        if datetime.strptime(LAST_COVID_DATASET_UPDATE_DATE, COVID_DATE_TIME_PATTERN) > datetime.strptime(snapshots['covid_snapshot_date'], COVID_DATE_TIME_PATTERN):
            raise KeyError

        # Else normally read dataset
        full_df = pandas.read_csv(COVID_DATASET_SAVE_NAME)
    except KeyError:
        # Download and save data and snapshot date
        full_df = pandas.read_csv(COVID_DATASET_URL)
        full_df.to_csv(COVID_DATASET_SAVE_NAME, index=False)
        snapshots['covid_snapshot_date'] = datetime.today().strftime(COVID_DATE_TIME_PATTERN)
        with open('data/snapshots.json', 'w') as write_file:
            json.dump(snapshots, write_file)

    return full_df

def load_nih_data():
    '''
    If dataset doesn't exist, load and save it and save date of download

    If dataset updated after last download, load and save it and save new date of download

    Return the dataset
    '''

    NIH_DATASET_SAVE_NAME = 'nih_metadata.csv'
    kaggle.api.authenticate()
    
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

    # res = kaggle.api.dataset_download_file(dataset='nih-chest-xrays/data', file_name='images_001/images/00000001_000.png', path='data/')
    # print(res)
    # dataset_list = kaggle.api.dataset_list(search='nih')
    # print(dataset_list)
    # dataset = vars(dataset_list[0])
    # print(dataset)
    print(kaggle.api.dataset_status(dataset='nih-chest-xrays/data'))
    print(kaggle.api.dataset_list_files('nih-chest-xrays/data').files)
    # filename = kaggle.api.dataset_list_files(dataset['ref']).files
    # print(filename, filename[7])
    # print('File downloaded? ', kaggle.api.dataset_download_file(dataset=dataset['ref'], file_name='/kaggle/input/data/Data_Entry_2017.csv', path='data/'))
    # print(kaggle.api.dataset_list_files(dataset['ref']), kaggle.api.dataset_list_files(dataset['ref']).files)

    try:
        # If dataset doesn't exist (and snapshot doesn't exist), or dataset updated after snapshot taken, re download dataset
        if not pathlib.Path(NIH_DATASET_SAVE_NAME).is_file():
            raise KeyError
        if dataset['lastUpdated'] > datetime.strptime(snapshots['nih_snapshot_date'], NIH_DATE_TIME_PATTERN):
            raise KeyError

        # Else normally read dataset
        print('normal')
        full_df = pandas.read_csv(NIH_DATASET_SAVE_NAME)
    except KeyError:
        # Download and save data and snapshot date
        print('update')
        full_df = pandas.read_csv('https://storage.googleapis.com/kaggle-data-sets/5839/18613/compressed/Data_Entry_2017.csv.zip?X-Goog-Algorithm=GOOG4-RSA-SHA256&X-Goog-Credential=gcp-kaggle-com%40kaggle-161607.iam.gserviceaccount.com%2F20221218%2Fauto%2Fstorage%2Fgoog4_request&X-Goog-Date=20221218T023553Z&X-Goog-Expires=259200&X-Goog-SignedHeaders=host&X-Goog-Signature=21ac1efae4e74516a0cb3b0ed18fbc85ed7d815a8639636d9bee50d1055317f0dd07e4820a72237ae7e7ac3915d9ce2bfeab8122ccac8d90cd89dd1435624918a3a4768f7f26eeab191a988af1a377dc85b1258ce95046e68c485c6566b94efa16ba7d29fb1dbbfa664577f717224126026c18610cf57c1732d1295cf58ea54c9155ccdd2174a073fc369779d4ceaddbfb6537c9029c233d3c545832b8278e8cca0c86520c0911fceccb36c4b89a4e1ea4d11c7798845eaefd0094175862eaa7a85f27c504473814b4076e2d2b321cd22efe7a32b027280bbae1eaa969d7b3379cfc2cd15a805ee3d3dd8ee20b843e5aa73e60ff2a27e96dcb27054417b5f0d1', encoding_errors='replace')
        full_df.to_csv(NIH_DATASET_SAVE_NAME, index=False)
        snapshots['nih_snapshot_date'] = datetime.today().strftime(NIH_DATE_TIME_PATTERN)
        with open('data/snapshots.json', 'w') as write_file:
            json.dump(snapshots, write_file)

    return full_df

full_df = load_nih_data()
print(full_df.head(50))
print(full_df.shape)