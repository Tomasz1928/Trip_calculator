from django.shortcuts import render, redirect

# Create your views here.
person = {"name": 'Tomasz'}
trip = {"name": "Rumunia","all_person": [{'name':'Tomasz', 'lastname':'Leśniak'},{'name':'Robert', 'lastname':'Kromka'}, {'name':'ff', 'lastname':'tt'},] }
background ={'img_url':'https://images.unsplash.com/photo-1500964757637-c85e8a162699?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=M3w2MzIyMjJ8MHwxfHNlYXJjaHwxfHxyYW5kb20lMjBuYXR1cmFsJTIwdmlld3xlbnwwfHx8fDE3MjA3MjU1MDV8MA&ixlib=rb-4.0.3&q=80&w=1080' }

person= {"frend_gr1":[{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"}],
"frend_gr3":[{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"},{"name":"Test1", "lastname":"test2"}]
         }


def login_page_view(request):
    login = {"error": False}
    return render(request, 'trip_calculator/login.html', {'login': login, 'background': background})



def error_login_page_view(request):
    login = {"error": True}
    return render(request, 'trip_calculator/login.html', {'login': login, 'background': background})



def create_trip_view(request):
    menu = {"current_page": 'Create new trip'}
    if request.method == 'POST':
        return redirect('login_view')
    return render(request, 'trip_calculator/create_trip.html', {'menu': menu, 'person': person, 'background': background})


def invite_friend_view(request):
    menu = {"current_page": 'Invite new friend'}
    return render(request, 'trip_calculator/addFriends.html', {'menu': menu, 'background': background})