from rest_framework import generics 
from .models import Place, Category
from .serializers import PlaceSerializer, PlaceNameSerializer, CategorySerializer, LandmarkDetectionSerializer 
from django.conf import settings
from rest_framework.response import Response
import os
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.preprocessing import image as image_utils
import numpy as np
import tensorflow as tf
from PIL import Image
import pickle
from ArabicOcr import arabicocr
from transformers import MarianTokenizer
import cv2
import io

class PlaceList(generics.ListAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceNameSerializer
   

class PlaceDetail(generics.RetrieveAPIView):
	queryset = Place.objects.all()
	serializer_class = PlaceSerializer
	lookup_field = 'name'
	

class CategoryList(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryPlaceList(generics.ListAPIView):
     serializer_class = PlaceNameSerializer

     def get_queryset(self):
        category_name = self.kwargs['name']
        places = Place.objects.filter(category__name=category_name)
        return places
     
     
class PlaceCategoryDetail(generics.RetrieveAPIView):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    lookup_field = 'name'

    def get_queryset(self):
        category_name = self.kwargs['name1']
        place_name = self.kwargs['name']
        place = Place.objects.filter(category__name=category_name, name=place_name)
        return place     


class LandmarkDetection(generics.GenericAPIView):
    def post(self, request): 
        # Get the image file from the request
        img_file = request.FILES.get('image')
        
        # Load the image and preprocess it
        img = Image.open(img_file).resize((224,224))
        img = image_utils.img_to_array(img)
        img = img.reshape(1,224,224,3)
        img = preprocess_input(img)         
        
        # Use the AI model to predict the landmark
        model_path = os.path.join(settings.BASE_DIR, 'static', 'ai_models', 'models', 'best_model.h5')
        model = tf.keras.models.load_model(model_path)
        classes = {0: 'Abdeen palace', 1: 'Bab Zuweila', 2: 'Baron palace', 3: 'Bent Pyramid', 4: 'Cairo Tower', 5: 'Deir al-Bahari (Hatshepsut Temple)', 6: "Edfu's Temple of Horus", 7: 'Great Sphinx of Giza', 8: 'Kalabsha Temple', 9: 'Luxor Temple', 10: 'Medinet Habu Temple', 11: 'Pyramid of Djoser', 12: 'Pyramid of teti', 13: 'Pyramids of Giza', 14: 'Ramesseum Temple', 15: 'Temple of Hathor', 16: 'Temple of Isis', 17: 'Temple of Kom Ombo', 18: 'The Egyptian Museum', 19: 'The Unfinished Obelisk', 20: 'The temple of Nefertari', 21: 'The temple of Ramesses ii', 22: 'saladin citadel'}
        pred = model.predict(img)
        landmark_name = classes[np.argmax(pred)]
        
        # Return the detected landmark name as a JSON response
        return Response({'landmark_name': landmark_name})


class OCRTranslation(generics.GenericAPIView):
    def post(self, request):
        # Get the image file from the request
        img_file = request.FILES.get('image')

        image_path = 'input_image.jpg'
        with open(image_path, 'wb') as f:
            f.write(img_file.read())

        # Perform OCR on the input image to extract text
        out_image = 'out.jpeg'
        results = arabicocr.arabic_ocr(image_path, out_image)
        text = ''
        for result in results:
            text += result[1] + ' '

        # Perform translation on the extracted text
        tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-ar-en")
        tokenized_text = tokenizer.prepare_seq2seq_batch([text], return_tensors='pt')

        # Load the saved model
        model_path = os.path.join(settings.BASE_DIR, 'static', 'ai_models', 'models', 'model.pkl')
        with open(model_path, 'rb') as f:
            model = pickle.load(f)

        # Perform translation and decode the output
        translation = model.generate(**tokenized_text)
        translated_text = tokenizer.batch_decode(translation, skip_special_tokens=True)[0]
        
        os.remove(image_path)

        # Return the translated text as a JSON response
        return Response({'translated_text': translated_text})
