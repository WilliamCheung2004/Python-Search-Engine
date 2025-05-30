# Search Engine
Simple search engine in Python that searches through a bunch of html files for some words you are looking for.

How this works is:
* You input something to search for
* Loops through the video games folder for each webpage
* Checks how "close" your word is to each word in each webpage
* Then does some weighting calculations to rank each result
* Finally displays top 10 results which should be close to your search input

* Involves using natural learning libraries such as nltk, spaCy and numpy
* Weighting - for results
* Page searching using Beautiful Soup
--- 

## Instructions

I recommend running this in Visual Studio Code or any other IDE supporting NLTK, Beautiful Soup, etc. 
In the terminal run these commands to download:

### Install Beautiful Soup
* pip3 install beautifulsoup4

### Install Nltk
* pip install nltk

### Install Numpy
* pip install numpy

### Install Spacy
* pip install spacy

### As well as the language model for spaCy
* python -m spacy download en_core_web_trf
* (Replace python depending on your python version you may need to search this)
---

## Note 
Also make sure you have the folder videogames in the same directory as the script which contains all html files this (should be 399 .html files)

---

## Limitations
* Currently does accurately search for words with minimal meanings
* But doesn't really have syntatic searching yet e.g. if you search for Python it could search up a snake or the programming language depending on the pages
* Only searches through a set list of html files within videogames

---

## Credits 
William Cheung 
