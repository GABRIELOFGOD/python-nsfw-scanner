
from rest_framework.response import Response
from rest_framework.decorators import api_view
import requests
from bs4 import BeautifulSoup
from nudenet import NudeDetector
import tempfile

forbiddens=["ANUS EXPOSED","BUTTOCKS_EXPOSED","FEMALE_BREAST_EXPOSED","MALE_GENITALIA_EXPOSED","FEMALE_GENITALIA_EXPOSED"]

@api_view(['POST'])
def requester(request):
    isExplicit = False
    if request.method == 'POST':
        
        # Initializing Temporary Array

        # Define the image URL
        image_url = request.data['data']

        # Make an HTTP GET request to fetch the image data
        response = requests.get(image_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Get the image data
            image_data = response.content
            
            # Save the image data to a temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
                temp_file.write(image_data)
                temp_file_path = temp_file.name
            
            # Initialize the NudeDetector object
            detector = NudeDetector()
            
            # Use the detect() method to perform nudity detection
            result = detector.detect(temp_file_path)
            print(result)

            
            # Process the result
            for forbidden in forbiddens:
                if(result['class' == forbidden] and result[0]['score'] >= 0.2):
                    isExplicit = not isExplicit

        else:
            print(f"Failed to fetch image: HTTP status code {response.status_code}")
    return Response(isExplicit)