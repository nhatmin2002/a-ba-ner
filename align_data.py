import pandas as pd


with open(r'documents\covid\train_syllable.text','r',encoding='utf8') as f:
    lines = f.readlines()
    lines = list(map(lambda x:x.strip(),lines))

df = pd.DataFrame(lst)