from django.shortcuts import render, redirect
from .models import User ,Job
from django.contrib import messages
import bcrypt
from datetime import date
# Create your views here.


def index(request):
    if 'uid' in request.session:
        return redirect("/dashboard")
    return render(request, "index.html")

def dashboard(request):
    if 'uid' not in request.session:
        return redirect("/")
    context = {
        "user": User.objects.get(id=request.session['uid']),
        "all_users": User.objects.all(),
        "all_jobs": Job.objects.all().order_by("-created_at") ,
    }
    return render(request, "dashboard.html", context)

def new_job(request):
    if 'uid' not in request.session:
        return redirect("/")
    context = {
        "user": User.objects.get(id=request.session['uid'])
    }
    return render(request, "new_job.html",context)

def create_job(request):
    if "cancel" in request.POST:
        return redirect("/dashboard")
    if request.method == "POST":
        errors = Job.objects.job_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("errors have been found")
            return redirect("/jobs/new")
        Job.objects.create(
            title=request.POST['title'],
            description=request.POST['desc'],
            location=request.POST['location'],
            posted_by=User.objects.get(id=request.session['uid']),
            category=request.POST.getlist('category'),
        )
        print("new job has been created")
    return redirect("/dashboard")

def register(request):
    if request.method == "POST":
        errors = User.objects.register_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(
            password.encode(), bcrypt.gensalt()).decode()  # create the hash
        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=pw_hash)
        request.session['uid'] = new_user.id
        return redirect("/dashboard")  # never render on a post, always redirect!


def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        logged_user = User.objects.get(email=request.POST['email'])
        request.session['uid'] = logged_user.id
        return redirect('/dashboard')
    return redirect("/")

def one_job(request,id):
    context={
    'this_job':Job.objects.get(id=id),
    }
    return render(request, "view.html", context)

def edit_job(request, id):
    context = {
        'job': Job.objects.get(id=id)
    }
    return render(request, "edit.html", context)

def update_job(request, id):
    if "cancel" in request.POST:
        return redirect("/dashboard")
    if request.method == "POST":
        errors = Job.objects.job_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            print("errors have been found")
            return redirect(f"/jobs/{id}/edit")
        job = Job.objects.get(id=id)
        job.title = request.POST['title']
        job.description = request.POST['desc']
        job.location=request.POST['location']
        job.save()
    
    return redirect("/dashboard")

def add_job(request, id):
    job = Job.objects.get(id=id)
    user= User.objects.get(id=request.session['uid'])
    job.add_job.add(user)
    job.give_up=False
    job.save()
    return redirect("/dashboard")

def give_up(request, id):
    job = Job.objects.get(id=id)
    job.give_up=True
    job.save()
    return redirect("/dashboard")

def delete_job(request, id):
    job = Job.objects.get(id=id)
    job.delete()
    return redirect("/dashboard")

def logout(request):
    request.session.flush()
    return redirect("/")

