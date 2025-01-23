from . import views
from django.urls import path

urlpatterns = [
    path("", views.index, name="index"),
    path("blog", views.blog, name="blog"),
    path('post/blog/author/<str:author_username>/', views.blog, name='blog_by_author'),
    path("signin", views.signin, name="signin"),
    path("signup", views.signup, name="signup"),
    path("logout", views.logout, name="logout"),
    path("create", views.create, name="create"),
    path("increaselikes/<int:id>", views.increaselikes, name='increaselikes'),
    path("profile/<int:id>", views.profile, name='profile'),
    path("profile/edit/<int:id>", views.profileedit, name='profileedit'),
    path("post/<int:id>", views.post, name="post"),
    path("post/comment/<int:id>", views.savecomment, name="savecomment"),
    path("post/comment/delete/<int:id>", views.deletecomment, name="deletecomment"),
    path("post/edit/<int:id>", views.editpost, name="editpost"),
    path("post/delete/<int:id>", views.deletepost, name="deletepost"),
    path('follow/<int:id>/', views.follow, name='follow'),
    path('unfollow/<int:id>/', views.unfollow, name='unfollow'),
]










# path("contact",views.contact_us,name="contact"),