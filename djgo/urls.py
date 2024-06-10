from django.urls import path # type: ignore
from . import views

urlpatterns=[
    path("",views.home,name="home"),
    path("bmi/",views.bmi,name="bmi"),
    path("calories/",views.calories,name="calories"),
    path("login/",views.login,name="login"),
    path("signup/",views.signup,name="signup"),
    path("video/",views.video,name="video"),
    path("profile/",views.port,name="profile"),
    path("shop/",views.shop,name="shop"),
    path("training/",views.training,name="training"),
    path("logout/",views.logout,name="logout"),
    path("profile/feedback/", views.feedback, name="feedback"),
    path("shop/addtocart", views.addtocart, name="addtocart"),
    path("shop/checkout", views.checkout, name="checkout"),
]