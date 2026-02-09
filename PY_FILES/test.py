











item_url = ['https://pahe.win/FKFMA', 'https://pahe.win/QAKuM', 'https://pahe.win/XXVti', 'https://pahe.win/gXqif', 'https://pahe.win/lMtqb', 'https://pahe.win/PuWfe']
item_text = ['MTBB · 360p (42MB) BD', 'MTBB · 720p (95MB) BD', 'MTBB · 1080p (178MB) BD', 'MTBB · 360p (41MB) BD eng', 'MTBB · 720p (92MB) BD eng', 'MTBB · 1080p (174MB) BD eng']




DQ = 0
CAT = 'SUB' #SELECT SUB [ENGLISH SUB] AND DUB [ENGLISH DUB]
QT = '720'  # SELECT QUALITY 480, 720, 1080

CAT_QT = [x for x in item_text if QT in x]

if CAT_QT:
    DQ1 = CAT_QT[0]
    DQ = item_text.index(DQ1)
else:
    print('\n DIDNT SELECT THE RIGHT QUALITY [360,720,1080] \n DEFAULTING TO QUALITY [360P] ')

print('DQ>>>>>', DQ)
print(item_url[DQ])

# page.goto(item_url[DQ], timeout=60000)