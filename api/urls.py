from django.urls import path
from api.views import (
    UserList,
    UserDetail,
    UserFollow,
    PostList,
    PostDetail,
    CommentList,
    CommentDetail,
)

urlpatterns = [
    path('users/', UserList.as_view(), name='user-list'),
    path('users/<int:pk>/', UserDetail.as_view(), name='user-detail'),
    path('users/<int:pk>/follow/<int:follow_id>/',
         UserFollow.as_view(), name='user-follow'),
    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetail.as_view(),
         name='post-detail'),
    path('posts/<int:pk>/comments/',
         CommentList.as_view(), name='comment-list'),
    path('comments/<int:pk>/',
         CommentDetail.as_view(), name='comment-detail'),
]
