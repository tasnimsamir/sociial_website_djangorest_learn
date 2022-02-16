from django.urls import include, path

from .views import UserRegistrationView,UserLoginView,AccountDetail,AccountList,friendsListView,deleteFriendRequestView,AcceptAccountView
urlpatterns = [
    path('signup', UserRegistrationView.as_view()),
    path('signin', UserLoginView.as_view()),
    path('accounts/', AccountList.as_view()),
    path('accounts/<int:id>/', AccountDetail.as_view()),
     path('account/<int:id>/', AcceptAccountView.as_view()),
    #  path('accounts/acceptfriends/<int:id>/', AcceptFriendRequestView.as_view()),
    path('friends/', friendsListView.as_view()),
    path('friends/from:<int:from_user>/to:<int:to_user>/', deleteFriendRequestView.as_view()),
    # 
]