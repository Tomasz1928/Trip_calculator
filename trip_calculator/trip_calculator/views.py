from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from trip_calculator.imp import registration_controller, trip_controller, cost_controller
from django.contrib.auth import authenticate, login, logout
from trip_calculator.imp.friend_controller import FriendController

background = {
    'img_url': 'https://images.unsplash.com/photo-1500964757637-c85e8a162699?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzIyMjJ8MHwxfHNlYXJjaHwxfHxyYW5kb20lMjBuYXR1cmFsJTIwdmlld3xlbnwwfHx8fDE3MjA3MjU1MDV8MA&ixlib=rb-4.0.3&q=80&w=1080'}


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
            return render(request, 'trip_calculator/login.html', {'login': {'error': True}, 'background': background})
    else:
        return render(request, 'trip_calculator/login.html', {'login': {'error': False}, 'background': background})


def registration_view(request):
    registration = {'error': False}
    if request.GET:
        registration_pass = registration_controller.registration(request.GET)
        if registration_pass["registration_pass"]:
            return redirect("login_view")
        else:
            registration['error'] = True
            return render(request, 'trip_calculator/registration.html',
                          {"registration": registration, 'background': background})

    return render(request, 'trip_calculator/registration.html',
                  {"registration": registration, 'background': background})


def recovery_endpoint(request):
    registration_controller.recovery(request.GET)
    return redirect("login_view")


@login_required()
def logout_endpoint(request):
    logout(request)
    return redirect("login_view")


@login_required()
def edit_friend_endpoint(request):
    FriendController(request.session.get('user_id')).delete_friend(request.GET['friend_id'])
    response = HttpResponseRedirect(reverse("home_view"))
    response.set_cookie('home_page', 'friend', max_age=3)
    return response


@login_required()
def edit_cost_endpoint(request):
    cost_controller.costStatusUpdate(request.POST)
    response = HttpResponseRedirect(reverse("home_view"))
    response.set_cookie('home_page', 'cost', max_age=3)
    response.set_cookie('trip_id', f'{request.POST['trip_id']}', max_age=3)
    return response


@login_required()
def edit_account_endpoint(request):
    registration_controller.update_account(request.session.get('user_id'), request.POST)
    response = HttpResponseRedirect(reverse("home_view"))
    response.set_cookie('home_page', 'account', max_age=3)
    return response


@login_required
def create_trip_view(request):
    menu = {"current_page": 'Create new trip'}
    if request.method == 'POST':
        trip_controller.add_trip(request.session.get('user_id'), request.POST)
        return redirect("home_view")

    return render(request, 'trip_calculator/create_trip.html',
              {'menu': menu, 'background': background,
               'person': FriendController(request.session.get('user_id')).get_friend_list()})


@login_required
def invite_friend_view(request):
    menu = {"current_page": 'Invite friend'}
    if request.method == 'POST':
        registration_controller.invite_user(request.session.get('user_id'), request.POST)
        response = HttpResponseRedirect(reverse("home_view"))
        response.set_cookie('home_page', 'friend', max_age=3)
        return response

    return render(request, 'trip_calculator/addFriends.html', {'menu': menu, 'background': background})


@login_required
def add_cost_view(request, trip_id):
    menu = {"current_page": 'Add trip cost'}
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        cost_controller.add_cost(user_id, trip_id, request.POST)
        response = HttpResponseRedirect(reverse("home_view"))
        response.set_cookie('home_page', 'cost', max_age=3)
        response.set_cookie('trip_id', f'{trip_id}', max_age=3)
        return response

    trip_squad = trip_controller.TripController().get_trip_squad(trip_id)
    trip_squad = list(filter(lambda item: item['user_id'] != user_id, trip_squad))
    return render(request, 'trip_calculator/add_cost.html', {'menu': menu, 'person': trip_squad, 'background': background})


@login_required
def home_view(request):
    menu = {"current_page": 'Home view'}
    user_id = request.session.get('user_id')
    trip = trip_controller.get_all_trips_with_details(user_id)
    friend = FriendController(user_id).get_friend_list()
    costs = cost_controller.get_all_cost_details(user_id)
    user = registration_controller.get_user_infor(user_id)

    return render(request, 'trip_calculator/home_view.html',
                  {'cost': costs, 'menu': menu, 'trip_list': trip, 'friends_list': friend, 'user': user, 'background': background})
