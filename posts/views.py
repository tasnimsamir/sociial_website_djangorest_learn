from cgitb import lookup
from rest_framework.generics import ListAPIView,ListCreateAPIView,RetrieveUpdateDestroyAPIView
from . import serializers
from users_api.models import Account
from .models import Post,Comments,Like
from rest_framework import permissions,authentication
from .permissions import IsOwnerOrReadOnly


class PostListView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, ]
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        # print(serializer)
        # print('=====================================',self.request.user)
        serializer.save(owner=self.request.user)

# class PostDetailView(RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly]
#     authentication_classes = (authentication.TokenAuthentication,)
#     queryset = Post.objects.all()
#     serializer_class = serializers.PostSerializer
    

class CommentListView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = Comments.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
class CommentView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = Comments.objects.all()
    serializer_class = serializers.CommentSerializer
    lookup_field = 'id'


class LikeListView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = Like.objects.all()
    serializer_class = serializers.LikeSerializer
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

from django.shortcuts import get_object_or_404
class MultipleFieldLookupORMixin(object):
    """
    Actual code http://www.django-rest-framework.org/api-guide/generic-views/#creating-custom-mixins
    Apply this mixin to any view or viewset to get multiple field filtering
    based on a `lookup_fields` attribute, instead of the default single field filtering.
    """
    def get_object(self):
        queryset = self.get_queryset()             # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            try:                                  # Get the result with one or more fields.
                filter[field] = self.kwargs[field]
            except Exception:
                pass
        return get_object_or_404(queryset, **filter)  # Lookup the object

class LikeView(MultipleFieldLookupORMixin,RetrieveUpdateDestroyAPIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = (authentication.TokenAuthentication,)
    queryset = Like.objects.all()
    serializer_class = serializers.LikeSerializer
    lookup_fields = ('post','owner')
    
