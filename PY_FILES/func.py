import pandas as pd
import requests
import atexit





def info_init():
    url = "https://trying-20541-default-rtdb.firebaseio.com/Main_info.json"
    response = requests.get(url)
    data = response.json()['main_init']
    print(data)
info_init()

def saving_files(data,path):
    df = pd.DataFrame(data)
    print(df.to_string())

    try:
        df2 = pd.read_csv(path)
        all_df = pd.concat([df2, df], ignore_index=True)
        all_df.to_csv(path, index=False)
        print(' ------------------------------------ ALL FILES SAVED  ------------------------------------- \n \n')

    except:
        df.to_csv(path, index=False)
        print('============================= SECOND FILE SAVED ==========================')


atexit.register(info_init)


