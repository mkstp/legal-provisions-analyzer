# collect then export matching provisions to csv
# Marc St. Pierre 1/4/2023


# setup

import csv
import os
import string
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

wordnet_lemmatizer = WordNetLemmatizer()


# test globals (to be provided eventually by external input)

search_input = 'adoption'
match_threshold = 0.3
selected_files = [
    'ANprovisionsdb.csv',
    'SVprovisionsdb.csv',
    'TLprovisionsdb.csv',
    'TSprovisionsdb.csv',
    'WBprovisionsdb.csv'
]


# helper functions


def cleanup(text):
    # making everything lower case for faster comparisons
    sample = text.lower()
    # removing all english-based punctuation (this will also remove punctuation used in indigenous language)
    sample = "".join([char for char in sample if char not in string.punctuation])
    # removing all numbers from the text
    sample = "".join([char for char in sample if not char.isdigit()])
    # transforming the string to a list of words
    sample = word_tokenize(sample)
    # removing stop words 'of' 'and' 'or' etc.
    sample = [token for token in sample if token not in stopwords.words('english')]
    # lemmatization of words means to simplify versions of words with the same meaning to a base version
    sample = [wordnet_lemmatizer.lemmatize(token) for token in sample]
    return sample


def check_similar(search_text, compare_text):
    # implementation of a cosine similarity algorithm
    # this changes each input string into a vector then compares their similarity as an angular distance
    x_set = {word for word in search_text}
    y_set = {word for word in compare_text}
    rvector = x_set.union(y_set)
    xvector = []
    yvector = []
    for word in rvector:
        if word in x_set:
            xvector.append(1)
        else:
            xvector.append(0)
        if word in y_set:
            yvector.append(1)
        else:
            yvector.append(0)
    c = 0
    for i in range(len(rvector)):
        c += xvector[i]*yvector[i]
    if c > 0:
        cosine = c / float((sum(xvector)*sum(yvector))**0.5)
        return cosine
    else:
        return 0.0


def sort_by(array, index):
    # quicksort
    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0][index]
        for x in array:
            if x[index] < pivot:
                less.append(x)
            elif x[index] == pivot:
                equal.append(x)
            elif x[index] > pivot:
                greater.append(x)
        return sort_by(greater, index)+equal+sort_by(less, index)
    else:
        return array


def format_export(array, destination_path):
    # formats the data and then exports a csv file
    with open(destination_path, 'w', newline='') as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow([
            'agreement',
            'year',
            'provisionNum',
            'part',
            'section',
            'provisionText',
            'matchPercent'])
        for row in array:
            csvwriter.writerow(row)
        file.close()


# main function


def collect_provisions(search_string, match_threshold_float, filename_shortlist, export=False):
    # collects all provisions that match a search string above a certain threshold
    data_folder = 'C:/Users/marcs/Documents/provisionsProject/Data/'
    destination = 'C:/Users/marcs/Documents/provisionsProject/Data/export.csv'
    data = []
    match_threshold_index = -1
    search_string = cleanup(search_string)
    for filename in os.listdir(data_folder):
        if filename in filename_shortlist:
            with open(data_folder + filename, 'r') as file:
                csvreader = csv.reader(file)
                for row in csvreader:
                    # will need to check back on this to change the index number if the underlying csv's change format
                    compare_string = cleanup(row[3] + " " + row[4] + " " + row[5])
                    score_float = check_similar(search_string, compare_string)
                    if score_float >= match_threshold_float:
                        data.append(row + [score_float])
            file.close()
    data = sort_by(data, match_threshold_index)
    # export to csv
    if export:
        format_export(data, destination)
    return data


printable = collect_provisions(search_input, match_threshold, selected_files, True)

# testing the output
for i in printable:
    print(i)



