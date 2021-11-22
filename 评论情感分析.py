from snownlp import SnowNLP
import os
filename = os.listdir(r'C:\Users\GJF\Desktop\社会实践\数据处理\评论\情感分析\每日评论（3.26-5.31）')
for i in filename:
    if 'txt' in i:
        with open(f'{i}','r',encoding='utf-8') as f:
            txt = f.readlines()
        value=[]
        for t in txt:
            t = t.strip()
            if t != '':
                s=SnowNLP(t)
                value.append(s.sentiments)
        a=0
        for t in value:
            a=a+t
        print('%.5f'%(a/len(value)))
print(filename)
