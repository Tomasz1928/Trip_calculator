from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from trip_calculator.imp import registration_controller
from django.contrib.auth import authenticate, login, logout
from trip_calculator.imp.friend_controller import FriendController
from trip_calculator.imp.trip_controller import get_user_TripController
from trip_calculator.imp import helper


def login_page_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.user_id
            return redirect('home_view')
        else:
            return render(request, 'trip_calculator/login.html', {'login': {'error': True}})
    else:
        return render(request, 'trip_calculator/login.html', {'login': {'error': False}})


def registration_view(request):
    registration = {'error': False}
    if request.GET:
        registration_pass = registration_controller.registration(request.GET)
        if registration_pass["registration_pass"]:
            return redirect("login_view")
        else:
            registration['error'] = True
            return render(request, 'trip_calculator/registration.html',
                          {"registration": registration})

    return render(request, 'trip_calculator/registration.html',
                  {"registration": registration})


def recovery_endpoint(request):
    registration_controller.recovery(request.GET)
    return redirect("login_view")


@login_required()
def logout_endpoint(request):
    logout(request)
    return redirect("login_view")


@login_required()
def edit_trip_endpoint(request):
    helper.manage_trip_action(request.session.get('user_id'), request.POST)
    response = HttpResponseRedirect(reverse("home_view"))
    response.set_cookie('home_page', 'trip', max_age=20)
    return response


@login_required()
def edit_friend_endpoint(request):
    FriendController(request.session.get('user_id')).delete_friend(request.GET['friend_id'])
    response = HttpResponseRedirect(reverse("home_view"))
    response.set_cookie('home_page', 'friend', max_age=20)
    return response


@login_required()
def edit_cost_endpoint(request):
    helper.manage_cost_action(request.session.get('user_id'), request.POST)
    response = HttpResponseRedirect(reverse("home_view"))
    trip_id = request.POST['trip_id']
    response.set_cookie('home_page', 'cost', max_age=20)
    response.set_cookie('trip_id', f'{trip_id}', max_age=20)
    return response


@login_required()
def edit_account_endpoint(request):
    registration_controller.update_account(request.session.get('user_id'), request.POST)
    response = HttpResponseRedirect(reverse("home_view"))
    response.set_cookie('home_page', 'account', max_age=20)
    return response


@login_required
def create_trip_view(request):
    menu = {"current_page": 'Create new trip'}
    if request.method == 'POST':
        helper.add_trip(request.session.get('user_id'), request.POST)
        return redirect("home_view")

    return render(request, 'trip_calculator/create_trip.html',
              {'menu': menu,
               'person': FriendController(request.session.get('user_id')).get_friend_list()})


@login_required
def invite_friend_view(request):
    menu = {"current_page": 'Invite friend'}
    if request.method == 'POST':
        registration_controller.invite_user(request.session.get('user_id'), request.POST)
        response = HttpResponseRedirect(reverse("home_view"))
        response.set_cookie('home_page', 'friend', max_age=20)
        return response

    return render(request, 'trip_calculator/addFriends.html', {'menu': menu})


@login_required
def add_cost_view(request, trip_id):
    menu = {"current_page": 'Add trip cost'}
    user_id = request.session.get('user_id')
    if request.method == 'POST':

        helper.add_cost(user_id, trip_id, request.POST)
        response = HttpResponseRedirect(reverse("home_view"))
        response.set_cookie('home_page', 'cost', max_age=20)
        response.set_cookie('trip_id', f'{trip_id}', max_age=20)
        return response

    instance = get_user_TripController(user_id)
    tripDetails = instance.get_info()
    trip_info = next((trip for trip in tripDetails if trip['trip_id'] == trip_id), None).get('squad')
    trip_squad = list(filter(lambda item: item['user_id'] != user_id, trip_info))
    return render(request, 'trip_calculator/add_cost.html', {'menu': menu, 'person': trip_squad})


@login_required
def home_view(request):
    user_id = request.session.get('user_id')
    user = registration_controller.get_user_infor(user_id)
    instance = get_user_TripController(user_id)
    tripDetails  = instance.get_info()

    userName = user['name']
    userLastname = user['lastname']
    menu = {"current_page": f'Hello {userName} {userLastname}'}

    friend = FriendController(user_id).get_friend_list()

    return render(request, 'trip_calculator/home_view.html',
                  {'menu': menu, 'friends_list': friend, 'user': user, 'allTripData':tripDetails})
