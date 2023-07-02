from django.urls import path, include
from .views import PlaceList, PlaceDetail, CategoryList, CategoryPlaceList, PlaceCategoryDetail,LandmarkDetection, OCRTranslation

urlpatterns = [
    path('places/', PlaceList.as_view()),
    path('places/<str:name>/', PlaceDetail.as_view()),
    path('categories/', CategoryList.as_view()),
    path('categories/<str:name>/', CategoryPlaceList.as_view()),
    path('categories/<str:name1>/<str:name>/', PlaceCategoryDetail.as_view()),   
    path('detect-landmark/', LandmarkDetection.as_view()),
    path('ocr-translate/', OCRTranslation.as_view()),
    #path('detect-landmark/<str:name>/', PlaceDetail.as_view()),
]
