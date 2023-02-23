# A compilation of helper functions for use in other files
# Marc St. Pierre
# 1/6/2023

import csv
import string
import os
import time
from collections import Counter
from typing import List
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sentence_transformers import SentenceTransformer, util
NLP_MODEL = SentenceTransformer('all-MiniLM-L6-v2')
WORDNET_LEMMATIZER = WordNetLemmatizer()
IGNORE_WORDS = [
    'anishinabek',
    'westbank',
    'tlicho',
    'tsawwassen',
    'nacho',
    'nyak',
    'teslin',
    'tlingit',
    'part',
    'chapter',
    'section',
    'subsection',
    'first',
    'nation'
]


# helper functions


def cleanup(text, ignore_words=[]):
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
    # removing special words
    sample = [token for token in sample if token not in ignore_words]
    # lemmatization of words means to simplify versions of words with the same meaning to a base version
    sample = [WORDNET_LEMMATIZER.lemmatize(token) for token in sample]
    # putting everything back together into a string
    sample = " ".join([word for word in sample])
    return sample


def check_similar(search_text, compare_text):
    # returns the score as an integer which represents the number of hits
    x_list = set(search_text.split())
    y_dict = Counter(compare_text.split())
    score = 0
    for word in x_list:  # this should be a set; wrap it in the set function; considered a logic error
        if word in y_dict:
            score += y_dict[word]
    return score


def format_cell(row):
    # string formatter for individual cells in csv
    key = f"{row[0]}\n{row[1]}"
    value = f"Part: {row[2]}\nSection: {row[3]}\nReference: {row[4]}\nText: {row[5]}\n\n\n"
    return key, value


def format_export(fields, data, cluster_map):
    export = []
    exclude_provisions = sorted([row_index for sublist in cluster_map for row_index in sublist])

    # collect clustered provisions first
    for cluster in cluster_map:
        common = dict.fromkeys(fields, '')
        searchable = ''
        for row_index in cluster:
            searchable += f"{data[row_index][6]}"
            cell = format_cell(data[row_index])
            common[cell[0]] += cell[1]
        common['Search Terms'] = searchable
        export.append(common)

    # then collect all remaining unique provisions
    for row_index in range(len(data)):
        if row_index not in exclude_provisions:
            unique = dict.fromkeys(fields, '')
            searchable = f"{data[row_index][6]}"
            unique['Search Terms'] = searchable
            cell = format_cell(data[row_index])
            unique[cell[0]] = cell[1]
            export.append(unique)
    return export


def collect_agreements(source_path):
    data = []
    agreement_names = []
    for filename in os.listdir(source_path):
        file_path = os.path.join(source_path, filename)
        with open(file_path, 'r') as file:
            csvreader = csv.reader(file)
            next(csvreader, None)  # skip header
            for row in csvreader:
                data.append(row)
                agreement_name = f"{row[0]}\n{row[1]}"
                if agreement_name not in agreement_names:
                    agreement_names.append(agreement_name)
    print_agr = '\n'.join([name for name in agreement_names])
    print(f"Agreements are:\n{print_agr}")
    print(f"{len(data)} provisions collected.")
    return agreement_names, data


def cluster_provisions(sentences, size=2, match_percent=0.85):
    start_time = time.time()
    print("Encoding the corpus; This might take a while...")
    corpus_embeddings = NLP_MODEL.encode(sentences, batch_size=64, show_progress_bar=True, convert_to_tensor=True)
    clusters = util.community_detection(corpus_embeddings, min_community_size=size, threshold=match_percent)
    print(f"{len(sentences)**2} provision comparisons done after {round(time.time() - start_time)} seconds.")
    return clusters


def search_filter(data, search_string):
    output = []
    for row in data:
        search_score = check_similar(search_string, row['Search Terms'])
        if search_score > 0:
            row['Search Score'] = search_score
            output.append(row)

    output = sorted(output, key=lambda item: item['Search Score'], reverse=True)
    return output


