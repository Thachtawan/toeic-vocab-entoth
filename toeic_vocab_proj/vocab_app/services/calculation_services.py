def calculate_progress(total_word, total_answer):
    current_progress = int((total_answer / total_word) * 100)
    print("progress: " + str(current_progress))
    return current_progress