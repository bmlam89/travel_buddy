from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.index,name="index"),
    url(r'^registration$',views.registration,name="registration"),
    url(r'^login$',views.login,name="login"),
    url(r'^logout$',views.logout,name="logout"),
    url(r'^travels$', views.travels, name="travels"),
    url(r'^travels/add$', views.add, name="add_plan"),
    url(r'^submit$', views.submit, name="submit_plan"),
    url(r'^travels/destination/(?P<id>\d+)$', views.destination, name="destination"),
    url(r'^join/(?P<id>\d+)$', views.join, name="join"),

]