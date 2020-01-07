from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Messages
from .forms import LoginForm
from django.db.models import Q
from django.http import HttpResponse ,HttpResponseRedirect

def chat(request,uid="23"):
	return render(request,"chat.html",{})

# def conversations(request):
# 	return render(request,"conversations.html",{})

# def do(request):
# 	return render(request,"2.html",{})

def index(request):
    return render(request, 'index.html', {})

def room(request, room_name):
    return render(request, 'room.html', {
        'room_name': room_name
    })

def login_required_api(function):
	def wrapper(request, *args, **kw):
		if not request.user.is_authenticated:
			return HttpResponseRedirect("/bot/login")
		user = user.username 
		return function(request, user)
	return wrapper

@login_required_api
def sync_messages(request,user):
	data = json.loads(str(request.body,'utf-8'))
	target ,index ,messages = data['target'] ,data['index'] ,[]
	objects = Messages.objects.filter(Q(target=target,sender=user) | Q(target=sender,sender=target)).order_by('-timestamp').count(50)
	messages = [ [{"text":obj.text,"time":obj.create},"out" if obj.sender == sender else "in"] for obj in objects ]
	return HttpResponse(json.dumps(messages),content_type="application/json")



def login(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect("/chat")
	if request.method == 'POST':
		login_form = LoginForm(request.POST or None)
		if login_form.is_valid():
			username = login_form.cleaned_data['username']
			password = login_form.cleaned_data['password']
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request,user)
				return HttpResponseRedirect("/chat")
			else:
				return render(request, 'login.html', {'login': LoginForm(),"incorrect":True})
	return render(request, 'login.html', {'login': LoginForm()})