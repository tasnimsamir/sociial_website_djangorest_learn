from django.contrib import admin

from django.urls import path, include
# from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authtoken.views import obtain_auth_token  

urlpatterns = [
path('admin/', admin.site.urls),
   path('', include('users_api.urls')),
   path('', include('posts.urls')),
   path('api-auth/', include('rest_framework.urls')),
   path('api-token-auth/', obtain_auth_token, name='api_token_auth'), 

]