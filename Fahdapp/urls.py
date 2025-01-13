from django.urls import path
from .views import HomeView,login_view,signup_view,blog_view, reservation_view



urlpatterns = [
   path("",HomeView.as_view(),name="Home"),
   path("login/",login_view,name ="Login"),
   path("signup/",signup_view, name="Signup"),
   path("blog/",blog_view,name= "Blog"),
   path("reservation/<int:hotel_id>", reservation_view,name="Reservation")
   
]