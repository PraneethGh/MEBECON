import pandas as pd
import numpy as np
import random
from tqdm import tqdm
from gensim.models import Word2Vec 
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
from nltk.corpus import wordnet
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.util import ngrams
from sklearn.feature_extraction.text import CountVectorizer
from collections import defaultdict
from collections import  Counter
nltk.download('stopwords')
nltk.download('punkt')
stop=set(stopwords.words('english'))
import re
from nltk.tokenize import word_tokenize
import gensim
import string
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import pickle

df=pd.read_csv('D:/FallSem_21-22/NLP - CSE4022/ndis_pred_2.csv')
df.head()

from sklearn import preprocessing
label_encoder = preprocessing.LabelEncoder()
print(df['disease'].unique())
# Encode labels in column 'disease'.
df['disease']= label_encoder.fit_transform(df['disease'])
X,Y=df['symptoms'],df['disease']
#df['disease']
type(X)

#Function definitions
dc={}
def clean(s): #Function to remove clean
    s=s.replace(" ","")
    s=s.strip()
    s=s.lower()
    if(s[len(s)-1]==','):
        s=s[:len(s)-1]
    for i in  s.split(","):
        dc[i]=0
    return s
def tknz(l):
    '''ans=[]
    for i in l:
        if(i!=" "):
            dc[i]+=1
            if(dc[i]==1):
               ans.append(nltk.word_tokenize(i))'''
    ans=nltk.word_tokenize(l)
    fans=[]
    for i in ans:
        if len(i)>=2:
            fans.append(i)
    return fans
def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}

    return tag_dict.get(tag, wordnet.NOUN)
def lmtz(word):
    lemmatizer=WordNetLemmatizer()
    return lemmatizer.lemmatize(word,get_wordnet_pos(word))
    
#Cleaning the data
#1. Removing the whitespaces and converting them to lower case and stripping them
for i in range(len(X)):
    X[i]=clean(X[i])
# print(X)

#2. Tokenizing each sentence
records=[]
for i in X:
    #print(type(X[i]))
    #rwords=i.split(",")
    #print(rwords)
    records.append(' '.join(tknz(i)))
#temp=tokens[0].split()
#print(temp)
print(records)

#3. Lemmatization of each word
symptoms=[]
i=0
for record in records:
    s=""
    for word in record.split(" "):
        s+=lmtz(word)+" "
    symptoms.append(s[:len(s)-1])
    #print(s)
print(symptoms)


df.isnull().sum()
X_train, X_test, y_train, y_test = train_test_split(symptoms, Y, test_size=0.20, random_state=42)

from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english')
features_train = vectorizer.fit_transform(X_train).toarray()
features_test = vectorizer.transform(X_test).toarray()
print(features_train)

from sklearn.naive_bayes import GaussianNB
from time import time
t0 = time()
model = GaussianNB()
model.fit(features_train, y_train)
print(f"\nTraining time: {round(time()-t0, 3)}s")
t0 = time()
score_train = model.score(features_train, y_train)
print(f"Prediction time (train): {round(time()-t0, 3)}s")
t0 = time()
score_test = model.score(features_test, y_test)
print(f"Prediction time (test): {round(time()-t0, 3)}s")
print("\nTrain set score:", score_train)
print("Test set score:", score_test)

pred_values=model.predict(features_test)
from sklearn.metrics import classification_report
classification_report(pred_values,y_test)

sample=["vomiting headache"]
sample=vectorizer.transform(sample)
print(label_encoder.inverse_transform(model.predict(sample.toarray())))

pickle.dump([model,vectorizer,label_encoder], open('model2.pkl','wb'))