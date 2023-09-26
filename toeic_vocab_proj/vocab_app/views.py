from django.shortcuts import render, redirect
from .services.app_services import service_login, service_register_user, reset_session, get_session_for_practice_section
from .services.vocab_services import get_vocabulary, create_choices, check_result, get_correct_answer
from .services.model_services import create_next_model, create_check_answer_model, create_total_result_model, \
    create_sub_menu_model, create_mode_model, create_part_model
from .constants.const_path import MAIN_MENU, SUB_MENU, WORD_AMOUNT_MENU, PRACTICE_VOCAB, SHOW_RESULT, \
    PRACTICE_SECTION
from .constants.const_session_request import USERNAME, PASSWORD, PASSWORD_2, MENU, VOCAB_LIST, CHOICE, \
    CHOICES, SUM_OF_CHECK, SUM_OF_NEXT, PAGE, PRACTICE_STATUS
from .constants.const_template import HOME_TP, FORM_TP, MAINMENU_TP, SUB_MENU_TP, PRACTICE_TP, \
    PT_VOCAB_TP, RESULT_TP, PART_MENU_TP
from .constants.cosnt_action import LOGIN, REGISTER
from .constants.const_variable import TOTAL_WORD, CORRECT_ANSWER, CURRENT_WORD_INDEX, \
    VOCAB_MENU, SELECTED_MAIN_MENU, SELECTED_SUB_MENU, SELECTED_MODE, SELECTED_MENU, \
    SELECTED_PART, IS_FROM_SUB_MENU


def index(request):
    try:
        if request.session[USERNAME] != "":
            return redirect(MAIN_MENU)
    
        request.session[USERNAME] = ""
        return render(request, HOME_TP)
    except:
        request.session[USERNAME] = ""
        return render(request, HOME_TP)


def login(request):
    if request.method == "POST":
        # Receive user data
        username = request.POST[USERNAME]
        password = request.POST[PASSWORD]

        # check if username and password is valid
        result = service_login(username, password)
        if result == True:
            request.session[USERNAME] = username
            return redirect(MAIN_MENU)
        else:
            model = {
                "action": LOGIN,
                "status": "fail"
            }
            return render(request, FORM_TP, model)
    else:
        model = {
            "action": LOGIN
        }
        return render(request, FORM_TP, model)


def register(request):
    if request.method == "POST":
        # Receive user data
        username = request.POST[USERNAME]
        password = request.POST[PASSWORD]
        confirm_password = request.POST[PASSWORD_2]

        # check if password is correct
        if password != confirm_password:
            model = {
                "action": REGISTER,
                "status": "fail_1"
            }
            return render(request, FORM_TP, model)

        # check if username and password is valid
        result = service_register_user(username, password)
        if result == True:
            return redirect("/")
        else:
            model = {
                "action": REGISTER,
                "status": "fail_2"
            }
            return render(request, FORM_TP, model)
    
    else:
        model = {
            "action": REGISTER
        }
        return render(request, FORM_TP, model)


def log_out(request):
    request.session[USERNAME] = ""
    return redirect("/")


def main_menu(request):
    if request.method == "GET":
        # reset all vocab session
        reset_session(request)

        # get username to use on display
        username = request.session[USERNAME]
        request.session[PAGE] = "select_type"

        model = {
            "username": username,
            "menu_list": VOCAB_MENU
        }
        return render(request, MAINMENU_TP, model)
    
    else: # POST
        selected_main_menu = request.POST[MENU]
        request.session[SELECTED_MENU] = request.POST[MENU]
        request.session[SELECTED_MAIN_MENU] = selected_main_menu
        return redirect(SUB_MENU)


def sub_menu(request):
    if request.method == "GET":
        model = create_sub_menu_model(request)
        print(model)
        return render(request, SUB_MENU_TP, model)
    else:
        request.session[SELECTED_SUB_MENU] = request.POST[MENU]
        model = create_mode_model(request)
        print(model)

        # check if the word amount is less than 100
        if model["vocab_length"] < 100:
            request.session[IS_FROM_SUB_MENU] = True
            return redirect(PRACTICE_VOCAB)
        else:
            return redirect(WORD_AMOUNT_MENU)
        

def word_amount_menu(request):
    if request.method == "GET":
        model = create_mode_model(request)
        return render(request, SUB_MENU_TP, model)
    else:
        request.session[SELECTED_MODE] = request.POST[MENU]
        print(request.session[SELECTED_MODE])
        model = create_part_model(request)
        print(model)

        return render(request, PART_MENU_TP, model)


def practice_vocab(request):
    # check if this function is invoked from submenu directly
    if request.session[IS_FROM_SUB_MENU] == False:
        request.session[SELECTED_PART] = request.POST[MENU]

    vocab = get_vocabulary(request)
    word_amount = len(vocab)

    # add vocab value to the session
    request.session[VOCAB_LIST] = vocab
    request.session[TOTAL_WORD] = word_amount

    model = {
        "vocab": vocab,
        "word_amount": word_amount,
        "main_menu": request.session[SELECTED_MAIN_MENU],
        "sub_menu": request.session[SELECTED_SUB_MENU],
        "part": request.session[SELECTED_PART],
        "username": request.session[USERNAME]
    }
    return render(request, PRACTICE_TP, model)


def start_practice(request):
    # reset the session for practice section
    get_session_for_practice_section(request)

    # create choices
    choices = create_choices(request)
    request.session[CHOICES] = choices
    request.session[PRACTICE_STATUS] = "first_question"

    return redirect(PRACTICE_SECTION)


def practice_section(request):
    # check if this is the first question
    if request.session[PRACTICE_STATUS] == "first_question":
        # render the first question
        next_model = create_next_model(request)
        request.session[PRACTICE_STATUS] = "continue_practice"
        return render(request, PT_VOCAB_TP, next_model)

    # check answer
    if request.method == "POST":
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
        return render(request, PT_VOCAB_TP, check_model)
    
    # next question
    if request.method == "GET":
        # get current_index value
        sum_check = request.session[SUM_OF_CHECK]
        sum_next = request.session[SUM_OF_NEXT]

        # prevent in case of refreshing page or press f5
        if sum_check == sum_next:
            next_model = create_next_model(request)
            return render(request, PT_VOCAB_TP, next_model)

        else:
            # update the current index
            request.session[CURRENT_WORD_INDEX] += 1

            # prevent word_index from out of range error
            if request.session[CURRENT_WORD_INDEX] > request.session[TOTAL_WORD]:
                request.session[CURRENT_WORD_INDEX] = request.session[TOTAL_WORD]
                return redirect(SHOW_RESULT)

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
                return render(request, PT_VOCAB_TP, next_model)
        

def show_result(request):
    result_model = create_total_result_model(request)
    return render(request, RESULT_TP, result_model)