from ..constants.const_path import CSVPATH
from ..constants.const_variable import VOCAB_CATEGORIES, VOCAB_ALPHABET_BY_CATEGORY, CURRENT_WORD_INDEX
from ..constants.const_session_request import VOCAB_TYPE, VOCAB_CATEGORY, VOCAB_LIST
import random
import pandas as pd

def get_vocabulary_type():
    # get data from csv
    df = pd.read_csv(CSVPATH)
    vocab_type_list = df["Type"].unique()
    return vocab_type_list.tolist()


def get_vocabulary(request):
    vocab_list = []
    selected_type = request.session[VOCAB_TYPE]
    selected_category = request.session[VOCAB_CATEGORY]

    # get neccessary information before render the practice template
    if selected_category != "":
        vocab_list = get_vocabulary_by_type_and_category(selected_type, selected_category)
    else:
        vocab_list = get_vocabulary_by_type(selected_type)
    return vocab_list


def get_vocabulary_by_type(vocab_type):
    # get data from csv
    df = pd.read_csv(CSVPATH)
    # filter the data with the selected type
    vocab_list = df[df['Type'] == vocab_type].values.tolist()
    return vocab_list


def get_vocabulary_length_by_type(vocab_type):
    vocab = get_vocabulary_by_type(vocab_type)
    return len(vocab)


def get_vocabulary_by_type_and_category(vocab_type, category):
    vocab_list = []

    # check for category and get vocab by type and category
    for i in range(len(VOCAB_CATEGORIES)):
        if category == VOCAB_CATEGORIES[i]:
            # get data from csv
            df = pd.read_csv(CSVPATH)
            data = df[(df['Type'] == vocab_type) & (df['Category'].isin(VOCAB_ALPHABET_BY_CATEGORY[i]))]
            vocab_list = data.values.tolist()
    return vocab_list


def random_choice(vocab, word_amount):
    vocab = list(vocab)
    return vocab[random.randint(0, word_amount - 1)][4]


def find_blank_index(choices):
    choices = list(choices)
    random_index = 0
    status = False

    while status == False:
        # get random number from choices index
        random_index = random.randint(0, len(choices) - 1)
        found_index = choices[random_index]

        # change status to True and return the blank index
        if found_index == "":
            status = True
        else:
            continue
    return random_index


def check_choice(vocab, current_index, choice):
    if choice == vocab[current_index][4]:
        return False
    else:
        return True


def create_choices(request):
    vocab = list(request.session[VOCAB_LIST])
    current_index = int(request.session[CURRENT_WORD_INDEX])
    choices = ["", "", "", ""]
    choice_count = 0

    while choice_count < 3:
        word_check = False

        # check that the first three choice is not answer
        choice = random_choice(vocab, len(vocab))
        word_check = check_choice(vocab, current_index, choice)

        while word_check != True:
            choice = random_choice(vocab, len(vocab))
            word_check = check_choice(vocab, current_index, choice)

        if choice in choices:
            continue
        else:
            blank_index = find_blank_index(choices)
            choices[blank_index] = choice

            # check the choices
            print(choices)
            choice_count += 1

    # check and insert the answer
    blank_index = find_blank_index(choices)
    choices[blank_index] = vocab[current_index][4]
    print(choices)
    return choices

def check_result(answer, request):
    correct_answer = get_correct_answer(request)
    if answer == correct_answer:
        return True
    else:
        return False
    

def get_correct_answer(request):
    vocab = request.session[VOCAB_LIST]
    current_index = request.session[CURRENT_WORD_INDEX]
    return vocab[current_index][4]