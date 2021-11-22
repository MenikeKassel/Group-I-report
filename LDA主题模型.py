from gensim import corpora, models
import jieba.posseg as jp
words_list = []
with open('E:\\program\\爬虫\\分类爬取\\文本\\新闻分类\\2017.txt','r',encoding = 'utf-8') as f:
    txt = f.readlines()
txt2 = [a.strip() for a in txt]#生成语句列表
with open('cn_stopwords.txt','r',encoding= 'utf-8') as f:
    stop = f.readlines()
stop1 = [a.strip() for a in stop]#生成停用词列表
for text in txt2:
    words = [w.word for w in jp.cut(text) if len(w.word) > 1 and w.word not in stop1]#进行分词和语料清洗
    words_list.append(words)#添加到词列表
dictionary = corpora.Dictionary(words_list) #给不同的词赋予一个唯一的id，存为字典类型如：{‘词语’：id}......
corpus = [dictionary.doc2bow(words) for words in words_list]
#把文档列表words_list变成一个稀疏向量[（词对应的id,词出现的次数），（2，1）...]，次数为0的词不显示
for i in range(5,6):
    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=i)#进行运算，生成i个主题
    #lda.save(f'E:\\program\\LDA主题模型\\模型计算\\模型\\topic{i}.model')#将模型保存至本地
    print(f'{i}个主题')
    for x in lda.print_topics(num_words=5):#结果输出
        print(x)
#print(lda.inference(corpus))
