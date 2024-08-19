from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from trip_calculator.imp import helper


def login_page_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home_view')
        else:
            return render(request, 'trip_calculator/login.html', {'login': {'error': True}})
    else:
        return render(request, 'trip_calculator/login.html', {'login': {'error': False}})


def registration_view(request):
    registration = {'error': False}
    if request.GET:
        registration_pass = helper.manage_account_action(request.GET, action='register')
        if registration_pass["registration_pass"]:
            return redirect("login_view")
        else:
            registration['error'] = True
            return render(request, 'trip_calculator/registration.html',
                          {"registration": registration})

    return render(request, 'trip_calculator/registration.html',
                  {"registration": registration})


def recovery_endpoint(request):
    helper.manage_account_action(request.GET, action='recovery')
    return redirect("login_view")


@login_required()
def logout_endpoint(request):
    logout(request)
    return redirect("login_view")


@login_required()
def edit_trip_endpoint(request):
    helper.manage_trip_action(request.user.user_id, request.POST)
    response = HttpResponseRedirect(reverse("home_view"))
    response.set_cookie('home_page', 'trip', max_age=20)
    return response


@login_required()
def edit_friend_endpoint(request):
    helper.manage_friend_action(user_id=request.user.user_id, friend_id= request.GET['friend_id'], action='delete')
    response = HttpResponseRedirect(reverse("home_view"))
    response.set_cookie('home_page', 'friend', max_age=20)
    return response


@login_required()
def edit_cost_endpoint(request):
    helper.manage_cost_action(request.user.user_id, request.POST)
    response = HttpResponseRedirect(reverse("home_view"))
    trip_id = request.POST['trip_id']
    response.set_cookie('home_page', 'cost', max_age=20)
    response.set_cookie('trip_id', f'{trip_id}', max_age=20)
    return response


@login_required()
def edit_account_endpoint(request):
    helper.manage_account_action(request.POST, request.user.user_id, action='update')
    response = HttpResponseRedirect(reverse("home_view"))
    response.set_cookie('home_page', 'account', max_age=20)
    return response


@login_required
def create_trip_view(request):
    if request.method == 'POST':
        helper.add_trip(request.user.user_id, request.POST)
        return redirect("home_view")
    person = helper.manage_friend_action(user_id=request.user.user_id, action='friend_list')
    return render(request, 'trip_calculator/create_trip.html', {'person':person})


@login_required
def invite_friend_view(request):
    if request.method == 'POST':
        helper.manage_friend_action(request.POST, user_id=request.user.user_id, action='add')
        response = HttpResponseRedirect(reverse("home_view"))
        response.set_cookie('home_page', 'friend', max_age=20)
        return response

    return render(request, 'trip_calculator/addFriends.html')


@login_required
def add_cost_view(request, trip_id):
    user_id = request.user.user_id

    if request.method == 'POST':
        helper.add_cost(user_id, trip_id, request.POST)
        response = HttpResponseRedirect(reverse("home_view"))
        response.set_cookie('home_page', 'cost', max_age=20)
        response.set_cookie('trip_id', f'{trip_id}', max_age=20)
        return response

    tripDetails = helper.manage_trip_action(user_id, {'action':'details'})
    trip_info = next((trip for trip in tripDetails if trip['trip_id'] == trip_id), None).get('squad')
    trip_squad = list(filter(lambda item: item['user_id'] != user_id, trip_info))

    return render(request, 'trip_calculator/add_cost.html', {'person': trip_squad})


@login_required
def home_view(request):
    tripDetails = helper.manage_trip_action(request.user.user_id, {'action': 'details'})
    friend = helper.manage_friend_action(user_id=request.user.user_id, action='friend_list')
    user = helper.manage_account_action('',request.user.user_id, action='info')
    return render(request, 'trip_calculator/home_view.html',
                  {'user': user, 'friends_list': friend, 'allTripData':tripDetails})
