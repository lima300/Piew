from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("piew", views.piew_view, name="piew"),
    path("like/<int:id>", views.like, name="like"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("user/<int:id>", views.user, name="user"),
    path("dislike/<int:id>", views.dislike, name="dislike"),
    path("delete/<int:id>", views.delete_piew, name="delete_piew"),
    path("deleteC/<int:id>", views.delete_comment, name="delete_comment"),
    path("likes/<int:id>", views.likes, name="likes"),
    path("follow/<int:id>", views.follow, name="follow"),
    path("followers/<int:id>", views.followers, name="followers"),
    path("unfollow/<int:id>", views.unfollow, name="unfollow"),
    path("following/<int:id>", views.following, name="following"),
    path("avatar", views.avatar, name="avatar"),
    path("search", views.search, name="search")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)