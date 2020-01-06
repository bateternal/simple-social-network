from django.shortcuts import render

# def chat(request,uid="23"):
# 	return render(request,"chat.html",{})

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


