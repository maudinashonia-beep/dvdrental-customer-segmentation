from django.urls import path

from dvdrental_prediction import admin_view
from . import views
from .views import search_result
from .views import customer_prediction_view, predict_customer
from .admin_view import retrain_model_view


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'), 
    path('movies/', views.movie_list, name='movie_list'), 
    path('movies/<int:film_id>/', views.movie_detail, name='movie_detail'),
    path('search/', search_result, name='search_result'),
    path('retrain-model/<int:model_id>/', admin_view.retrain_model_view, name='retrain_model'),
    path('predict_view/', customer_prediction_view, name='customer_prediction_view'),
    path('predict_customer/', predict_customer, name='predict_customer'),
    path('predict-segment/', views.predict_segment, name='predict_segment'),#baru 
]