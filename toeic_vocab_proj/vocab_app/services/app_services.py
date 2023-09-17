from vocab_app.models import User
from ..constants.const_session_request import SUM_OF_CHECK, SUM_OF_NEXT, CHOICES, VOCAB_LIST, VOCAB_TYPE, VOCAB_CATEGORY
from ..constants.const_variable import CURRENT_WORD_INDEX, CORRECT_ANSWER, TOTAL_WORD, SELECTED_MAIN_MENU, \
    SELECTED_SUB_MENU, SELECTED_MODE, IS_FROM_SUB_MENU, SELECTED_PART


def service_register_user(_username, _password):
    # check if username if existed
    result = User.objects.filter(username=_username).exists()

    if result == True:
        print("You can't use this username.")
        return False
    else:
        user = User.objects.create(
            username = _username,
            password = _password
        )

        user.save()
        print("Create user success!")
        return True


def service_login(_username, _password):
    # check if username existed and password is corrected
    result = User.objects.filter(username=_username).exists()

    if result == True:
        user = User.objects.filter(username=_username)

        if _password == user.first().password:
            return True
        else:
            print("Password is incorrect!")
            return False
    else:
        print("Username is incorrect!")
        return False
    

def reset_session(request):
    request.session[CURRENT_WORD_INDEX] = 0
    request.session[TOTAL_WORD] = 0
    request.session[CORRECT_ANSWER] = 0
    request.session[SUM_OF_CHECK] = 0
    request.session[SUM_OF_NEXT] = 0
    request.session[CHOICES] = []
    request.session[VOCAB_LIST] = []
    request.session[VOCAB_TYPE] = ""
    request.session[VOCAB_CATEGORY] = ""
    request.session[SELECTED_MAIN_MENU] = ""
    request.session[SELECTED_SUB_MENU] = ""
    request.session[SELECTED_MODE] = ""
    request.session[SELECTED_PART] = ""
    request.session[IS_FROM_SUB_MENU] = False
    
