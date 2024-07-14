from django.urls import path

from trip_calculator import views

urlpatterns = [
    path('login/', views.login_page_view, name='login_view'),
    path('error_login/', views.error_login_page_view, name='error_login_view'),
    path('create_trip/', views.create_trip_view, name='create_trip_view'),
    path('invite_friend/', views.invite_friend_view, name='invite_friend_view'),
    # path('add_expense/', views.add_expense_view, name='add_expense_view')
]