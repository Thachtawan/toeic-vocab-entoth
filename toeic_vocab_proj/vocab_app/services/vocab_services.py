from ..constants.const_path import CSVPATH
from ..constants.const_variable import VOCAB_CATEGORIES, VOCAB_ALPHABET_BY_CATEGORY, CURRENT_WORD_INDEX, \
    SELECTED_MAIN_MENU, SELECTED_SUB_MENU, SELECTED_MODE, VOCAB_MENU, SELECTED_PART
from ..constants.const_session_request import VOCAB_TYPE, VOCAB_CATEGORY, VOCAB_LIST, MENU
import math
import random
import pandas as pd
    

def get_vocabulary_type():
    # get data from csv
    df = pd.read_csv(CSVPATH)
    vocab_type_list = df["part of speech"].unique()
    return vocab_type_list.tolist()


def get_vocabulary(request):
    vocab_list = []
    selected_mode = request.session[SELECTED_MODE]
    selected_sub_menu = request.session[SELECTED_SUB_MENU]
    selected_part = request.session[SELECTED_PART]
    print("selected_mode: " + str(selected_mode))
    print("selected_menu: " + str(selected_sub_menu))
    print("selected_mode: " + str(selected_part))
    
    if selected_mode != "":
        vocab_by_part = get_vocab_by_part(request)
        vocab_list = vocab_by_part[(int(selected_part) - 1)]
    else:
        vocab_list = get_vocabulary_by_type(selected_sub_menu)

    return vocab_list


def get_vocabulary_by_main_menu(request):
    vocab_list = []
    selected_main_menu = request.session[SELECTED_MAIN_MENU]
    print("selected_main_menu: " + selected_main_menu)
    # get data from csv
    df = pd.read_csv(CSVPATH)
    if selected_main_menu == VOCAB_MENU[1]:
        vocab_list = df[df["oxford"] == 1].values.tolist()

    elif selected_main_menu == VOCAB_MENU[2]:
        vocab_list = df[df["academic"] == 1].values.tolist()

    elif selected_main_menu == VOCAB_MENU[4]:
        vocab_list = df[df["ielts"] == 1].values.tolist()

    return vocab_list


def get_vocabulary_by_CEFR_lvl(level):
    # get data from csv
    df = pd.read_csv(CSVPATH)
    vocab_list = df[df["cefr"] == level].values.tolist()
    return vocab_list


def get_vocabulary_by_type(vocab_type):
    # get data from csv
    df = pd.read_csv(CSVPATH)
    # filter the data with the selected type
    vocab_list = df[df['part of speech'] == vocab_type].values.tolist()
    return vocab_list


def get_vocabulary_length_by_type(vocab_type):
    vocab = get_vocabulary_by_type(vocab_type)
    return len(vocab)


def random_choice(vocab, word_amount, answer_index = 5):
    vocab = list(vocab)
    return vocab[random.randint(0, word_amount - 1)][answer_index]


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


def check_choice(vocab, current_index, choice, answer_index = 5):
    if choice == vocab[current_index][answer_index]:
        return False
    else:
        return True


def create_choices(request, answer_index = 5):
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
            # print(choices)
            choice_count += 1

    # check and insert the answer
    blank_index = find_blank_index(choices)
    choices[blank_index] = vocab[current_index][answer_index]
    print(choices)
    return choices


def check_result(answer, request):
    correct_answer = get_correct_answer(request)
    if answer == correct_answer:
        return True
    else:
        return False
    

def get_correct_answer(request, answer_index = 5):
    vocab = request.session[VOCAB_LIST]
    current_index = request.session[CURRENT_WORD_INDEX]
    return vocab[current_index][answer_index]


def get_vocab_by_part(request):
    vocab_list = []
    selected_mode = int(request.session[SELECTED_MODE])
    selected_main_menu = request.session[SELECTED_MAIN_MENU]
    vocab_by_user = []

    print(VOCAB_MENU)
    # get data from CSV
    df = pd.read_csv(CSVPATH)
    if selected_main_menu == VOCAB_MENU[1] or selected_main_menu == VOCAB_MENU[2] or selected_main_menu == VOCAB_MENU[4]:
        vocab_by_user = get_vocabulary_by_main_menu(request)

    else:
        selected_sub_menu = request.session[SELECTED_SUB_MENU]
        column = ""

        # check if main menu is cefr or part of speech
        if selected_main_menu == VOCAB_MENU[0]:
            column = "cefr"
        else:
            column = "part of speech"

        vocab_by_user = df[df[column] == selected_sub_menu].values.tolist()
    
    # create the loop to seperate part
    part = int(math.ceil(len(vocab_by_user) / selected_mode))
    start_index = 0

    for i in range(part):
        end_index = (i + 1) * selected_mode
        vocab_part = vocab_by_user[start_index:end_index]

        vocab_list.append(vocab_part)
        start_index = end_index

    return vocab_list