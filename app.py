import streamlit as st
import pandas as pd
import numpy as np
import the_most_complex_algorithm_ever as tmcae
import matplotlib.pyplot as plt
import random

@st.cache_data
def get_frequencies_of(iterable):
    unique_values, counts = np.unique(iterable, return_counts=True) # унікальні пари
    unique_counts = dict(zip(unique_values, counts/len(iterable))) # унікальні пари і їх кількість у словнику 
    unique_counts = dict(sorted(unique_counts.items(), key=lambda item: item[1], reverse=True))# відсортований словник
   
    return unique_counts

@st.cache_data
def get_double_combinations(text):
    return [text[i:i+2] for i in range(len(text)-1)]

@st.cache_data
def group_by_first_letter(frequencies):
    groupped = {}

    for k, v in frequencies.items():
        if k[0] not in groupped:
            groupped[k[0]] = {}
        groupped[k[0]][k[1]] = v
    
    return groupped

st.set_page_config(page_title='Двобуквенні комбінації')
st.header('Частота двобуквенних комбінацій')
books = {
    "Антін Мухарський - Доба. Сповідь молодого бандерівця": 'mukharskyi-spovid.txt',
    "Ліна Костенко - Записки українського самашедшого": 'kostenko_zapysky.txt',
    "Валерій Маркус - Сліди на дорозі": 'markus-slidy.txt',
}

titles = list(books.keys())
book = st.selectbox(label="Книжка", options=titles, index=0)

text = tmcae.get_text_from_file(f'books/{books[book]}')
text = tmcae.clear_text(text)

double_combinations = get_double_combinations(text)
frequencies = get_frequencies_of(double_combinations)

groupped = group_by_first_letter(frequencies)
alphabet = list(groupped.keys())
EPS = 10**-4

st.subheader(f'Враховано частоти, які більші за {EPS}')

all_letters = st.checkbox('Усі літери', value=False)

if not all_letters:
    letters_to_display = st.multiselect("Літери", sorted(alphabet))
else:
    letters_to_display = groupped.keys()
top = st.number_input(label="Кількість топ літер:", value=3)

fig, ax = plt.subplots()
for letter in letters_to_display:
    cum_sum = 0
    groupped_by_letter = groupped[letter]
    for index, second_letter in enumerate(groupped_by_letter):
        if index == top:
            break

        probability = groupped[letter][second_letter]
        if probability > EPS:
            ax.bar(letter, probability, bottom=cum_sum)
            ax.text(letter, cum_sum, second_letter, ha='center', va='bottom')
            cum_sum += probability

plt.gca().invert_yaxis()
st.pyplot(fig)

# df = pd.DataFrame.from_dict({(i, j): groupped[i][j] for i in groupped.keys() for j in groupped[i].keys()}, orient='index')
# st.write(df)

df = pd.DataFrame(groupped)
st.table(df)