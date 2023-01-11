# A compilation of helper functions for use in other files
# Marc St. Pierre
# 1/6/2023

import csv
import string
import os
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
WORDNET_LEMMATIZER = WordNetLemmatizer()


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
    sample = [WORDNET_LEMMATIZER.lemmatize(token) for token in sample]
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


def sort_descending(array, index):
    # quicksort
    greater = []
    equal = []
    less = []

    if len(array) > 1:
        pivot = array[0][index]
        for x in array:
            if x[index] < pivot:
                less.append(x)
            elif x[index] == pivot:
                equal.append(x)
            elif x[index] > pivot:
                greater.append(x)
        return sort_descending(greater, index)+equal+sort_descending(less, index)
    else:
        return array


def format_export(data, path, field_names):
    # formats the data and then exports a csv file
    with open(path, 'w', newline='') as file:
        csvwriter = csv.DictWriter(file, fieldnames=field_names)
        csvwriter.writeheader()
        csvwriter.writerows(data)


def compile_row_ids():
    data_folder = 'C:/Users/marcs/Documents/provisionsProject/Data/agreements'
    row_id = 1
    data = []
    for filename in os.listdir(data_folder):
        file_path = os.path.join(data_folder, filename)
        with open(file_path, 'r') as file:
            csvreader = csv.reader(file)
            next(csvreader, None)  # skip header
            for row in csvreader:
                data.append([str(row_id)] + row)
                row_id += 1
    return data


def collect_provisions(data_source_path, search_string, match_threshold_float):
    data = []
    with open(data_source_path, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            # will need to check back on this to change the index number if the underlying csv's change format
            compare_string = cleanup(row[2] + " " + row[3] + " " + row[5])
            score_float = check_similar(search_string, compare_string)
            if score_float >= match_threshold_float:
                data.append(row + [score_float])
    return data




