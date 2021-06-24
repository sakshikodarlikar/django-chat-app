from django.urls import path


from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('signup', views.signup, name="signup"),
    path('lists', views.lists, name="lists"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('addfriend', views.addfriend, name="addfriend"),
    path('acceptfriend/<str:friend_request>', views.acceptfriend, name="acceptfriend"),
    path('declinefriend/<str:friend_request>', views.declinefriend, name="declinefriend"),
    path('message/<str:friend_list>', views.message, name="message"),
    path('send', views.send, name="send"),

]

