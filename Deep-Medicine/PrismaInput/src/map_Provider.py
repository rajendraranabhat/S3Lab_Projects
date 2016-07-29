#Swati Tezcan Version

import pandas as pd


def get_provider_map(path):

    read_var = ['acc','attend_doc']
    df = pd.read_csv(path+'provider_info.csv', usecols=read_var)
    AccountId = []
    ProviderId = []
    for index, row in df.iterrows():
         AccountId.append(row['acc'])
         ProviderId.append(row['attend_doc'])
    dictionary = dict(zip(AccountId, ProviderId))
    return dictionary