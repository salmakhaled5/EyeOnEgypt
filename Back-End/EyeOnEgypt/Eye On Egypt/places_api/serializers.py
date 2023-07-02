from rest_framework import serializers
from .models import Category, Place  


class PlaceSerializer(serializers.ModelSerializer):
	class Meta:
		model = Place 
		fields = '__all__'

class PlaceNameSerializer(serializers.ModelSerializer):
	class Meta:
		model = Place
		fields = ['name']


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category 
		fields = ['name']		
		
class LandmarkDetectionSerializer(serializers.Serializer):
    image = serializers.ImageField()				
		
		
