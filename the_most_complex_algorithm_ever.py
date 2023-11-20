import re
import numpy as np
import os
import random
import streamlit as st

@st.cache_data
def get_text_from_file(text_file_name):
    file = open(text_file_name, "r", encoding='utf-8') 
    file_contents = file.read()
    file.close()

    return file_contents

@st.cache_data
def clear_text(text):
    # видаляєм пунктуацію і цифри
    pattern = r"[^а-яА-Я'їЇіІґҐЄє \n]"
    clean_contents = re.sub(pattern, '', text)
    clean_contents = clean_contents.lower()
    # забираєм лишні пробіли
    clean_contents = re.sub(r'\s+', ' ', clean_contents)

    return clean_contents

def get_pairs_frequencies(text):
    clean_contents = clear_text(text)
    clean_contents = list(clean_contents)
    pairs = [clean_contents[i] + clean_contents[i + 1] for i in range(len(clean_contents) - 1)]#пари літер
    unique_values, counts = np.unique(pairs, return_counts=True)#унікальні пари
    unique_counts = dict(zip(unique_values, counts/len(pairs)))#унікальні пари і їх кількість у словнику 
    unique_counts = dict(sorted(unique_counts.items(), key=lambda item: item[1], reverse=True))#відсортований словник
    return unique_counts

def most_frequent_combinations(pairs_and_frequencies_dict, letter):
    three_combinations = [i for i in pairs_and_frequencies_dict if i[0]==letter][:3]
    return three_combinations

def get_filename_by_source(source):
    sources = {
        'book1': 'kostenko_zapysky.txt',
        'book2': 'markus-slidy.txt',
        'book3': 'mukharskyi-spovid.txt'
    }

    if source not in sources:
        raise Exception('WTF: Invalid source')

    filename = sources[source]

    current_dir = os.path.dirname(__file__)
    return os.path.join(current_dir, 'books', filename)

def get_three_words(combination, text):
    text = clear_text(text)
    words = list(map(lambda x: ' ' + x + ' ', (text.lower()).split()))
    dictionary = list(set([i.strip() for i in words if combination in i]))
    return random.sample(dictionary, 3)

