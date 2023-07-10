from nlpcda import Randomword, Ner, Similarword
from nlpcda import Simbert
import json

'''
config: model_path(上述下载的模型位置)\设备(cpu/cuda...)\最大长度、随机种子
sent: 需要增强的句子
create_num: 构造的句子数量
'''


path = '/home/tzl/Projects/Competition/data/kg/tkbc_processed_data'
file_name = 'rel_id.txt'

'''
with open(path + file_name, 'r', encoding='utf-8') as fp:
    print(type(fp))
    data = json.load(fp)
    print(type(data))
'''

config = {
        'model_path': '/home/tzl/Projects/Competition/chinese_simbert_L-12_H-768_A-12',
        'CUDA_VISIBLE_DEVICES': '0',
        'max_len': 32,
        'seed': 1
}


simbert = Simbert(config=config)
sent = 'Appeal for change in institutions, regime'
Similar_replace = Similarword(create_num=3, change_rate=1.0)
rsl = Similar_replace.replace(sent)

for s in rsl:
    print(s)


#synonyms = simbert.replace(sent=sent, create_num=5)
#print(synonyms)



