from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path("", views.index, name="index"),
    path("create-post/", views.create_post, name="create_post"),
    path("your-posts/", views.your_posts, name="your_posts"),
    path("delete-post/<int:post_id>/", views.delete_post, name="delete_post"),
    path("detail-post/<int:post_id>/", views.detail_post, name="detail_post"),
    path("edit-post/<int:post_id>/", views.edit_post, name="edit_post"),
    path("login/", views.login_to, name="login"),
    path("logout/", views.logout_from, name="logout"),
    path("sign-up/", views.sign_up_to, name="sign_up_to"),
    path("profile/", views.profile, name="profile"),
    path("edit-profile/", views.edit_profile, name="edit_profile"),
    path("edit-user/", views.edit_user, name="edit_user"),
]
