from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import random
import json
import nltk
nltk.download('stopwords')


# 加载英文停用词词表
stop_words=stopwords.words('english')
for w in ['!',',','.','?','-s','-ly','</s>','s']:
    stop_words.append(w)

# 加载数据路径
path = '/home/tzl/Projects/Competition/data/kg/tkbc_processed_data'
file_name = 'rel_id'

#近义词随机替换。这里传入的words是一个列表, eg:"hello world".split(" ") or ["hello","world"]
def synonym_replacement(words, n):
    new_words = words.copy()
    random_word_list = list(set([word for word in words if word not in stop_words]))     
    random.shuffle(random_word_list)
    num_replaced = 0  
    for random_word in random_word_list:          
        synonyms = get_synonyms(random_word)
        if len(synonyms) >= 1:
            synonym = random.choice(synonyms)   
            new_words = [synonym if word == random_word else word for word in new_words]   
            num_replaced += 1
        if num_replaced >= n: 
            break

    sentence = ' '.join(new_words)
    new_words = sentence.split(' ')

    return " ".join(new_words)

#获取同义词
def get_synonyms(word):
    nearbyWordSet=wn.synsets(word)
    if len(nearbyWordSet)==0:
        return word
    else:
        return nearbyWordSet[0].lemma_names()


# 随机删除
def random_deletion(words, p):
    if len(words) == 1:
        return words[0]

    new_words = []
    for word in words:
        r = random.uniform(0, 1)
        if r > p:
            new_words.append(word)

    if len(new_words) == 0:
        rand_int = random.randint(0, len(words)-1)
        return words[rand_int]

    return " ".join(new_words)

# 随机插入
def random_insertion(words, n):
    new_words = words.copy()
    for _ in range(n):
        add_word(new_words)
    return " ".join(new_words)
#插入单词，这里插入随机挑选的单词的同义词
def add_word(new_words):
    synonyms = []
    counter = 0    
    while len(synonyms) < 1:
        random_word = new_words[random.randint(0, len(new_words)-1)]
        synonyms = get_synonyms(random_word)
        counter += 1
        if counter >= 10:
            return
    random_synonym = random.choice(synonyms)
    random_idx = random.randint(0, len(new_words)-1)
    new_words.insert(random_idx, random_synonym)

# key: relation_id    value: {raw_data:str, processed_data:list[str]}
data_processed = {}

with open(path + "/" + file_name, "r", encoding='utf-8') as file:
    lines = file.readlines()
    for id, line in enumerate(lines):
        processed = []
        interdict = {}
        sentence = line.strip().split('\t')[0]
        interdict['raw_data'] = sentence
        interdict['processed_data'] = [sentence]
        # 近义词随机替换
        for k in range(3):
            interdict['processed_data'].append(synonym_replacement(sentence.replace(',',"").split(" "), len(sentence.split(" "))//3))

        # 随机插入
        for k in range(3):
            interdict['processed_data'].append(random_insertion(sentence.replace(',',"").split(" "), len(sentence.split(" "))//3))

        # 随机删除
        for k in range(10):
            interdict['processed_data'].append(random_deletion(sentence.replace(',',"").split(" "), 0.25))   # 概率值

        '''
        s = set()
        for item in interdict['processed_data']:
            print(item)
        interdict['processed_data'] = list(s)
        '''
        interdict['processed_data'] = list(set(interdict['processed_data']))
        
        data_processed[id] = interdict

data_processed = json.dumps(data_processed, ensure_ascii=False, indent=4)
with open("/home/tzl/Projects/Competition/data_new/" + file_name + ".json", 'w', encoding='utf-8') as f:
    f.write(data_processed)
