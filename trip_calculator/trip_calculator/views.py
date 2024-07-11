from django.shortcuts import render

# Create your views here.
person = {"name": 'Tomasz'}
trip = {"name": "Rumunia","all_person": [{'name':'Tomasz', 'lastname':'Leśniak'},{'name':'Robert', 'lastname':'Kromka'}, {'name':'ff', 'lastname':'tt'},] }
login = {"error": False}
background ={'img_url':'https://images.unsplash.com/photo-1500964757637-c85e8a162699?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzIyMjJ8MHwxfHNlYXJjaHwxfHxyYW5kb20lMjBuYXR1cmFsJTIwdmlld3xlbnwwfHx8fDE3MjA3MjU1MDV8MA&ixlib=rb-4.0.3&q=80&w=1080' }


def login_page_view(request):
    return render(request, 'trip_calculator/login_page/login.html', {'login': login, 'background': background})


def error_login_page_view(request):
    return render(request, 'trip_calculator/login_page/login.html', {'login': login, 'background': background})


def add_expense_view(request):
    pass