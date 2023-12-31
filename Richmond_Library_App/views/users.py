from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from Richmond_Library_App.models import User

class UsersPage(View):
    def get(self, request):
        if get_user_status(request) != 'admin':
            return redirect('/home/')
        
        # Gets list of all users and passes it to the user page
        users = User.objects.all()
        return render(request, "users.html", {'users': users, 'status': get_user_status(request)})
    
class EditUser(View):
    # def get(self, request, user):
    #     # Passes the user received from pressing edit button to the edit page
    #     return render(request, "edituser.html", {'user': user})

    def get(self, request, _username):
        # Passes the user received from pressing edit button to the edit page
        user = User.objects.get(username=_username)
        return render(request, "edituser.html", {'user': user, 'status': get_user_status(request)})
    
    def post(self, request, **kwargs):
        user = User.objects.get(username=kwargs["_username"])
        # user.username = request.POST.get("_username")
        user.email = request.POST.get("_email")
        if not request.POST.get("_password"):
            user.password = user.password
        else:
            user.password = make_password(request.POST.get("_password"))
        user.user_type=request.POST.get("_user_type")
        user.save()


        # Need to get all of the users after editing the user info
        users = User.objects.all()
        return render(request, "users.html", {"users": users, 'status': get_user_status(request)})
    
    # def post(self, request):
    #     User.objects.create(
    #         username=request.POST.get("username"),
    #         password=request.POST.get("password"),
    #         name=request.POST.get("name"),
    #         email=request.POST.get("email"),
    #         user_type=request.POST.get("user_type")
    #     )
    #     users = User.objects.all()
    #     return render(request, "users.html", {'users': users})

def get_user_status(request):
    user = User.objects.get(username=request.user.username)
    return user.user_type