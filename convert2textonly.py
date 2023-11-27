import json

data = []
with open(r'raw_doc\VLSP\2021\train.json',encoding='utf8') as f:
    data1 = json.loads(f.read())
    words,ner_tags = data1['words'],data1['ner_tags']
for ix in words.keys():
    data.append(' '.join(words[ix]))
with open(r'documents\vlsp\train.text','w',encoding='utf8') as f:
    for item in data:
        f.write(item)
        f.write('\n')


# data = []
# with open(r'raw_doc\Covid19\train_syllable.json',encoding='utf8') as f:
#     for line in f:
#         data.append(" ".join(json.loads(line)['words']))

# with open(r'documents\covid\train_syllable.text','w',encoding='utf8') as f:
#     for item in data:
#         f.write(item)
#         f.write('\n')


# input_file = open (r'raw_doc\ViMQ\train.json',encoding='utf8')
# json_array = json.load(input_file)
# store_list = []

# for item in json_array:
#     store_details = item['sentence'].replace("_"," ")
#     store_list.append(store_details)

# with open(r'documents\vimq\train.text','w',encoding='utf8') as f:
#     for item in store_list:
#         f.write(item)
#         f.write('\n')

# input_file = open (r'raw_doc\ViMQ\train.json',encoding='utf8')
# json_array = json.load(input_file)
# store_list = []

# for item in json_array:
#     store_details = item['sentence'].replace("_"," ")
#     store_list.append(store_details)

# with open(r'documents\vimq\train.text','w',encoding='utf8') as f:
#     for item in store_list:
#         f.write(item)
#         f.write('\n')