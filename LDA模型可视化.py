from gensim import corpora, models
import jieba.posseg as jp
import pyLDAvis.gensim_models
words_list = []
with open('E:\\program\\爬虫\\分类爬取\\文本\\新闻分类\\2017.txt', 'r', encoding='utf-8') as f:
    txt = f.readlines()
txt2 = [a.strip() for a in txt]
with open('cn_stopwords.txt', 'r', encoding='utf-8') as f:
    stop = f.readlines()
stop1 = [a.strip() for a in stop]
for text in txt2:
    words = [w.word for w in jp.cut(text) if len(w.word) > 1 and w.word not in stop1]
    words_list.append(words)
dictionary = corpora.Dictionary(words_list)
corpus = [dictionary.doc2bow(words) for words in words_list]
lda0 = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=7) #更改主题数（num_topics=x）
plot = pyLDAvis.gensim_models.prepare(lda0, corpus, dictionary)#导入模型、字典、稀疏向量进行可视化处理
pyLDAvis.save_html(plot, 'E:\\program\\爬虫\\分类爬取\\文本\\新闻分类\\模型可视化\\2017\\7主题模型.html')# 保存到本地html
