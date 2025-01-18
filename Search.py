import nltk
import regex as re
import os
import spacy 
import en_core_web_trf
import numpy as np 
import contractions
import math
import matplotlib.pyplot as plt
import string
import sys

from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.tokenize import word_tokenize

#Download stopwords - NLTK but only if it is not installed, else skip
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")
    
stop = set(stopwords.words('english'))

#load spaCy language model
nlp = spacy.load("en_core_web_trf")
nlp = en_core_web_trf.load()

#num of results to return 
top = 10

#folder containing html files
folder = "videogames"

#stores the current total of doc
def calcTotalDoc(totalDocs):
    try:
        for num in os.listdir(folder):
         totalDocs += 1
    #given that folder read has a problem, print error 
    except Exception as e:
        print(f"\nError reading file: {folder}\n{e}") 
        exit()
    #else return total docs as intended
    return totalDocs

#function to tokenize and clean text
def Tokenize(text,vocab,vocabID,htmlElements,query,totalTokens,Lemma):
 
 soup = BeautifulSoup(text,"html.parser")
 page = soup.get_text()
 
 tempClean = re.sub(r"[|\n\t\s]+"," ",page).strip()
 tempToken = word_tokenize(tempClean)
 totalTokens += len(tempToken)
 tempDoc = nlp(" ".join(tempToken))
 
 #Find title of webpage and store 
 title = soup.find_all("title")
 temp = 0
 
 #Finds title tag in html 
 for t in title:
     titles = t.get_text()
     #nltk tokenizes punctuation as well as words
     titles = word_tokenize(titles)
     for t in titles:
         htmlElements[temp] = ["title",t] 
         temp+=1
  
  #Finds description content in meta tag within doc    
 content = soup.find("meta", attrs={"name":"description"})
 if content:
     contents = content.get("content")
     contents = word_tokenize(contents)
     for c in contents:
         htmlElements[temp] = ["description",c] 
         temp+=1
         
  #Finds keyword content in meta tag within doc    
 keyword = soup.find("meta", attrs={"name":"keywords"})
 if keyword:
     keywords = content.get("content")
     keywords = word_tokenize(keywords)
     for k in keywords:
         htmlElements[temp] = ["keywords",k] 
         temp+=1
     
 
 #returns expanded contractions also remove starting space from doc
 doc = contractions.fix(text)
 
 #remove any text and unecessary punctuation and newline
 clean = re.sub(r"[\n\t]+|[?!<>()-:,\|]+|\s+"," ", page)
           
 tokens = nlp(clean)
 tokens = [token.text.strip() for token in tokens if not token.is_punct and token.text.lower() not in stop]       
 num = 0
 
 #add the vocab to dictionary
 for token in tokens:
  #Make sure no whitespace left     
  if len(token) > 0:
      if token not in Ftoken:
        Ftoken[num] = token
        num+=1    
   
      if token not in vocab:
        vocab[vocabID] = token
        vocabID+=1

 return vocabID,htmlElements,query,totalTokens,Lemma
       
#calculate term frequency with log weighting        
def calcTF(tf,weight):
    if tf > 0:
       tf = weight * (1 + math.log10(tf))
       return tf
    else:
        return 0

#calculate term frequency with log weighting to dampen idf        
def calcDF(df,N):
    if df > 0:
        df = math.log10(N/df)
        return df
    else:
        return 0

#calculate precision and display
def calcPrec(tp,fp):
    precision = tp/(tp+fp)
    #to convert decimal to %
    precision *= 100
    print(f"\nSearch Engine Ran At Precision = {precision}%")
 
#format termId:term (no repeats of vocab)
vocab = {} 
vocabID = 0  
totalTokens = 0
totalStop = 0
totalPunct = 0
Lemma = set()
LemmaID = 0
#main code to get user query
while True:
        
 #format id:name
 docIDs = {}

 #ids for each vocab/doc
 docIDNum = 0
 totalDocs = 0
 
 tokenCounter = 0
 
 total = calcTotalDoc(totalDocs)
 query = input("\nWhat would you like to query? (type Quit to exit)\n")
 
 if query == "Quit":
     break
 
 #split each query into individual term
 query = word_tokenize(query)
 
 #holds total tf-idf of queries in each document
 tfIdf = {}
 
 #holds individual tf-idf of each term in a query in each document
 tfIdfTerm = {}
 
 #holds individual tf-idf scores for each query in each document
 tfIdfQuery = {}
 
 #holds num of times token appears in each doc
 tokenFreq = {}
 
 #term frequencies of all terms in query in all docs
 freq = {}
 
 #inital df before log weighting 
 docFreq = defaultdict(int)
 
 #df weighting of individual terms 
 docFreqLog = {}
 
 #holds tokens relating to query appearing in doc - use list to allow multiple of same value
 tokenFound = {}
 
 count = 0
 tfIdfCount = 0
 
 terms = set()
 
 #read filenames in current folder
 for filename in os.listdir(folder):
     
    #Debugging
    #if docIDNum == 2:
    #     break
    
    #found tokens - with repeats of vocab
    Ftoken = {}
    
    #all elements in doument that are important in html 
    htmlElements = {}
     
    file_path = os.path.join(folder, filename)
    #store current file dir in filedir
    filedir = os.getcwd()+ "\\" + file_path
    
    #check if file is in dir 
    if os.path.isfile(file_path):
      #only read the file name and ignore everything else - like extentions .txt
      name = filename.split(".")[0]
      #then fill dictionary
      docIDs[docIDNum] = name

      #read this current file and store contents in page
      with open(filedir,"r",encoding='utf-8') as file:
       content = file.read()
       file.close()
    

    vocabID,htmlElements,query,totalTokens,Lemma = Tokenize(content, vocab, vocabID,htmlElements,query,totalTokens,Lemma)
    totalTf = 0
    totalTfIdf = 0
    totalDf = 0

    for queries in query:
     #remove /U error
     queries = queries.replace("\\","")
     
     #Flag for incrementing df
     incremented = False
     
     #Term frequency - num times term appears in a doc
     tf = 0
     
     #Document frequency - informativeness of term - reset per input
     df = 0 
     
     #Term weighting 
     weight = 1
            
     #use partial match of query
     for token in Ftoken.values(): 
       
       #Reset weighting per token 
       weight = 1
       
       #Flags to check if stopword or punctuation
       isPunct = False
       isStop = False
       
       #Check if current term looking at is punctuaion or stopword
       if queries in stop:
           isStop = True
       else:
           if queries in string.punctuation:
               isPunct = True
               
       #Term weighting based on token found in html
       for element in htmlElements.values():
           #If token is in html
           if token in element[1]:
               
               #if token is a title
               if element[0] == "title":
                   weight = 1.75
               
               #meta description content tag
               elif element[0] == "description":
                       weight==1.5 
               else:
                   #meta keyword content tag
                   if element[0] == "keywords":
                       weight==1.5   
               break
               
       #If token full matches with query  
       if re.fullmatch(queries,token):
           #Check if full match and is Stopword or Puncutation if so apply lower weight
           if isStop or isPunct:
               weight = 1.05
           else:
               weight = 1.5
           tokenFound[tokenCounter] = [docIDNum,token]
           tokenCounter+=1
           tf +=1
               
       #If token full matches with query but lowercase        
       elif re.fullmatch(queries,token,re.IGNORECASE):
           if isStop:
               weight = 1.05
           else:
                weight = 1.4
                
           tokenFound[tokenCounter] = [docIDNum,token]
           tokenCounter+=1
           tf +=1     
           
       else:  
           #If token is within a word it could be related but smaller weight  
           if re.match(queries,token, re.IGNORECASE):
               weight = 1.2
               tokenFound[tokenCounter] = [docIDNum,token]
               tokenCounter+=1
               tf = tf + 1 
       
       #Increment df as long as term hasn't been read and has a tf
       if not incremented and queries not in terms and tf > 0:
            incremented = True
            docFreq[queries] +=1     
            terms.add(queries) 
       #If term doesn't exist still add it to docFreq for comparing 
       if tf == 0 and queries not in terms:
            docFreq[queries] = 0        
         
     totalTf += tf                
     
     #Store freq - formatted by (documentID,queryName,Term Frequency)
     Tf = calcTF(tf,weight)

     freq[count] = [docIDNum,queries,Tf]
     count+=1
    
    #only print if found in doc     
    if totalTf > 0:
        print(f"Term found in: document[{docIDNum}] ({totalTf} times)") 
        tokenFreq[docIDNum] = totalTf       
    docIDNum +=1
    
    for term in docFreq:
        docFreqLog[term] = calcDF(docFreq[term],total)
    
    counter = 0
    
    #Store Tf-Idf for each term in query
    for i in range(total):
        #for each value stored within freq
        for items in freq.values():
            #if current document is in freq
            if items[0] == i:
                #find the df of that term then * by the tf
                for name,df in docFreqLog.items():
                    if name == items[1]:
                        tfIdfTerm[counter] = [i,name,(df * items[2])]
                        counter+=1
                        
    #Store total Tf-Idf for each document - similar process to method above                  
    for i in range(total):
        tfIdfTotal = 0
        for items in tfIdfTerm.values():
            if items[0] == i:
                tfIdfTotal += items[2]
            tfIdf[i] = tfIdfTotal
 
 #Calculate Tf-Idf of Query 
 QueryTF = {} 
 QueryTfIdf = {}
 
 #First calc tf of each term
 queryTfCounter = 0
 for queries in query:
    queryTf = query.count(queries)
    queryTfLog = calcTF(queryTf,1)
    QueryTF[queries] = queryTfLog
 
 #Then multiply by existing idf to get TfIdf
 for name,df in docFreqLog.items():
     for queries,tf in QueryTF.items():
         if name in queries:
             querytfidf = df * tf
             QueryTfIdf[name] = querytfidf  
 
 #After that find the dot product of query and document
 queryDot = {}

 #For doc and term in query get TfIdf and multiply together
 for i in range(total):
     currentAngle = 0
     for terms in tfIdfTerm.values():
         if terms[0] == i:
             for name,queryTFIDF in QueryTfIdf.items():
                 if name == terms[1]:
                     currentAngle += terms[2] * queryTFIDF
                 queryDot[i] = currentAngle  
                 
 #Calculate magnitude of Query and Doc Vector    
 
 #Find magnitude - all TfIdf scores squared added together then find root of total
 currentQueryTotal = 0
 
 #Magnitude of query
 for name,tfidf in QueryTfIdf.items():
     currentQueryTotal += math.pow(tfidf,2) 
 queryVec = math.sqrt(currentQueryTotal)   
 
 currentDocTotal = 0
 
 #Magnitude of docs
 for tfidf in tfIdfTerm.values():
     currentDocTotal += math.pow(tfidf[2],2) 
 docVec = math.sqrt(currentDocTotal) 
 
 #Doc Vector multiplied by Query Vector
 totalVec = docVec*queryVec   
 
 queryAngle = {} 
 
 #Then divide dot product by magnitude
 for docID,dot in queryDot.items():
     if totalVec <= 0:
         queryAngle[docID] = 0
     else:    
         queryAngle[docID] = dot/totalVec
              
 #sort tf-idf scores desc       
 tfIdf = dict(sorted(tfIdf.items(), key=lambda item:item[1],reverse=True))
 #Sort queryAngle by angles
 queryAngle = dict(sorted(queryAngle.items(), key=lambda item:item[1],reverse=True))
 
 #make sure some documents are displayed even if nothing appears
 for i in range(total):
     if i not in tfIdf:
         tfIdf[i] = 0

 i = 1
 
 #Note - to rank by tfIdf replace below in list use (tfIdf.items() or rank by angle use (queryAngle.items()
 for docnum, tfidf in list(queryAngle.items())[:top]:
    #retrieve corresponding name by id from docIDs
    docname = docIDs.get(docnum," ")
    print(f"{i}: [{docname}]-{tfidf}")
    i+=1   
 
 #Next find relevance feedback   
 print("\nFrom the Top 10 are the documents found relevant?")
 
 j = 1
 
 #holds values if doc was relevant or not (true positive and false positive)
 tp = 0
 fp = 0
 
 times = {}
 
 x = np.array([])
 y = np.array([])

 for docnum, tfidf in list(tfIdf.items())[:top]:
    docname = docIDs.get(docnum," ")
    print(f"\nDocument name: {docname}")
    display = np.array([])
    #Display useful info to user to help determine relevance 
    #such as times appeared and tokens that actually appeared
    for doc, name in list(tokenFreq.items()):
        
      #Display num of times query appeared in doc  
      if docnum == doc:
          print(f"Query: {query} appeared: ({name} times)")
          times[j] = name
          j+=1
          
          if len(tokenFound) != 0:
           for items in tokenFound.values():
              if items[0] == doc:
                  display = np.append(display,items[1])
    
    #Display tokens in document as long as they were found
    if display.size != 0:             
        print(f"\nTokens found based on your query: {display}")
    else:
        print(f"No tokens were found")
            
    #Manual Relevance Feedback
    relevance = input("\nWas this document relevant - type (Yes) or (No)\n")
    
    while True:
        if relevance.lower() == "yes" or relevance.lower() == "no":
            
            if relevance.lower() == "yes":
                tp+=1
                break
        
            if relevance.lower() == "no":
                fp+=1
                break
        
        #Make sure user can only type yes or no otherwise keep asking them until then   
        else:
            print("\nInvalid Output")
            relevance = input(f"Was this document relevant ({docname})- type (Yes) or (No)\n")
 
 # Display Precision Given that no errors occur 
 try:                  
  calcPrec(tp,fp)
  #Throw an error is something does go wrong 
 except Exception as e:
        print(f"\nError trying to calculate Precision: \n{e}") 
        exit()
        
 

         

#Plan for creating Seach Engine :

#Scoring on tf-idf 

#1 get user input
#2 read each file in folder
#3 tokenize each word and add to respective dictionary
#4 clean tokens using pre-processing techniques
#5 calculate tf,idf, tf-idf
#6 sort by tf-idf or convert to angle (desc) (larger tf-idf means closer)
#7 get top 10 documents by tf-idf score
#8 display top 10
#9 calculate precision and display

#Or if using angles:

#6 convert tf-idf to angle
#7 sort by angle (asc) (smaller means closer) 
#8 get top 10 documents by angle 
#9 display top 10
#10 calculate precision and display



#code for testing - this may be used later
    
'''
 for value in tfIdf.values():
     if i < top :
         print(value)
         i+=1
     else:
        break
'''   

'''       
    #for each docID add to freq list
    if docIDNum not in freq:
        freq[docIDNum] = tf    
    docIDNum+=1
    print(freq)
 '''  

'''  
    #convert dictionary to numpy array for efficiency 
    list = list(docIDs.items())
    array = np.array(docIDs)
    print(array)
'''
 

'''
    #otherwise raise an error since folder probably dosen't exist
else:
    if filename not in os.listdir(folder):
     raise Exception("Folder videogames doesn't exist in current directory")
'''    

#Useful code - for visuals on flowchart


#To see distrubution of punctuation and stopwords within the collection:
'''    
#Add this after count = 0

 #Find words that aren't consisting of Stopwords and Punctuation
 Other = StopLen[-1] - (StopwordsLen[-1] + PunctLen[-1])
 
 #get last element of list 
 print(f"Total number of words in collection (including stopwords): {StopLen[-1]}\n")
 print(f"Number of punctuation: {PunctLen[-1]}")
 print(f"Number of stopwords in collection: {StopwordsLen[-1]}")
 
 print(f"\nTotal number of words in collection (not including punctuation or stopwords): {Other}")
 
 y = np.array([PunctLen[-1],StopwordsLen[-1],Other])
 pielabels = ["Punctuation","Stopwords","Other"]
 
 font1 = {"family":"serif","color":"blue","size":20}
 plt.title("Vocab in collection", fontdict=font1, loc = "center")
 plt.pie(y,labels=pielabels)
 plt.show()
'''