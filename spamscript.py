####----*----SpamScript----*----####
"""

SpamScript performs the following:

    Loads email delivery data as a Pandas DataFrame object.
    Loads spam terms as a Pandas DataFrame object.
    Outputs a CSV-file named `spam_over_40.csv` for email subject lines,
    which contain said spam terms, and spammed >= 40% in at least one ESP,
    excluding Microsoft Outlook.
    Outputs a CSV-file named `spam_over_80.csv` for email subject lines,
    which contain any words in said spam terms, and spammed >= 80% in at least one ESP,
    excluding Microsoft Outlook.

"""

##### Directions #####
'''
For best results:
	1) Have Anaconda Python 3.x installed
	2) Run `nltk.download()`, and download all packages.
	3) Place `spamscript.py` and the two other files in the same folder.
	4) Ensure that the `email data` & `spam word` files to be processed are in `csv UTF-8` format.
	5) It works best to name the files `data.csv` & `words.csv` for quick typing.
	6) Open or cd `terminal` (MacOS), or `cmd` (Windows), to the folder in which the files are located.
	7) Type `python spamscript.py` (or `python3 spamscript.py`) in the shell window, and push `ENTER`.
	8) Respond to the prompts in the shell window, and push `ENTER`.
	9 Check the folder in which the file was run for `spam_over_40.csv` & `spam_over_80.csv`.
'''
######################

## Importing Libraries ##
import pandas as pd # Manipulates DataFrames
import numpy as np # Higher-level Math Library
from nltk.stem.snowball import SnowballStemmer # Linguistic-processing Package
import re # Processes Regular Expressions

## Function Definitions ##
def cleansub(DataFrame):
	'''
	Takes a Pandas DataFrame object.
	Cleans all subjects withing the Pandas DataFrame object,
	using a regular expression; then, reduces each word to its
	linguistic stem before rejoining the subjects.
	Returns a Pandas DataFrame object.
	'''
	df = DataFrame[:]
	stemmer = SnowballStemmer("english")
	df.subject = df.subject.str.lower()
	regex_pat = re.compile(r'[^\w\d\s$%]')
	df.subject = df.subject.str.replace(regex_pat, '')
	df.subject = df.subject.str.split(' ')
	df.subject = df.subject.apply(lambda x: [stemmer.stem(y) for y in x])
	df.subject = [' '.join(sent) for sent in df.subject]
	return df

def cleantokens(DataFrame):
	'''
	Takes a Pandas DataFrame object,
	cleans it using a regular expression,
	tokenizes each phrase,
	returns a List of tokenized phrases.
	'''
	df = DataFrame[:]
	stemmer = SnowballStemmer("english")
	tokenlist = df[df.columns[0]].str.lower().tolist()
	tokenlist = [re.sub(r'[^\w\d\s$%]', '', sent) for sent in tokenlist]
	tokens = []
	for sent in tokenlist:
		nsent = []
		sent = sent.split()
		for word in sent:
			nword = stemmer.stem(word)
			nsent.append(nword)
		tokens.append(nsent)
	tokens = [' '.join(sent) for sent in tokens]
	return tokens


def submatch40(DataFrame, tokens):
	'''
	Takes a Pandas DataFrame object, and a List of Strings.
	Matches the tokenized words with tokenized DataFrame 'subject' fields,
	which contain said tokenized phrases.
	Returns a Pandas DataFrame object.
	'''
	locs = set()
	df = DataFrame[:]
	for sent in tokens:
		ix = list(np.where(df.subject.str.contains(sent))[0])
		for num in ix:
			if num > 0:
				locs.add(num)
	locs = list(locs)
	df = df.iloc[locs]
	return df

def submatch80(DataFrame, tokens):
	'''
	Takes a Pandas DataFrame object, and a List of Strings.
	Performs set-matching, using the tokenized words,
	with tokenized DataFrame 'subject' fields,
	which may contain *any* of said tokens.
	Returns a Pandas DataFrame object.
	'''
	tokenset = set()
	tokens = [sent.split() for sent in tokens]
	[tokenset.add(word) for sent in tokens for word in sent]
	tokenset = list(tokenset)
	locs = set()
	df = DataFrame[:]
	for token in tokenset:
		ix = list(np.where(df.subject.str.contains(token))[0])
		for num in ix:
			if num > 0:
				locs.add(num)
	locs = list(locs)
	df = df.iloc[locs]
	return df

##### Main Function #####

## Loading Data ##
data = pd.read_csv(str(input("Enter the email datafile's name: "))) # loads email data
spamwords = pd.read_csv(str(input("Enter the spamwords datafile's name: "))) # loads spam words

## Selecting Data Columns ##
spamcolumns = [column for column in list(data.columns) if 'spam' in column and 'outlook' not in column] # finds spam columns in email DataFrame

## Cleaning Spamwords ##
tokens = cleantokens(spamwords) # gets processed tokens

## Finding & Generating 40% matches ##
over40 = data[spamcolumns].where(data[spamcolumns] >= 40) # gets email data rows where any spam rate is over 40%.
ix40 = list(np.where(data[spamcolumns] >= 40)[0]) # gets indices of the above.
over40 = data.loc[ix40] # generates new DataFrame based on above indices.
over40 = cleansub(over40) # cleans subject fields of DataFrame.
over40 = submatch40(over40, tokens) # generates DataFrame where subjects match tokens.
over40_ind = list(over40.index) # gets original indices of rows in 'data'.
over40 = data.loc[over40_ind] # generates new DataFrame from original 'data' based on above indices.
over40.to_csv('spam_over_40.csv') # saves DataFrame as csv file.

## Finding & Generating 80% matches ##
over80 = data[spamcolumns].where(data[spamcolumns] >= 80) # gets email data rows where any spam rate is over 80%.
ix80 = list(np.where(data[spamcolumns] >= 80)[0]) # gets indices of the above.
over80 = data.loc[ix80] # generates new DataFrame based on above indices.
over80 = cleansub(over80) # cleans subject fields of DataFrame.
over80 = submatch80(over80, tokens) # generates DataFrame where subjects match tokens.
over80_ind = list(over80.index) # gets original indices of rows in 'data'.
over80 = data.loc[over80_ind] # generates new DataFrame from original 'data' based on above indices.
over80.to_csv('spam_over_80.csv') # saves DataFrame as csv file.
