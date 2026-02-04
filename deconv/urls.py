from django.urls import path
from . import views
app_name="deconv"

urlpatterns=[
  path("",views.index , name="index"),
] 