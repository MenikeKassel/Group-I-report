from snownlp import sentiment
sentiment.train('neg.txt','pos.txt')
sentiment.save('new model')
print('训练完成')
