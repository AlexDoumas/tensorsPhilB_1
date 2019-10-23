

# imports. 
import csv
import numpy as np
import pdb

# import ratings.
data1 = csv.reader(open('All_logfiles.csv'))
mydata = []
for row in data1:
	mydata.append(row)
# pop the 0th item as it is column information.
mydata.pop(0)

# initialise dictionary of rating responses. 
resp_dict = {}
# each element in mydata is a response to a single word pair. 
# index 8 is word 1, index 9 is word 2, and index 10 is rating. 
# for each respose, check if a resp_dict key exists as frozenset((['word1', 'word2'])); if yes, add the response to the array for that key, if not, create an entry with that key and a list of ratings with the current rating as the first entry as the entry for that key.
for resp in mydata:
    if frozenset([resp[8], resp[9]]) in resp_dict:
        resp_dict[frozenset([resp[8], resp[9]])].append(resp[10])
    else:
        resp_dict[frozenset([resp[8], resp[9]])] = [resp[10]]

# import main data set. 
data2 = csv.reader(open('AllData768CleanResorted.csv'))
mydata = []
for row in data2:
	mydata.append(row)

# for each entry of the data, find the human similarity ratings of the two predicates and the two nouns and add them to the data set. 
for resp in mydata[1:]:
    Phrase1 = resp[5].split(' ')
    Phrase2 = resp[6].split(' ')
    # if it's a predicate first trial, then the 1th item of the Phrase array will the the predicate. Otherwise, it'll be the 2th item of the Phrase array. 
    if resp[3] == 'A':
        # pred first, object second. 
        pred1 = Phrase1[1]
        pred2 = Phrase2[1]
        noun1 = Phrase1[2]
        noun2 = Phrase2[2]
    else:
        # pred second, object first. 
        pred1 = Phrase1[2]
        pred2 = Phrase2[2]
        noun1 = Phrase1[1]
        noun2 = Phrase2[1]
    # find pred and noun similarities.
    try:
        pred_sim = np.mean(list(map(int, resp_dict[frozenset([pred1, pred2])])))
    except:
        pred_sim = np.mean(list(map(int, resp_dict[frozenset(['wijst af'])])))
    noun_sim = np.mean(list(map(int, resp_dict[frozenset([noun1,noun2])])))
    # add pred and noun similarities to resp. 
    resp.extend([pred_sim, noun_sim, pred1, pred2, noun1, noun2])

f = open('tensor_data.csv', 'w')
for out_item in mydata:
	for item in out_item:
		f.write(str(item) + ' , ')
	f.write('\n')





