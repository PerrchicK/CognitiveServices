# import necessary libraries (I installed them via pip)
import urllib
import json
import requests
import concurrent.futures

from io import BytesIO
from PIL import Image, ImageDraw

# Replace 'KEY_<some-service>' with your subscription key as a string
face_subscription_key = 'KEY_<for-face-api>'

# Replace with your chosen region (same region in your REST API call as you used to obtain your subscription keys).
your_region = 'westeurope'
base_uri = 'https://' + your_region + '.api.cognitive.microsoft.com' # Your base URL for using MCS (Microsoft Cognitive Service) APIs

#<=- Face API -=>#

def detect(filename):
    # Detection options for Face API
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }

    requestHeaders = {
        'Content-Type': 'application/octet-stream', # Use 'application/octet-stream' and 'data' for locally stored image files OR 'application/json' and 'url' for a remote image
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the api
    path_to_face_api = '/face/v1.0/detect' # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395236

    # open jpg file as binary file data
    with open(filename, 'rb') as f:
        print(f)
        img_data = f.read()
    try:
        # Execute the api call as a POST request. 
        # Note: MCS Face API only returns 1 analysis at a time
        response = requests.post(base_uri + path_to_face_api,
                                data=img_data, 
                                headers=requestHeaders,
                                params=params)
        
        print ('Parsed response:')
        parsed = response.json() # The 'json()' method converts the json reponse to a python friendly data structure

        print (parsed) # Print the analysis data
        img = Image.open(filename)
        draw = ImageDraw.Draw(img)

        for face in parsed:
            draw.rectangle(getRectangle(face), outline='red')
        img.show() # Open and display the same image, while marking the detected faces

    except Exception as e:
        print('Error:')
        print(e)

def verifyFaces(face_id_1, face_id_2): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f3039523a
    # face_id_1 AND face_id_2 should come from the Face Detection API
    requestHeaders = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the api
    path_to_face_verification_api = '/face/v1.0/verify/'

    payload = {
        "faceId1": face_id_1,
        "faceId2": face_id_2
    }

    try:
        # Execute the api call as a POST request. 
        response = requests.post(base_uri + path_to_face_verification_api, json=payload, headers=requestHeaders)
        
        print ('Response:')
        print (response)

        parsed = response.json() # The 'json()' method converts the json reponse to a python friendly data structure
        print ("parsed:")
        print (parsed)
            
    except Exception as e:
        print('Error:')
        print(e)

def verifyPerson(face_id, person_id, person_group_id): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f3039523a
    # Request headers
    requestHeaders = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the api
    path_to_face_verification_api = '/face/v1.0/verify/'

    payload = {
        "faceId": face_id,
        "personGroupId": person_group_id,
        "personId": person_id
    }

    try:
        response = requests.post(base_uri + path_to_face_verification_api, json=payload, headers=requestHeaders)
        
        print ('Response:')
        print (response)

        parsed = response.json() # The 'json()' method converts the json reponse to a python friendly data structure
        print ("parsed:")
        print (parsed)
            
    except Exception as e:
        print('Error:')
        print(e)

def getPersonGroups(persons_list_id = ''): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395246
    # Request headers
    requestHeaders = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the api
    path_to_persons_groups_api = '/face/v1.0/persongroups/' + persons_list_id # in case you want to get a specific list

    try:
        print(base_uri + path_to_persons_groups_api)

        response = requests.get(base_uri + path_to_persons_groups_api,
                                headers=requestHeaders)
        
        print ('Response:')
        print (response)

        parsed = response.json() # The 'json()' method converts the json reponse to a python friendly data structure
        print ("parsed:")
        print (parsed)
            
        print (response.status_code)
        print ("response.status_code:")

    except Exception as e:
        print('Error:')
        print(e)
        # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/5a157b68d2de3616c086f2cc
        # 409: already exists

def addPersonGroup(personGroupId, name, userData): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f3039524b
    # Request parameters 
    params = {
        "name": name,
        "userData": userData
    }

    requestHeaders = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the api
    path_to_persons_groups_api = '/face/v1.0/persongroups/' + personGroupId

    try:
        payload = params
        
        print(base_uri + path_to_persons_groups_api)

        response = requests.put(base_uri + path_to_persons_groups_api,
                                json=payload,
                                # body=payload,
                                # params=payload,
                                headers=requestHeaders)
        
        print ('Response:')
        print (response)

        # Print the status code
        print ("response.status_code:")
        print (response.status_code)

    except Exception as e:
        print('Error:')
        print(e)
        # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/5a157b68d2de3616c086f2cc
        # 409: already exists

def addPersonToPersonGroup(personGroupId, name, userData): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395249
    # Request parameters 
    params = {
        "name": name,
        "userData": userData
    }
    # route to the api
    path_to_face_api = '/face/v1.0/persongroups/' + personGroupId + '/persons'
    # path_to_face_api = '/face/v1.0/findsimilars'

    # Request headers
    # for locally stored image files use
    requestHeaders = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    try:
        response = requests.post(base_uri + path_to_face_api,
                                json=params, 
                                headers=requestHeaders)
        
        print ('Response:')
        print (response)
        parsed = response.json()
        print ("parsed:")
        print (parsed)
        personId = parsed["personId"]
        print (name + "'s ID is: " + personId)

    except Exception as e:
        print('Error:')
        print(e)

def addFaceToPerson(filename, personId, personGroupId): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395250
    requestHeaders = {
        'Content-Type': 'application/octet-stream', # Use 'application/octet-stream' and 'data' for locally stored image files OR 'application/json' and 'url' for a remote image
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the api
    path_to_face_api = '/face/v1.0/persongroups/' + personGroupId + '/persons/' + personId + '/persistedFaces' # + '[?userData][&targetFace]'

    # open jpg file as binary file data for intake by the MCS api
    with open(filename, 'rb') as f:
        print(f)
        img_data = f.read()
    try:
        response = requests.post(base_uri + path_to_face_api,
                                data=img_data,
                                headers=requestHeaders)
        
        print ('Response:')
        parsed = response.json() # The 'json()' method converts the json reponse to a python friendly data structure            
        print (parsed)

    except Exception as e:
        print('Error:')
        print(e)

def train(personGroupId): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395249

    # The training task is an asynchronous task (seconds to minutes, depends on the number of person entries and their faces).
    # Use checkTrainingStatus to check training status.
    params = { } # Yes, the API reference guides us to send an empty body

    # route to the api
    path_to_face_api = '/face/v1.0/persongroups/' + personGroupId + '/train'

    requestHeaders = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    try:
        response = requests.post(base_uri + path_to_face_api,
                                json=params, 
                                headers=requestHeaders)
        
        print ('Response:')
        print (response) # A successful call returns an empty JSON body with 202 ACCEPTED code: https://httpstatuses.com/202

    except Exception as e:
        print('Error:')
        print(e)

def checkTrainingStatus(personGroupId): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395246

    requestHeaders = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the face api
    path_to_face_api = '/face/v1.0/persongroups/' + personGroupId + '/training'

    try:
        response = requests.get(base_uri + path_to_face_api, headers=requestHeaders)
        
        print ('Response:')
        print (response)

        parsed = response.json() # The 'json()' method converts the json reponse to a python friendly data structure            
        print ("parsed:")
        print (parsed)

        print ("response.status_code:")
        print (response.status_code)

    except Exception as e:
        print('Error:')
        print(e)
        # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/5a157b68d2de3616c086f2cc
        # 409: already exists

                #==- Utilities -==#

# Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

# detect('The_Avengers_Assembled.jpg')

# getPersonGroups() # Yeah, I had a hard time getting used to the snake_case (https://en.wikipedia.org/wiki/Snake_case)
# getPersonGroups(person_group_id)

# addPersonGroup(person_group_id, person_group_name, optional_user_data_1)
# addPersonToPersonGroup(person_group_id, person_name, optional_user_data_2)
# addFaceToPerson('{http:/}/path/to/image.jpg', person_id, person_group_id)
# train(person_group_id)
# checkTrainingStatus(trained_person_group_id)
# verifyPerson(temporary_face_id_from_detect_api, person_id, trained_person_group_id)
