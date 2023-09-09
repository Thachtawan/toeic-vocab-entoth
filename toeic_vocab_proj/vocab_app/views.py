from django.shortcuts import render, redirect
from .services.app_services import service_login, service_register_user, reset_session
from .services.vocab_services import get_vocabulary_type, get_vocabulary, get_vocabulary_length_by_type, create_choices, check_result, get_correct_answer
from .services.model_services import create_next_model, create_check_answer_model, create_total_result_model
from .constants.const_path import MAIN, PRACTICE_VOCAB, SHOW_RESULT
from .constants.const_session_request import USERNAME, PASSWORD, MENU, VOCAB_TYPE, VOCAB_CATEGORY, VOCAB_LIST, CHOICE, CHOICES, SUM_OF_CHECK, SUM_OF_NEXT, PAGE
from .constants.const_template import HOME, FORM, MAINMENU, PRACTICE, PT_VOCAB, RESULT
from .constants.cosnt_action import LOGIN, REGISTER
from .constants.const_variable import TOTAL_WORD, CORRECT_ANSWER, CURRENT_WORD_INDEX, VOCAB_CATEGORIES


def index(request):
    try:
        if request.session[USERNAME] != "":
            return redirect(MAIN)
    
        request.session[USERNAME] = ""
        return render(request, HOME)
    except:
        request.session[USERNAME] = ""
        return render(request, HOME)

def login(request):
    if request.method == "POST":
        # Receive user data
        username = request.POST[USERNAME]
        password = request.POST[PASSWORD]

        # check if username and password is valid
        result = service_login(username, password)
        if result == True:
            request.session[USERNAME] = username
            return redirect(MAIN)
        else:
            model = {
                "action": LOGIN,
                "status": "fail"
            }
            return render(request, FORM, model)
    else:
        model = {
            "action": LOGIN
        }
        return render(request, FORM, model)


def register(request):
    if request.method == "POST":
        # Receive user data
        username = request.POST[USERNAME]
        password = request.POST[PASSWORD]

        # check if username and password is valid
        result = service_register_user(username, password)
        if result == True:
            return redirect("/")
        else:
            model = {
                "action": REGISTER,
                "status": "fail"
            }
            return render(request, FORM, model)
    
    else:
        model = {
            "action": REGISTER
        }
        return render(request, FORM, model)


def log_out(request):
    request.session[USERNAME] = ""
    return redirect("/")


def main_menu(request):
    # reset all vocab session
    reset_session(request)

    # get username to use on display
    username = request.session[USERNAME]
    request.session[PAGE] = "select_type"

    # get category from the csv vocabulary file
    word_type = get_vocabulary_type()
    print(word_type)

    model = {
        "username": username,
        "menu_list": word_type
    }
    return render(request, MAINMENU, model)


def select_menu(request):
    selected_type = request.POST[MENU]

    request.session[VOCAB_TYPE] = selected_type
    print(request.session[VOCAB_TYPE])

    # check if vocab length is larger than 100
    vocab_length = get_vocabulary_length_by_type(selected_type)
    print(vocab_length)
    if vocab_length > 100:
        username = request.session[USERNAME]
        request.session[PAGE] = "select_category"

        model = {
            "username": username,
            "menu_list": VOCAB_CATEGORIES,
            "page": "select_category"
        }
        return render(request, MAINMENU, model)
    else:
        request.session[VOCAB_CATEGORY] = ""
        return redirect(PRACTICE_VOCAB)


def select_menu_category(request):
    selected_category = request.POST[MENU]
    request.session[VOCAB_CATEGORY] = selected_category
    return redirect(PRACTICE_VOCAB)


def practice_vocab(request):
    vocab = get_vocabulary(request)
    word_amount = len(vocab)

    # add vocab value to the session
    request.session[VOCAB_LIST] = vocab
    request.session[TOTAL_WORD] = word_amount

    model = {
        "vocab": vocab,
        "word_amount": word_amount,
        "type": request.session[VOCAB_TYPE],
        "category": request.session[VOCAB_CATEGORY],
        "username": request.session[USERNAME]
    }
    return render(request, PRACTICE, model)


def start_practice(request):
    # create choices
    choices = create_choices(request)
    request.session[CHOICES] = choices

    # username = request.session[USERNAME]
    next_model = create_next_model(request)
    return render(request, PT_VOCAB, next_model)


def check_answer(request):
    # get answer
    answer = request.POST[CHOICE]

    # check if the result is correct
    result = check_result(answer, request)
    correct_answer = get_correct_answer(request)

    # update page index
    request.session[SUM_OF_CHECK] += 1

    # check if this is from refresh
    if (request.session[SUM_OF_CHECK] - request.session[SUM_OF_NEXT]) > 1:
        request.session[SUM_OF_CHECK] -= 1

    else:
        # update scores
        if result == True: 
            request.session[CORRECT_ANSWER] += 1

    check_model = create_check_answer_model(request, result, answer, correct_answer)
    return render(request, PT_VOCAB, check_model)
    

def next_question(request):
    # get current_index value
    sum_check = request.session[SUM_OF_CHECK]
    sum_next = request.session[SUM_OF_NEXT]

    # prevent in case of refreshing page or press f5
    if sum_check == sum_next:
        next_model = create_next_model(request)
        return render(request, PT_VOCAB, next_model)

    else:
        # update the current index
        request.session[CURRENT_WORD_INDEX] += 1

        # check if this is the last word
        if request.session[CURRENT_WORD_INDEX] == request.session[TOTAL_WORD]:
            return redirect(SHOW_RESULT)

        else:
            # create choices
            choices = create_choices(request)
            request.session[CHOICES] = choices

            # update page index
            request.session[SUM_OF_NEXT] += 1

            # create the next question model
            next_model = create_next_model(request)
            return render(request, PT_VOCAB, next_model)
        

def show_result(request):
    result_model = create_total_result_model(request)
    return render(request, RESULT, result_model)