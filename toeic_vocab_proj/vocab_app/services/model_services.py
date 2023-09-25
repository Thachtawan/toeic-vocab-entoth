from .calculation_services import calculate_progress
from ..constants.const_session_request import VOCAB_LIST, CHOICES, USERNAME
from ..constants.const_variable import CURRENT_WORD_INDEX, TOTAL_WORD, CORRECT_ANSWER, \
    VOCAB_MENU, CEFR_LEVEL, WORD_AMOUNT_MODE, SELECTED_MAIN_MENU, SELECTED_SUB_MENU, SELECTED_MENU, \
    SELECTED_PART
from .vocab_services import get_vocabulary_type, get_vocabulary_by_CEFR_lvl, get_vocabulary_length_by_type, \
    get_vocab_by_part, get_vocabulary_by_main_menu

def create_part_model(request):
    username = request.session[USERNAME]
    length = len(get_vocab_by_part(request))
    print(length)

    # create the list for part menu
    part_list = []
    for i in range(length):
        part_list.append(i + 1)

    model = {
        "username": username,
        "main_menu": request.session[SELECTED_MAIN_MENU],
        "sub_menu": request.session[SELECTED_SUB_MENU],
        "part_list": part_list
    }
    return model


def create_sub_menu_model(request):
    main_menu = request.session[SELECTED_MENU]
    username = request.session[USERNAME]
    model = {}
    if main_menu == VOCAB_MENU[0]:
        model = {
            "username": username,
            "menu_list": CEFR_LEVEL,
            "page": "select_sub_menu"
        }
    elif main_menu == VOCAB_MENU[3]:
        model = {
            "username": username,
            "menu_list": get_vocabulary_type(),
            "page": "select_sub_menu"
        }
    else:
        model = {
            "username": username,
            "menu_list": WORD_AMOUNT_MODE,
            "page": "select_mode",
            "vocab_length": len(get_vocabulary_by_main_menu(request))
        }
    print(model)
    return model


def create_mode_model(request):
    main_menu = request.session[SELECTED_MAIN_MENU]
    sub_menu = request.session[SELECTED_SUB_MENU]
    username = request.session[USERNAME]
    model = {}

    if main_menu == VOCAB_MENU[0]:
        vocab_length = len(get_vocabulary_by_CEFR_lvl(sub_menu))

        model = {
            "username": username,
            "menu_list": WORD_AMOUNT_MODE,
            "page": "select_mode",
            "vocab_length": vocab_length
        }
    elif main_menu == VOCAB_MENU[3]:
        vocab_length = get_vocabulary_length_by_type(sub_menu)

        model = {
            "username": username,
            "menu_list": WORD_AMOUNT_MODE,
            "page": "select_mode",
            "vocab_length": vocab_length
        }

    return model


def create_next_model(request):
    vocab = list(request.session[VOCAB_LIST])
    main_menu = request.session[SELECTED_MAIN_MENU]
    sub_menu = request.session[SELECTED_SUB_MENU]
    part = request.session[SELECTED_PART]
    current_index = request.session[CURRENT_WORD_INDEX]
    choices = request.session[CHOICES]
    username = request.session[USERNAME]

    # calculate progress
    progress = 0
    if current_index > 0:
        progress = calculate_progress(len(vocab), current_index)

    model = {
        "main_menu": main_menu.upper(),
        "sub_menu": sub_menu.upper(),
        "part": part,
        "question": vocab[current_index][2],
        "part_of_speech": vocab[current_index][3],
        "practice_status": "start",
        "choices": choices,
        "current_word": current_index + 1,
        "total_word": len(vocab),
        "username": username,
        "progress": progress,
        "is_answer": False
    }

    return model


def create_check_answer_model(request, status, answer, correct_answer):
    vocab = list(request.session[VOCAB_LIST])
    current_index = request.session[CURRENT_WORD_INDEX]
    choices = request.session[CHOICES]
    username = request.session[USERNAME]
    main_menu = request.session[SELECTED_MAIN_MENU]
    sub_menu = request.session[SELECTED_SUB_MENU]
    part = request.session[SELECTED_PART]

    # calculate progress
    progress = calculate_progress(len(vocab), current_index + 1)

    model = {
        "main_menu": main_menu.upper(),
        "sub_menu": sub_menu.upper(),
        "part": part,
        "question": vocab[current_index][2],
        "part_of_speech": vocab[current_index][3],
        "practice_status": "start",
        "choices": choices,
        "current_word": current_index + 1,
        "total_word": len(vocab),
        "username": username,
        "progress": progress,
        "is_answer": True,
        "is_correct": status,
        "answer": answer,
        "correct_answer": correct_answer
    }

    return model


def create_total_result_model(request):
    username = str(request.session[USERNAME])
    total_word = int(request.session[TOTAL_WORD])
    correct_amount = int(request.session[CORRECT_ANSWER])
    main_menu = request.session[SELECTED_MAIN_MENU]
    sub_menu = request.session[SELECTED_SUB_MENU]
    part = request.session[SELECTED_PART]

    # set the value
    wrong_amount = total_word - correct_amount
    accuracy = int((correct_amount / total_word) * 100)

    model = {
        "main_menu": main_menu.upper(),
        "sub_menu": sub_menu.upper(),
        "part": part,
        "total_word": total_word,
        "correct_amount": correct_amount,
        "wrong_amount": wrong_amount,
        "accuracy": accuracy,
        "username": username
    }

    return model