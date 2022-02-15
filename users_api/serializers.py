from rest_framework import serializers
from users_api.models import Account,FriendRequest
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.authtoken.models import Token

class RegistrationSerializer(serializers.ModelSerializer):
   class Meta:
       model=Account
       fields = [
            "name",
            "email",
            "zipcode",
            "Date_of_Birth",
            "gender",
            "password",
        ]
       extra_kwargs={'password':{'write_only':True}}
   def create(self,validated_data):
       password=validated_data.pop('password',None)
       instance=self.Meta.model(**validated_data)
       if password is not None:
           instance.set_password(password)
       instance.save()
       return instance

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password is not found.'
            )
        try:
            Token.objects.get_or_create(user=user)
            update_last_login(None, user)
        except Account.DoesNotExist:
            raise serializers.ValidationError(
                'User with given email and password does not exists'
            )

        return {
            'email':user.email,
            'token': user.auth_token.key
        }



class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"



class FriendRequestSerializer(serializers.ModelSerializer):
    from_user = serializers.ReadOnlyField(source='from_user.id')
    class Meta:
        model = FriendRequest
        fields = "__all__"