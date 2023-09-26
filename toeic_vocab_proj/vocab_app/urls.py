from vocab_app import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('logout', views.log_out),
    path('main_menu', views.main_menu),
    path('sub_menu', views.sub_menu),
    path('word_amount_menu', views.word_amount_menu),
    path('practice_vocab', views.practice_vocab),
    path('start_practice', views.start_practice),
    path('practice_section', views.practice_section),
    # path('check_answer', views.check_answer),
    # path('next_question', views.next_question),
    path('show_result', views.show_result)
]