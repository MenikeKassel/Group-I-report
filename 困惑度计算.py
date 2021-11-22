from gensim import corpora, models
from gensim.models import CoherenceModel
import jieba.posseg as jp
import math
words_list = []
with open('E:\\program\\爬虫\\分类爬取\\文本\\新闻分类\\2010.txt','r',encoding = 'utf-8') as f:
    txt = f.readlines()
txt2 = [a.strip() for a in txt]
with open('cn_stopwords.txt','r',encoding= 'utf-8') as f:
    stop = f.readlines()
stop1 = [a.strip() for a in stop]
for text in txt2:
    words = [w.word for w in jp.cut(text) if len(w.word) > 1 and w.word not in stop1]
    words_list.append(words)
dictionary = corpora.Dictionary(words_list)
corpus = [dictionary.doc2bow(words) for words in words_list]
for i in range(1,11):
    lda0 = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=i)#LDA模型生成
    Lperplexity = lda0.log_perplexity(corpus)#计算log_perplexity参数
    perplexity = math.exp(-Lperplexity)#根据log_perplexity参数计算困惑度
    cv_tmp = CoherenceModel(model=lda0, texts=words_list, dictionary=dictionary, coherence='u_mass')#计算模型的一致性
    print(perplexity,cv_tmp.get_coherence())

