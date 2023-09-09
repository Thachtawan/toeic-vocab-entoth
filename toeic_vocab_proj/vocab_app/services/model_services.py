from .calculation_services import calculate_progress
from ..constants.const_session_request import VOCAB_LIST, VOCAB_TYPE, CHOICES, USERNAME, VOCAB_CATEGORY
from ..constants.const_variable import CURRENT_WORD_INDEX, TOTAL_WORD, CORRECT_ANSWER


def create_next_model(request):
    vocab = list(request.session[VOCAB_LIST])
    selected_type = str(request.session[VOCAB_TYPE])
    current_index = request.session[CURRENT_WORD_INDEX]
    choices = request.session[CHOICES]
    username = request.session[USERNAME]

    # calculate progress
    progress = 0
    if current_index > 0:
        progress = calculate_progress(len(vocab), current_index)

    model = {
        "selected_type": selected_type.upper(),
        "question": vocab[current_index][2],
        "practice_status": "start",
        "choices": choices,
        "synonyms": vocab[current_index][5],
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
    selected_type = str(request.session[VOCAB_TYPE])

    # calculate progress
    progress = calculate_progress(len(vocab), current_index + 1)

    model = {
        "selected_type": selected_type.upper(),
        "question": vocab[current_index][2],
        "practice_status": "start",
        "choices": choices,
        "synonyms": vocab[current_index][5],
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
    word_type = str(request.session[VOCAB_TYPE])
    category = str(request.session[VOCAB_CATEGORY])
    total_word = int(request.session[TOTAL_WORD])
    correct_amount = int(request.session[CORRECT_ANSWER])

    # set the value
    wrong_amount = total_word - correct_amount
    accuracy = int((correct_amount / total_word) * 100)

    model = {
        "word_type": word_type.upper(),
        "category": category,
        "total_word": total_word,
        "correct_amount": correct_amount,
        "wrong_amount": wrong_amount,
        "accuracy": accuracy,
        "username": username
    }

    return model