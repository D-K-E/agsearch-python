# agsearch-python
A Very Simple Command Line Based Ancient Greek Search Engine in Python 

There are mainly two features in this engine:

- Text similarity search

- Tf-idf metrics


```
usage: search.py [-h] {0,1} filepath {1,2}

Ancient Greek Search Engine

positional arguments:
  {0,1}       update term info before proceeding with search
  filepath    File path that includes search terms separated by a newline character
  {1,2}       Choose your searcher: 1->Similarity, 2->TfIdf search

optional arguments:
  -h, --help  show this help message and exit
```

## Install

- For those who are using conda: `conda env create -f environment.yml`

- Then: `conda activate agsearch`

If you are not using conda, there are two main dependencies:

- `scikit-learn`

- `numpy`


## Intended Public and Usage

This library is made for and by ancient historians working on ancient greek
texts. 
Basically the usage scenario for the tf-idf metric search is following:

I have a series of keywords that I find interesting and important for a given
number of documents. I want to gather the texts that are in relation with the
these keywords. Thus, I want to order my set of texts, with respect to my
keywords, such that the most significant text with respect to a keyword
appears first in a list of documents containing the keyword.
I create a document which contains my keywords separated by newline character.
If the documents that I want to use as database is not included in
`textinfo.json`, I add them to this database file. The location of texts
should be specified with respect to the location of the `textinfo.json` file.

TODO: continue usage scenarios
