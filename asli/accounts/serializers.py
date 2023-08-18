from rest_framework import serializers
from accounts.models import User

class LoginSerializer(serializers.Serializer):
    phone=serializers.CharField()
    password=serializers.CharField()

    # def create(self, validated_data):
    #     User.objects.create_user(**validated_data)
        #return super().create(**validated_data)



class SingupSerializer(serializers.Serializer):
    phone=serializers.CharField()
    email=serializers.EmailField()
    username=serializers.CharField()
    password=serializers.CharField()
    password2=serializers.CharField()

    # def create(self, validated_data):
    #     User.objects.create_user(**validated_data)

    def validate_phone(self,value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError('Phone is alredy')
        return value
    
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Email is alredy')
        return value
    
    def validate_username(self,value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('username is alredy')
        return value
        
    def validate(self, value):
        if value['password'] and value['password2'] and value['password'] != value['password2']:
            raise serializers.ValidationError('passwords is not mach')
        return value
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('phone','email','username','password')
        
        
