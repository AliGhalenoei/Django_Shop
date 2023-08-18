from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    name_category=serializers.SerializerMethodField()
    class Meta:
        model=Category
        fields=('__all__')
    
    def get_name_category(self,obj):
        result=obj.cate.all()
        return ProductSerializer(instance=result,many=True).data

class ProductSerializer(serializers.ModelSerializer):
    #name_category=serializers.SerializerMethodField()
    class Meta:
        model=Product
        fields=('__all__')

    # def get_name_category(self,obj):
    #     result=obj.cate.all()
    #     return CategorySerializer(instance=result,many=True).data