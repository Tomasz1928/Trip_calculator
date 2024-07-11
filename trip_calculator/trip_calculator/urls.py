from django.urls import path

from trip_calculator import views

urlpatterns = [
    path('login/', views.login_page_view, name='login_view'),
    path('error_login/', views.error_login_page_view, name='error_login_view'),
    # path('home/', views.home_view, name='home_view'),
    # path('add_expense/', views.add_expense_view, name='add_expense_view')
]