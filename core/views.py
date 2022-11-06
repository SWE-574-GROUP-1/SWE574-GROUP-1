from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages

# Create your views here.
def index(request):
    # return HttpResponse('<h1>Welcome to LinkMe.</h2>')    
    return render(request, 'index.html')

def homepage(request):
    return render(request, 'homepage.html')

def register(request):
    return render(request, "signup.html")

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("core:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render(request=request, template_name="register.html", context={"register_form":form})
