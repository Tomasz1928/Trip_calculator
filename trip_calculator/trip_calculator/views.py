from django.shortcuts import render, redirect
from trip_calculator.imp.email_controler import *



# Create your views here.
person = {"name": 'Tomasz'}
trip = {"name": "Rumunia","all_person": [{'name':'Tomasz', 'lastname':'Leśniak'},{'name':'Robert', 'lastname':'Kromka'}, {'name':'ff', 'lastname':'tt'},] }
background ={'img_url':'https://images.unsplash.com/photo-1500964757637-c85e8a162699?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzIyMjJ8MHwxfHNlYXJjaHwxfHxyYW5kb20lMjBuYXR1cmFsJTIwdmlld3xlbnwwfHx8fDE3MjA3MjU1MDV8MA&ixlib=rb-4.0.3&q=80&w=1080' }

person= {"friend":[{"name":"Katarzyna", "lastname":"testNowakowska"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},
{"name":"Katarzyna", "lastname":"testNowakowska"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"}]}

cost = {
    "any": True,
    "for_trip": [{
        "id":'123',
        "name": 'Rumunia',
        "totalCost": 123123,
        "balance": { "amount": 123, "positive": True },
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
                "who_pay": { "name": 'Elilia', "was_you": False},
                "cost": 123,
                "split_by": ['name1', 'name2'],
                "unit_cost": 12,
                "return": 123
            }
        ]
    },
    {
        "id":'1233',
        "name": 'Polska',
        "totalCost": 1223,
        "balance": {"amount": 13, "positive": False},
        "costs": [
            {
                "name": 'Hotel',
                "who_pay": { "name": 'Emi', "was_you": False},
                "cost": 1223,
                "split_by": ['name3', 'name2'],
                "unit_cost": 13572,
                "return": 123453
            },
            {
                "name": 'Hotel',
                "who_pay": { "name": 'Emi', "was_you": False},
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
        login = {"error": True}
        return render(request, 'trip_calculator/login.html', {'login': login, 'background': background})

    login = {"error": False}
    return render(request, 'trip_calculator/login.html', {'login': login, 'background': background})


def registration_view(request):

    if request.GET:
        registration = {"error": True}
        return render(request, 'trip_calculator/registration.html',
                      {'registration': registration, 'background': background})

    registration = {"error": False}
    return render(request, 'trip_calculator/registration.html', {'registration': registration, 'background': background})


def create_trip_view(request):
    menu = {"current_page": 'Create new trip'}
    if request.method == 'POST':
        return redirect('login_view')
    return render(request, 'trip_calculator/create_trip.html', {'menu': menu, 'person': person, 'background': background})


def invite_friend_view(request):
    send_email = InvitationEmailSender()
    send_email.set_password('Hasłoxxx1')
    send_email.set_email('tomasz1928l@gmail.com')
    send_email.generate_invitation_message()
    # send_email.send_email()
    menu = {"current_page": 'Invite friend'}
    return render(request, 'trip_calculator/addFriends.html', {'menu': menu, 'background': background})


def add_cost_view(request):
    menu = {"current_page": 'Add trip cost'}
    return render(request, 'trip_calculator/add_cost.html', {'menu': menu,'person': person, 'background': background})


def home_view(request):
    menu = {"current_page": 'home view'}
    trip  = [{'name':'Rumunia','description':'Jedziemy do Rumuni pozwiedzać zamek drakuli', 'cost':'1561 zł','squad':[{'name':'Tomasz'},{'name':'Adam'},{'name':'Emi'}]},
             {'name':'Bługaria','description':'Jedziemy do Bługari nad morze', 'cost':'12561 zł','squad':[{'name':'Adam'},{'name':'Adam'},{'name':'Łukasz'}]}]

    trip = [{'name': 'Rumunia', 'description': 'Jedziemy do Rumuni pozwiedzać zamek drakuli', 'cost': '1561 zł',
             'squad': [{'name': 'Tomasz'}, {'name': 'Adam'}, {'name': 'Emi'}]},
            {'name': 'Bługaria', 'description': 'Jedziemy do Bługari nad morze', 'cost': '12561 zł',
             'squad': [{'name': 'Adam'}, {'name': 'Adam'}, {'name': 'Łukasz'}]}]

    friend = [{'name':'Tomasz', 'lastname':'Leśniak','added':'12.03.2024', 'trips':[{'name':'Rumunia'}, {'name':'Bługaria'}]},
              {'name':'Adam', 'lastname':'Markowski','added':'12.03.2023', 'trips':[]}]


    user= {'name':'Tomasz', 'lastname':'Leśniak', 'email':'tomasz1lesniak@gmail.com', 'added':'12-12-2023'}






    return render(request, 'trip_calculator/home_view.html', {'cost': cost, 'menu': menu,'trip_list':trip,'friends_list':friend,'user':user, 'person': person, 'background': background})