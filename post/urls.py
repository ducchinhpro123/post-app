from django.urls import path
from . import views

app_name='post'

urlpatterns = [
    path("", views.index, name="index"),
    path("create-post/", views.create_post, name="create_post"),
    path("detail-post/<int:post_id>/", views.detail_post, name="detail_post"),
    path("edit-post/<int:post_id>/", views.edit_post, name="edit_post"),
]
