from rest_framework import status
from rest_framework.generics import CreateAPIView,RetrieveAPIView,ListAPIView,UpdateAPIView,ListCreateAPIView,DestroyAPIView,RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAdminUser
from .serializers import FriendRequestSerializer, RegistrationSerializer,LoginSerializer,AccountSerializer
from rest_framework.views import APIView
from .models import Account,FriendRequest
from rest_framework.authtoken.models import Token
from rest_framework import permissions,authentication
from posts.permissions import IsOwnerOrReadOnly

class UserRegistrationView(CreateAPIView):

    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        
        response = {
            'success' : 'True',
            'status code' : status_code,
            'message': 'User registered  successfully',
            }
        
        return Response(response, status=status_code)

class UserLoginView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        
        is_accepted_value = Account.objects.filter(email = serializer.data['email']).values_list('is_accepted',flat=True)[0]
        isaccepted_message = Account.objects.filter(email = serializer.data['email']).values_list('is_accepted_message',flat=True)[0]

     
        acc_id = Token.objects.filter(key= serializer.data['token']).values_list('user',flat=True)[0]
    

        if is_accepted_value == 1:
            response = {
                'success' : 'True',
                'status code' : status.HTTP_200_OK,
                'is accepted' : is_accepted_value,
                'message': 'User logged in  successfully',
                'token' : serializer.data['token'],
                'id': acc_id
                }
            status_code = status.HTTP_200_OK
            return Response(response, status=status_code)

        elif is_accepted_value == 0:

            response = {
                'success' : 'False',
                # 'status code' : status.HTTP_406_NOT_ACCEPTABLE,
                'is accepted' : is_accepted_value,
                'message': isaccepted_message,
                'token' : serializer.data['token'],
                'id': acc_id
                }
            return Response(response)
        else:
            response = {
                'success' : 'False',
                # 'status code' : status.HTTP_406_NOT_ACCEPTABLE,
                'is accepted' : is_accepted_value,
                'message': isaccepted_message,
                'token' : serializer.data['token'],
                'id': acc_id
                }
            return Response(response)
            # status_code = status.HTTP_406_NOT_ACCEPTABLE


class AccountList(ListAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class AccountDetail(RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'id'


class AcceptAccountView(RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    authentication_classes = (authentication.TokenAuthentication,)
    serializer_class = AccountSerializer
    lookup_field = 'id'
    queryset = Account.objects.all()

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            # print('==================================',serializer.data)
            return Response({"message": "message are updated successfully"})

        else:
            return Response({"message": "failed", "details": serializer.errors})



class friendsListView(ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = (authentication.TokenAuthentication,)
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    
    def perform_create(self, serializer):
        serializer.save(from_user=self.request.user)

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

class deleteFriendRequestView(MultipleFieldLookupORMixin,DestroyAPIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    # authentication_classes = (authentication.TokenAuthentication,)
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    lookup_fields = ('from_user','to_user')

    
# class AcceptFriendRequestView(UpdateAPIView):
#     serializer_class = AccountSerializer
#     lookup_field = 'id'
#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data, partial=True)
        

#         if serializer.is_valid():
#             serializer.save()
#             print('==================================',serializer.data)
#             return Response({"message": "Friends are updated successfully"})

#         else:
#             return Response({"message": "failed", "details": serializer.errors})



# class PostEditView(UpdateView):
#      def form_valid(self, form):
#         # Take care of creating of updating your post with cleaned data
#         # by yourself

#         category_tokens = form.cleaned_data['categories'].split()
#         categories = set()
#         for token in category_tokens:
#             try:
#                 category = Category.objects.get(name=token)
#             except ObjectDoesNotExist:
#                 category = Category.objects.create(name=token)
            
#             categories.add(category)

#         # now you need to add the categories which are new to this post
#         # and delete the categories which do not belong anymore to your post
#         current_posts_categories = set(post_instance.categories_set.all())
#         categories_to_add = categories - current_posts_categories
#         categories_to_delete = current_posts_categories - categories