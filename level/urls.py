from django.conf.urls import url

from . import views

app_name = "users"
urlpatterns = [
    url(r"^join/$", views.leveljoin, name="join"),
    url(r"^team/", views.leveltree, name="tree"),
]