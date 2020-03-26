from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.contrib import messages
import bcrypt


# Create your views here.
def index(request):
    return render(request, "index.html")


def register(request):
    errors = User.objects.r_validator(request.POST)

    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v, extra_tags=k)
        return redirect("/")
    else:
        # hash password and then create
        hash_brown = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hash_brown,
            date_hired=request.POST['date_hired']
        )
        u = User.objects.last()
        request.session['userid'] = u.id
        return redirect("/dashboard")


def login(request):
    errors = User.objects.l_validator(request.POST)
    if len(errors) > 0:
        for k, v in errors.items():
            messages.error(request, v, extra_tags=k)
        return redirect("/")
    else:
        user = User.objects.get(email=request.POST['login_email'])
        request.session['userid'] = user.id
        return redirect("/dashboard")


def logout(request):
    request.session.clear()
    return redirect("/")


def dashboard(request):
    # if 'userid' not in request.session:
    #    return redirect("/")
    context = {
        "logged_in_user": User.objects.get(id=request.session['userid']),
        "items": Item.objects.all()
    }
    return render(request, "dashboard.html", context)


def create(request):
    if request.method == "GET":
        return render(request, "add.html")
    if request.method == "POST":
        # errors = Event.objects.create_validator(request.POST)
        # if len(errors) > 0:
        #     for key, value in errors.items():
        #         messages.error(request, value, extra_tags=key)
        #     return redirect("/create")  # this is a GET request
        # else:
        logged_in_user = User.objects.get(id=request.session['userid'])
        Item.objects.create(
            title=request.POST['title'],
            # description=request.POST['description'],
            creator=logged_in_user
        )
        #recent_item = Item.objects.last()
        #recent_item_creator = Item.creator.last()
        #recent_item.save()
        #recent_item.guests.add(recent_item_creator)

        return redirect("/dashboard")


def show(request, id):
    context = {
        "item": Item.objects.get(id=id),
        "logged": User.objects.get(id=request.session['userid']),
    }
    return render(request, "show.html", context)


# def edit(request, id):
#     if request.method == "GET":
#         context = {
#             "event": Item.objects.get(id=id)
#         }
#         return render(request, "edit.html", context)
#     if request.method == "POST":
# errors = Item.objects.create_validator(request.POST)
# if len(errors) > 0:
#     for key, value in errors.items():
#         messages.error(request, value, extra_tags=key)
#     return redirect(f"/edit/{id}")  # this is a GET request
# else:
# recent_item = Item.objects.get(id=id)
# recent_item.title = request.POST['title']
# recent_item.description = request.POST['description']
# recent_item.save()
# return redirect("/dashboard")


def delete(request, id):
    Item.objects.get(id=id).delete()
    return redirect("/dashboard")


def join(request, id):
    logged_in_user = User.objects.get(id=request.session['userid'])
    item = Item.objects.get(id=id)
    logged_in_user.attending_events.add(item)
    return redirect("/dashboard")


def cancel(request, id):
    logged_in_user = User.objects.get(id=request.session['userid'])
    item = Item.objects.get(id=id)
    logged_in_user.attending_events.remove(item)

    return redirect("/dashboard")


def validemail(request):
    print(request.POST['email'])
    if len(User.objects.filter(email=request.POST['email'])) == 0:
        return JsonResponse({"msg": "true"})
    else:
        return JsonResponse({"msg": "false"})


def validlogin(request):
    errors = User.objects.l_validator(request.POST)
    if len(errors) > 0:
        return render(request, "partial_email.html")
    else:
        print(request.POST)
        user = User.objects.get(email=request.POST['login_email'])
        request.session['userid'] = user.id
        return JsonResponse({"msg": "success"})
