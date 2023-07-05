
#Meet Candy: your friend

#import necessary libraries

import csv #to read and write in csv files
import random # to generate a random response from the given variable 
import string # to process standard python strings
import warnings # to avoid warnings
# to compare the input text from the dataset
from sklearn.feature_extraction.text import TfidfVectorizer
#to provide frequency to the matched data 
from sklearn.metrics.pairwise import cosine_similarity
warnings.filterwarnings('ignore')

import datetime # to get date cuurent date and time of the system

# for sentimental analysis of the provided feedback 
from textblob import TextBlob

# libary containig tools to work with human language
import nltk
from nltk.stem import WordNetLemmatizer

#  nltk.download('popular', quiet=True) # for downloading packages
#  nltk.download('punkt')
#  nltk.download('wordnet') 

#date to string format
CDT = datetime.datetime.now()
cdt=CDT.strftime("%d-%b-%Y ,%H:%M:%S")

#Reading in the corpus
with open('cbot.txt','r', encoding='utf8', errors ='ignore') as fin:
    raw = fin.read().lower()
    

#TOkenisation
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words
#sent_tokens
counter=0


# Preprocessing
lemmer = WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


#To add chat history
def addchat(name,time,res):
    text=["\n",name,": [",time,"] :",res]
    with open('chathis.txt', mode='a') as hf:
        hf.writelines(text)
        hf.close()
# to add a marker before every chat
addchat("new chat history",cdt,"file opened")

# Keyword Matching

GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)


# Generating response

def response(user_response):
    robo_response=''
    sent_tokens.append(user_response)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"To get more information about us please contact  +91-120-3063371-73"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        return robo_response


flag=True
print("Candy: Hi I am Candy.\n Welcome to CDAC . How can I help you?.\n If you want to exit, type Bye!")
name=input("Enter name: ")
eid =input("Enter mail: ")
addchat("chat history data \n",cdt,name)

# algorthm working behind the program:
while(flag==True):
         
    user_response = input(name +":")
    user_response=user_response.lower()
    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' or user_response=='ty'):
            flag=False
            print("Candy: You are welcome..")
            addchat(name,cdt,user_response)
            addchat("Candy",cdt,"You are welcome..")
            counter=counter+1
            
        elif user_response in ["hw r u","how r u","how are u" "how are you","hw r u ?","how are you?","hw r u?",]:
            print(" Candy: i am fine thank you !")
        else:
            if(greeting(user_response)!=None):
                print("Candy: "+greeting(user_response))
                addchat(name,cdt,user_response)
                addchat("Candy",cdt,greeting(user_response))
                counter=counter+1
                
            else:
                print("Candy: ",end="")
                print(response(user_response))
                addchat(name,cdt,user_response)
                sent_tokens.remove(user_response)
                counter=counter+1
    else:
        feed=input("How was your exprience with me : ")
        blob=TextBlob(feed)
        addchat(name,cdt,user_response)
        if(blob.sentiment.polarity < 0):
            sug=input("what would you like to suggest: ")
            counter=counter+1
            
        else:
            print("thank you")
            sug=""
            counter=counter+1
            
        row =[name,eid,feed,sug,cdt]

        with open('feed.csv', mode='a') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(row)
            employee_file.close()
        flag=False
        print("Candy: Your feedback was important to us Thank You !!! Have a nice day !!!!")
       

