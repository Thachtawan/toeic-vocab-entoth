from vocab_app import views
from django.urls import path

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('register', views.register),
    path('main_menu', views.main_menu),
    path('logout', views.log_out),
    path('select_menu', views.select_menu),
    path('select_menu_category', views.select_menu_category),
    path('practice_vocab', views.practice_vocab),
    path('start_practice', views.start_practice),
    path('check_answer', views.check_answer),
    path('next_question', views.next_question),
    path('show_result', views.show_result)
]