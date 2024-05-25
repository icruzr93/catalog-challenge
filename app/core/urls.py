from django.urls import path

from .views import AuthLoginView, UserDetailView, UserListCreateView

urlpatterns = [
    path("users/", UserListCreateView.as_view(), name="users"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="user-detail"),
    path("login/", AuthLoginView.as_view(), name="login"),
]
