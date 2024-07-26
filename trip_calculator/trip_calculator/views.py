from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from trip_calculator.imp import registration_controller, trip_controller
from django.contrib.auth import authenticate, login
from trip_calculator.imp.friend_controller import FriendController


# Create your views here.
person = {"name": 'Tomasz'}
trip = {"name": "Rumunia",
        "all_person": [{'name': 'Tomasz', 'lastname': 'Leśniak'}, {'name': 'Robert', 'lastname': 'Kromka'},
                       {'name': 'ff', 'lastname': 'tt'}, ]}
background = {
    'img_url': 'https://images.unsplash.com/photo-1500964757637-c85e8a162699?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzIyMjJ8MHwxfHNlYXJjaHwxfHxyYW5kb20lMjBuYXR1cmFsJTIwdmlld3xlbnwwfHx8fDE3MjA3MjU1MDV8MA&ixlib=rb-4.0.3&q=80&w=1080'}

person = {"friend": [{"name": "Katarzyna", "lastname": "testNowakowska", 'user_id':10}, {"name": "Test1", "lastname": "test2", 'user_id':2},
                     {"name": "Test1", "lastname": "test2", 'user_id':3}, {"name": "Test1", "lastname": "test2",  'user_id':4}]}

cost = {
    "any": True,
    "for_trip": [{
        "id": '36',
        "name": 'Rumunia',
        "totalCost": 123123,
        "balance": {"amount": 123, "positive": True},
        "costs": [
            {
                "name": 'Paliwo',
                "who_pay": {"name": 'Tomasz', "was_you": True},
                "cost": 123,
                "split_by": ['name1', 'name2'],
                "unit_cost": 12,
                "return": 123
            },
            {
                "name": 'Hotel',
                "who_pay": {"name": 'Elilia', "was_you": False},
                "cost": 123,
                "split_by": ['name1', 'name2'],
                "unit_cost": 12,
                "return": 123
            }
        ]
    },
        {
            "id": '37',
            "name": 'Polska',
            "totalCost": 1223,
            "balance": {"amount": 13, "positive": False},
            "costs": [
                {
                    "name": 'Hotel',
                    "who_pay": {"name": 'Emi', "was_you": False},
                    "cost": 1223,
                    "split_by": ['name3', 'name2'],
                    "unit_cost": 13572,
                    "return": 123453
                },
                {
                    "name": 'Hotel',
                    "who_pay": {"name": 'Emi', "was_you": False},
                    "cost": 12324,
                    "split_by": ['name1', 'name2'],
                    "unit_cost": 12754,
                    "return": 122343
                }
            ]
        }]

}


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


@login_required
def create_trip_view(request):
    menu = {"current_page": 'Create new trip'}
    if request.method == 'POST':
        trip_controller.add_trip(request.session.get('user_id'), request.POST)
        return redirect("home_view")

    return render(request, 'trip_calculator/create_trip.html',
              {'menu': menu, 'background': background,
               'person': FriendController(request.session.get('user_id')).get_Friend_list()})


@login_required
def invite_friend_view(request):
    menu = {"current_page": 'Invite friend'}
    if request.method == 'POST':
        registration_controller.invite_user(request.session.get('user_id'), request.POST)
        return redirect("home_view")

    return render(request, 'trip_calculator/addFriends.html', {'menu': menu, 'background': background})


@login_required
def add_cost_view(request, trip_id):
    menu = {"current_page": 'Add trip cost'}
    user_id = request.session.get('user_id')
    if request.method == 'POST':
        trip_controller.add_cost(user_id, trip_id, request.POST)
        return redirect("home_view")
    trip_squad = trip_controller.TripController().get_trip_squad(trip_id)
    trip_squad = list(filter(lambda item: item['user_id'] != user_id, trip_squad))
    return render(request, 'trip_calculator/add_cost.html', {'menu': menu, 'person': trip_squad, 'background': background})


@login_required
def home_view(request):
    menu = {"current_page": 'home view'}
    user_id = request.session.get('user_id')
    trip = trip_controller.get_all_trips_with_details(user_id)
    friend = FriendController(request.session.get('user_id')).get_Friend_list()


    user = {'name': 'Tomasz', 'lastname': 'Leśniak', 'email': 'tomasz1lesniak@gmail.com', 'added': '12-12-2023'}

    return render(request, 'trip_calculator/home_view.html',
                  {'cost': cost, 'menu': menu, 'trip_list': trip, 'friends_list': friend, 'user': user,
                   'person': person, 'background': background})
