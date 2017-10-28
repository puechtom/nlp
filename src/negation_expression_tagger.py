from nltk import *
import json
from bs4 import BeautifulSoup
import re
import random
import string
import time
import pprint

# negationExpressionPattern = [(r"(?:[^.?!:\r\n]*(?:No|Not|Neither|Never|No one|Nobody|None|Nor|Nothing|Nowhere)\b[^.?!:]*(?:\.|\?|!|:))|(?:[^.?!:\r\n]*\b(?:no|not|neither|never|no one|nobody|none|nor|nothing|nowhere)\b[^.?!:]*(?:\.|\?|!|:))|(?:[^.?!:\r\n]*(?:n(?:'|’)t|less)\b[^.?!:]*(?:\.|\?|!|:))|(?:[^.?!:\r\n]*\b(?:few|hardly|little|rarely|scarcely|seldom)\b[^.?!:]*(?:\.|\?|!|:))|(?:[^.?!:\r\n]*\b(?:de|dis|un)[^.?!:]*(?:\.|\?|!|:))",'NEGATION')]
# negationExpressionPattern = [(r"(?:[^.?!:\r\n]*(?:No|Not|Neither|Never|No one|Nobody|None|Nor|Nothing|Nowhere)\b[^.?!:]*(?:\.|\?|!|:))|(?:[^.?!:\r\n]*\b(?:no|not|neither|never|no one|nobody|none|nor|nothing|nowhere)\b[^.?!:]*(?:\.|\?|!|:))|(?:[^.?!:\r\n]*(?:n(?:'|’)t|less)\b[^.?!:]*(?:\.|\?|!|:))|(?:[^.?!:\r\n]*\b(?:few|hardly|little|rarely|scarcely|seldom)\b[^.?!:]*(?:\.|\?|!|:))",'NEGATION')]
negationExpressionPattern = [(r"(?:[^.?!:\r\n]*(?:No|Not|Neither|Never|No one|Nobody|None|Nor|Nothing|Nowhere)\b[^.?!:]*(?:\.|\?|!|:))|(?:[^.?!:\r\n]*\b(?:no|not|neither|never|no one|nobody|none|nor|nothing|nowhere)\b[^.?!:]*(?:\.|\?|!|:))|(?:[^.?!:\r\n]*(?:n(?:'|’)t)\b[^.?!:]*(?:\.|\?|!|:))|(?:[^.?!:\r\n]*\b(?:few|hardly|little|rarely|scarcely|seldom)\b[^.?!:]*(?:\.|\?|!|:))",'NEGATION')]

negationTagger = RegexpTagger(negationExpressionPattern)

with open('dirty_result.json', encoding = 'utf-8', mode='r') as f:
    try:
        dataset = json.load(f)
        for i in range(len(dataset)):
            dataset[i]['question'] = BeautifulSoup(dataset[i]['question'], 'html.parser').get_text()
            for j in range(len(dataset[i]['answers'])):
                dataset[i]['answers'][j] = BeautifulSoup(dataset[i]['answers'][j], 'html.parser').get_text()

    except Exception as e:
        print(e)

# pprint.pprint(dataset)
# exit(0)

stop_words = corpus.stopwords.words("english")
contractions = ["n't", "'s", "s'", "'d", "'ll" , "'ve", "'re", "'m"] + [x for x in string.punctuation] + [ x for x in '0123456789']
mydict = [x.lower() for x in corpus.words.words()]
ps = stem.PorterStemmer()
lmtzr = stem.wordnet.WordNetLemmatizer()

mywords = []
negations = []
newdataset = dataset
i = 0
for i in range(len(dataset)):
##    print(i)
    sentences = sent_tokenize(dataset[i]['question'])
    for k in range(len(sentences)):
        tokens = regexp_tokenize(sentences[k], negationExpressionPattern[0][0])
        for l in range(len(tokens)):
            negations.append(tokens[l].lower())
            newdataset[i]['question'] = dataset[i]['question'].replace(tokens[l],'')
            # print("dataset[i]['question']", dataset[i]['question'])
            # print("newdataset[i]['question']", newdataset[i]['question'])
    for j in range(len(dataset[i]['answers'])):
        sentences = sent_tokenize(dataset[i]['answers'][j])
        for k in range(len(sentences)):
            tokens = regexp_tokenize(sentences[k], negationExpressionPattern[0][0])
            # print(tokens)
            for l in range(len(tokens)):
                negations.append(tokens[l].lower())
                # print("i:", i)
                # print("j:", j)
                # print("l:", l)
                # print("newdataset:", len(newdataset))
                # print("newdataset[i]['answers']:", len(newdataset[i]['answers']))
                # print("dataset[i]['question']:", len(dataset[i]['question']))
                newdataset[i]['answers'][j] = dataset[i]['answers'][j].replace(tokens[l],'')

sentences = []
for post in newdataset:
    for sent in sent_tokenize(post['question']):
        sentences.append(sent)
        for token in word_tokenize(sent.lower()):
            if len(token) > 1 and token.lower() not in stop_words and token not in contractions and not re.search("^[\W\d]+$", token):
                mywords.append(token.lower())
    for texts in post['answers']:
        for sent in sent_tokenize(texts):
            sentences.append(sent.lower())
            for token in word_tokenize(sent):
                if len(token) > 1 and token.lower() not in stop_words and token not in contractions and not re.search("^[\W\d]+$", token):
                    mywords.append(token.lower())

textDist = FreqDist(negations+mywords)

##for i in sorted(set(comments)):
##    print(i)
##    print('========')

print("\n Top 20 words")
for i in textDist.most_common(20):
    print(i)

# print("Negations:", negations)
# pprint.pprint(negations)


# irregularWords = []

# ##print(len(mywords))
# start = time.time()
# for token in mywords:
#     lemmaed_token = lmtzr.lemmatize(token.lower())
#     stemmed_token = ps.stem(token.lower())
#     lemmaedV_token = lmtzr.lemmatize(token.lower(), 'v')
# ##    print('next token')
#     if token.lower() not in stop_words and lemmaed_token not in mydict and lemmaedV_token not in mydict and stemmed_token not in mydict:
#         irregularWords.append(token.lower())
# print('time taken to check for irregulars: %f' %(time.time()-start))

# irregularWordsDist = FreqDist(irregularWords)
# print("\n Top 20 irregular words")
# top20irregulars = []
# with open('top_20_irregulars.txt', encoding="utf-8",mode='w') as f:
#     for irregularWord in irregularWordsDist.most_common(20):
#         print(irregularWord)
#         f.write('\n%s\n' %'#######################################')
#         f.write('irregular word: %s\n' %str(irregularWord))
#         f.write('%s\n' %'showing all unique tokens')
#         f.write("\n")
#         for word in irregularWords:
#             if irregularWord[0] in word and word not in top20irregulars:
#                 for i in range(len(irregularWord[0])):
#                     if irregularWord[0][i] != word[i]:
#                         break
#                     elif i == len(irregularWord[0][i])-1:
#                         top20irregulars.append(word)
#                         f.write("%s\n" % word)
#     f.write('%s\n' %'#######################################')

# irregularWordSentences = []
# for sent in sentences:
#     for word in irregularWords:
#         if word in sent and sent not in irregularWordSentences:
#             irregularWordSentences.append(sent)
# with open('random_10_POStags_with_irregulars.txt', encoding="utf-8",mode='w') as f:
#     for i in range(10):
#         f.write('\n%s\n' %'#######################################')
#         r = random.random()*len(irregularWordSentences)
#         if len(irregularWordSentences[int(r)])<2:
#             r = random.random()*len(irregularWordSentences)
#         for w in pos_tag(word_tokenize(irregularWordSentences[int(r)])):
#             f.write("%s\n" % str(w))
#     f.write('%s\n' %'#######################################')
