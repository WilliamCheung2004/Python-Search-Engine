# Search Engine
Simple search engine in Python that searches through a bunch of html files for some words you are looking for - basically just weights how close the words are to the worlds found in the videogames directory then displays the top 10 search results - this should work if you add some custom html files to the video games folder if you wanted to test some more pages. 

* Involves using natural learning libraries such as nltk, spaCy and numpy
* Weighting - for results
* Page searching using Beautiful Soup
--- 

## Instructions

Whilst I ran this in Visual Studio Code this should be runnable as long as:
Within (where you run the code) in the terminal run these commands to download:

Ensuring that bs4 is installed for Beautiful Soup
(pip3 install beautifulsoup4)

Ensuring NLTK is installed 
(pip install nltk)

Ensuring numPy is installed 
(pip install numpy)

Ensuring spaCy is installed 
(pip install spacy)

As well as the language model for spaCy
(python -m spacy download en_core_web_trf)

---

## Note 
Also make sure you have the folder videogames in the same directory as the script which contains all html files this (should be 399 .html files)

---

## Limitations
* Currently does accurately search for words with minimal meanings
* But doesn't really have syntatic searching yet e.g. if you search for Python it could search up a snake or the programming language depending on the pages

---

## Credits 
William Cheung 
