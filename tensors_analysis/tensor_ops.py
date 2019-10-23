

# imports. 
import csv
import spacy
import numpy as np
from scipy import spatial
import pdb

# import data.
data1 = csv.reader(open('tensor_data.csv'))
mydata = []
for row in data1:
	mydata.append(row)
# pop the 0th item as it is column information.

# load dutch w2v.
nlp = spacy.load("nl_core_news_sm")

# for each word pair, create the additive binding, and the tensor binding, then compute the similarity of the two bindings. 
for resp in mydata[1:]:
    pred1_emb = nlp(resp[18])
    pred2_emb = nlp(resp[19])
    noun1_emb = nlp(resp[20])
    noun2_emb = nlp(resp[21])
    add_bind1 = pred1_emb.vector + noun1_emb.vector
    add_bind2 = pred2_emb.vector + noun2_emb.vector
    tensor_bind1 = np.tensordot(pred1_emb.vector, noun1_emb.vector, axes=0)
    tensor_bind2 = np.tensordot(pred2_emb.vector, noun2_emb.vector, axes=0)
    add_sim = 1 - spatial.distance.cosine(add_bind1, add_bind2)
    tens_sim = 1 - spatial.distance.cosine(tensor_bind1.flatten(), tensor_bind2.flatten())
    async_sim = ((1 - spatial.distance.cosine(pred1_emb.vector, pred2_emb.vector))+(1 - spatial.distance.cosine(noun1_emb.vector, noun2_emb.vector)))/2.0
    resp.extend([add_sim, tens_sim, async_sim])
    
f = open('tensor_data3.csv', 'w')
for out_item in mydata:
	for item in out_item:
		f.write(str(item) + ' , ')
	f.write('\n')










