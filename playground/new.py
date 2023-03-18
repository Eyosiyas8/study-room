from django.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
def loginForm(request):
    if request.method=="POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User Not Found!")
        
        user = authenticate(request, username=username, password=password)

        if user is not none:
            login()
        else:
            messages.error(request, "Username or Pasword is incorrect!")

  
