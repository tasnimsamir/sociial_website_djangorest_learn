from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # path('users/', views.UserList.as_view()),
    # path('users/<int:pk>/', views.UserDetail.as_view()),
    path('posts/', views.PostListView.as_view()),
    # path('posts/<int:pk>/', views.PostDetailView.as_view()),
    path('comments/', views.CommentListView.as_view()),
    path('comments/<int:id>/', views.CommentView.as_view()),
    path('likes/', views.LikeListView.as_view()),
    path('likes/<int:post>/<int:owner>/', views.LikeView.as_view()),
]
# In our case, the primary key for the User is the id field

urlpatterns = format_suffix_patterns(urlpatterns)