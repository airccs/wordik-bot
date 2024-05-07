NewWord = list()

with open('1000 слов.txt', 'r',  encoding='utf-8') as f:
    for str in f:
        NewWord.append([str[:str.find('—')-1],str[str.find('—')+2:]])
