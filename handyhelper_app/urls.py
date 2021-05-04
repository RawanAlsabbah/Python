from django.urls import path
from . import views

urlpatterns = [
    # return render templates
    path('', views.index),
    path('dashboard', views.dashboard),
    path('jobs/new', views.new_job),
    path('jobs/<int:id>', views.one_job),
    path('jobs/<int:id>/edit', views.edit_job),



    # return redirects
    path('register', views.register),
    path('login', views.login),
    path('jobs/create', views.create_job),
    path('jobs/<int:id>/update', views.update_job),
    path('jobs/<int:id>/delete', views.delete_job),
    path("jobs/<int:id>/add", views.add_job),
     path("jobs/<int:id>/give_up", views.give_up),



    #logout
    path('logout', views.logout),

]