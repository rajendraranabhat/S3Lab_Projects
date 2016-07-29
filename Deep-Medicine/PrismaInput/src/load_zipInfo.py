#Swati Tezcan Version
import pandas as pd

def get_provider_map():
    print 'lala'
    read_var = ['Account','Attend_Doc']
    df = pd.read_csv('ip.csv', usecols=read_var)
    AccountId = []
    ProviderId = []
    for index, row in df.iterrows():
         AccountId.append(row['Account'])
         ProviderId.append(row['Attend_Doc'])
    dictionary = dict(zip(AccountId, ProviderId))
    return dictionary 