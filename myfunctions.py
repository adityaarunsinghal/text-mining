
# coding: utf-8

# In[1]:


import pandas as pd
from zipfile import ZipFile
import os
import re
import json
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import wordcloud
from sklearn.preprocessing import OneHotEncoder
import matplotlib.animation as animation
import nltk
from nltk.corpus import wordnet
nltk.download('wordnet')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
sns.set()


# In[2]:


datadf = pd.read_csv(r'All Data/Raw Journey Data/Until16May2020(all jsons to csv).csv')
datadf = datadf.set_index('id')


# In[3]:


test = "Brigadier Suraj singh\n\nMy name is brigadier suraj singh. Presiding officer of this general court martial! Have you ever confronted death ? (takes a pull at his smoke pipe)\nI guess not! I HAVE faced death a lot of times..\nThere in the battlefield..and here in the rooms of court martial too.\nThose few seconds when you stand in front of the devil himself..and he sets your blood on fireee and then turns it as cold as ice! (gives a haughty laugh)\nYour heart beats like a drum(strikes his chest in lubb dub sound) while your limbs go numb.\nYou can see this fear and agony in the eyes of the victim..\nBut you can also see it in the eyes of the killer.\nWhen the soldier raises his sword and brings it down on the enemys throat...\nYou'll can never have the thrill of such near death experiences!\nThis warfare has been flowing in the veins of my family since ages. All my forefathers have been warriors. \nI've heard their stories from my grandmother. And those stories are now a part of by subconscious.\nI dream of my ancestors carrying blazing swords in  their hands and riding dark horses leading great armies to war.\n\n The riders of death !! \n\nMaybe those stories were the reason i had this affinity towards the battlefield.\nThey used to call me GRENADE SINGH! i used to carry a garland of grenades round my neck and plucked those deathly devices and hurled them at masses of the nemesis.\nOhhhhhhh the fear in their eyes.. It makes me drunk! It is such a heavenly pleasure to send someone to hell. \nBut yes..there was a time..just once .when i was at the mercy of someone else. Once!! When my arms refused to lift my saber. Once! When i felt my legs quivering under the weight of someone elses sword.\nAt that moment all the stories my grandmother told me fell false. Just that once. It was my father.\nI have been finding him ever since trying to avenge that humiliation. That experience was something you wouldnt like to have . You common folks. Typical coca cola products.\nAnyways (gives a disgusted look) so let the court martial advance! \n\n\nBrigadier Suraj singh\n\nMera naam brigadier suraj singh hai... Presiding officer of this general training program! \nDo you know what fear is? Saccha darr kya hota hai? Darr ek dhadakte angaare ke tarah hota hai jo uske saamne aane waali harr cheez ko jala deta hai..\nHave you ever confronted death ?\nI guess not! I HAVE faced death a lot of times..\nThere on the battlefield..and in the rooms of court martial as well..\nThose few seconds when you stand in front of the devil himself , wo chand pal...when he sets your blood on fireee and then turns it as cold as ice! \n\nYour heart beats like a drum while your limbs go numb.\nYou can see this fear and agony in the eyes of the victim..\nBut you can also see it in the eyes of the killer.\nWhen the soldier raises his sword and brings it down on the enemys throat...\nAaaaahchick..\nAap log abhi naye ho..you all are still Typical coca cola products. \n\nMy dear friends.. Just like everyone else.. I have had a fear that keeps eating into my consciousness. \nThe fear of rejection!! Being a dramatist.. Just like every other artist.. I think agar logo ko pasand nahi aaya toh kya hoga? But now i have decided to let it rip. I will stand there-look it in its eyes and reject this fear of rejection. \n\n\nAaj se humhaara safar shuru hoga.. \nAre u ready? Am i going to hear you roarrr?? \n so let the training begin!! "


# In[4]:


test


# In[5]:


def no_punc (text):
    text = re.sub('<.*?>', '', text)
    text = re.sub('[^\w\s]', '', text)
    text = re.sub('\\n', '', text)
    text = re.sub('nbsp', '', text)
    text = re.sub('\s+', ' ', text).strip()
    return (text)


# In[6]:


stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]


# In[7]:


personal_stopwords = ["i've", "i'm","i'll", "like", "i'd", "he's", "she's", "he'd", "she'd"]

stopwords.extend(personal_stopwords)


# In[8]:


stopwords = list(map(lambda x: re.sub('\'','',x), stopwords))


# In[9]:


def no_stop (text):
    new_text = []
    for x in text.split():
        if x.lower() not in stopwords:
            new_text.append(x)
    return ' '.join(new_text)
        


# In[10]:


contractions = { 
"ain't": "am not",
"aren't": "are not",
"can't": "cannot",
"could've": "could have",
"couldn't": "could not",
"couldn't've": "could not have",
"didn't": "did not",
"doesn't": "does not",
"don't": "do not",
"hadn't": "had not",
"hasn't": "has not",
"haven't": "have not",
"he'd": "he would",
"he'll": "he will",
"he's": "he is",
"how'd": "how did",
"how'll": "how will",
"how's": "how is",
"hows": "how is",   
"I'd": "I would",
"I'll": "I will",
"I'm": "I am",
"I've": "I have",
"isn't": "is not",
"it'd": "it would",
"it'll": "it shall / it will",
"it's": "it is",
"let's": "let us",
"ma'am": "madam",
"might've": "might have",
"mightn't": "might not",
"mightn't've": "might not have",
"must've": "must have",
"mustn't": "must not",
"mustn't've": "must not have",
"needn't": "need not",
"needn't've": "need not have",
"o'clock": "of the clock",
"oughtn't": "ought not",
"oughtn't've": "ought not have",
"shan't": "shall not",
"sha'n't": "shall not",
"shan't've": "shall not have",
"she'd": "she would",
"she'd've": "she would have",
"she'll": "she will",
"she'll've": "she will have",
"she's": "she is",
"should've": "should have",
"shouldn't": "should not",
"shouldn't've": "should not have",
"so've": "so have",
"that'd": "that would",
"that'd've": "that would have",
"that's": "that is",
"there'd": "there would",
"there'd've": "there would have",
"there's": "there is",
"they'd": "they would",
"they'd've": "they would have",
"they'll": "they will",
"they'll've": "they will have",
"they're": "they are",
"they've": "they have",
"to've": "to have",
"wasn't": "was not",
"we'd": "we would",
"we'd've": "we would have",
"we'll": "we will",
"we'll've": "we will have",
"we're": "we are",
"we've": "we have",
"weren't": "were not",
"what'll": "what will",
"what're": "what are",
"what's": "what is",
"what've": "what have",
"when's": "when is",
"when've": "when have",
"where'd": "where did",
"where's": "where is",
"where've": "where have",
"who'll": "who will",
"who's": "who is",
"who've": "who have",
"why's": "why is",
"why've": "why have",
"will've": "will have",
"won't": "will not",
"won't've": "will not have",
"would've": "would have",
"wouldn't": "would not",
"wouldn't've": "would not have",
"y'all": "you all",
"y'all'd": "you all would",
"y'all'd've": "you all would have",
"y'all're": "you all are",
"y'all've": "you all have",
"you'd": "you would",
"you'd've": "you would have",
"you'll": "you will",
"you're": "you are",
"you've": "you have"
}


# In[16]:


def cleaner (test):
    test = re.sub('\\n', ' ', test)
    test = re.sub('<.*?>', ' ', test)
    test = re.sub('&nbsp;', ' ', test)
    test = re.sub('&[a-z]+;', '', test)
    test = re.sub('\.{2,}', ' ... ', test)
    test = re.sub('!{2,}', ' ! ', test)
    test = re.sub('\?{2,}', ' ? ', test)
    test = re.sub("’", "'", test)
    test = re.sub(" ' ", "'", test)
    test = re.sub("([^A-Za-z0-9'])", r" \1 ", test)
    test = re.sub('\s+', ' ', test)
    test = re.sub('\. \. \.', '...', test)

    test = re.sub(" i ", ' I ', test)
    test = re.sub(" u ", ' you ', test)
    test = re.sub("( im )|( Im )", " I'm ", test)
    test = re.sub(" ill ", " I'll ", test)
    test = re.sub("( ive )|( I ve )|( i ve )", " I've ", test)
    test = re.sub("( adi )|( Aditya )|( aditya )", " Adi ", test)

    uncontracted = []
    for x in test.split():
        if x.istitle():
            if x.lower() in contractions.keys():
                uncontracted.append(contractions[x.lower()].title())
            else:
                uncontracted.append(x)
        elif x.lower() in contractions.keys():
                uncontracted.append(contractions[x.lower()])
        elif x in contractions.keys():
                uncontracted.append(contractions[x])
        else:
            uncontracted.append(x)
        
        
    return(" ".join(uncontracted))


# In[17]:


from nltk.stem import WordNetLemmatizer as wnl
lemmatizer = wnl()


# In[18]:


def nltk_tag_to_wordnet_tag(nltk_tag):
    if nltk_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_tag.startswith('R'):
        return wordnet.ADV
    else:          
        return None

def lemmatize(sentence):
    #tokenize the sentence and find the POS tag for each token
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))  
    #tuple of (token, wordnet_tag)
    wordnet_tagged = map(lambda x: (x[0], nltk_tag_to_wordnet_tag(x[1])), nltk_tagged)
    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            #if there is no available tag, append the token as is
            lemmatized_sentence.append(word)
        else:        
            #else use the tag to lemmatize the token
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    return " ".join(lemmatized_sentence)


# In[21]:


# show('1586737092738-3fa9f1f5ffbc2dc0')


# In[19]:


# def show (ID):
#     print(datadf.text.loc[ID])
#     print('\n ------------------ \n')
#     print(datadf.cleaned_text.loc[ID])
#     return datadf.loc[ID].to_frame().T


# In[2]:


def binner(nbins, df):
    bin_size = round(len(df)/nbins)
    try:
        out = pd.cut(df.index, bins=nbins, include_lowest=False,labels=df.index[bin_size::bin_size].values) #binning
    except:
        out = pd.cut(df.index, bins=nbins, include_lowest=False,labels=df.index[::bin_size].values)
    df['bins']=out
    return (df)

