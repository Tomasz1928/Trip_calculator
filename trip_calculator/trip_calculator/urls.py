from django.urls import path

from trip_calculator import views

urlpatterns = [
    path('login/', views.login_page_view, name='login_view'),
    path('logout/', views.logout_endpoint, name='logout_endpoint'),
    path('edit_friend/', views.edit_friend_endpoint, name='edit_friend_endpoint'),
    path('registration/', views.registration_view, name='registration_view'),
    path('recovery/', views.recovery_endpoint, name='recovery_endpoint'),
    path('create_trip/', views.create_trip_view, name='create_trip_view'),
    path('invite_friend/', views.invite_friend_view, name='invite_friend_view'),
    path('add_cost/TripId=<int:trip_id>/', views.add_cost_view, name='add_cost_view'),
    path('home/', views.home_view, name='home_view'),
    # path('add_expense/', views.add_expense_view, name='add_expense_view')
]