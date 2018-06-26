# import necessary libraries, you need to have previously installed # these via pip 
import urllib
import json
import requests
import concurrent.futures

from io import BytesIO
from PIL import Image, ImageDraw
# Replace 'KEY_x' with your subscription key as a string
face_subscription_key = '<YOUR_API_KEY>'

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your subscription keys.
# For example, if you obtained your subscription keys from the westus region, replace 
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
# a free trial subscription key, you should not need to change this region.
uri_base = 'https://westeurope.api.cognitive.microsoft.com'

def detect(filename):
    # Request parameters 
    # The detection options for MCS Face API check MCS face api 
    # documentation for complete list of features available for 
    # detection in an image
    # these parameters tell the api I want to detect a face and a smile
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,' +
        'emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
    }

    # Request headers
    # for locally stored image files use
    # 'Content-Type': 'application/octet-stream'
    headers = {
        'Content-Type': 'application/octet-stream', # OR 'application/json' with: "url": "http://example.com/1.jpg"
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the face api
    path_to_face_api = '/face/v1.0/detect'
    # open jpg file as binary file data for intake by the MCS api

    with open(filename, 'rb') as f:
        print(f)
        img_data = f.read()
    try:
        # Execute the api call as a POST request. 
        # What's happening?: You're sending the data, headers and
        # parameter to the api route & saving the
        # mcs server's response to a variable.
        # Note: mcs face api only returns 1 analysis at time

        # trump: bc644c9b-516b-4f00-92ac-a3201d6b3d2a

        response = requests.post(uri_base + path_to_face_api,
                                data=img_data, 
                                headers=headers,
                                params=params)
        
        print ('Parsed response:')
        # json() is a method from the request library that converts 
        # the json reponse to a python friendly data structure
        parsed = response.json()
            
        # display the image analysis data
        print (parsed)
        img = Image.open(filename)
        draw = ImageDraw.Draw(img)

        for face in parsed:
            draw.rectangle(getRectangle(face), outline='red')
        #Display the image in the users default image browser.
        img.show()

    except Exception as e:
        print('Error:')
        print(e)

def addFace(filename, faceListId): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395250
    # Request parameters 
    # The detection options for MCS Face API check MCS face api 
    # documentation for complete list of features available for 
    # detection in an image
    # these parameters tell the api I want to detect a face and a smile

    # Request headers
    # for locally stored image files use
    # 'Content-Type': 'application/octet-stream'
    headers = {
        'Content-Type': 'application/octet-stream', # OR 'application/json' with: "url": "http://example.com/1.jpg"
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the face api
    path_to_face_api = '/face/v1.0/facelists/' + faceListId + '/persistedFaces'
    # open jpg file as binary file data for intake by the MCS api

    with open(filename, 'rb') as f:
        print(f)
        img_data = f.read()
    try:
        # Execute the api call as a POST request. 
        # What's happening?: You're sending the data, headers and
        # parameter to the api route & saving the
        # mcs server's response to a variable.
        # Note: mcs face api only returns 1 analysis at time

        # trump: bc644c9b-516b-4f00-92ac-a3201d6b3d2a

        response = requests.post(uri_base + path_to_face_api,
                                data=img_data, 
                                headers=headers)
        
        print ('Response:')
        # json() is a method from the request library that converts 
        # the json reponse to a python friendly data structure
        parsed = response.json()
            
        # display the image analysis data
        print (parsed)

    except Exception as e:
        print('Error:')
        print(e)

def verifyFaces(face_id_1, face_id_2): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f3039523a
    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the face api
    path_to_face_verification_api = '/face/v1.0/verify/'

    payload = {
        "faceId1": face_id_1,
        "faceId2": face_id_2
    }

    try:
        # Execute the api call as a POST request. 
        # What's happening?: You're sending the data, headers and
        # parameter to the api route & saving the
        # mcs server's response to a variable.
        # Note: mcs face api only returns 1 analysis at time
        
        response = requests.post(uri_base + path_to_face_verification_api, json=payload, headers=headers)
        
        print ('Response:')
        print (response)
        # json() is a method from the request library that converts 
        # the json reponse to a python friendly data structure
        parsed = response.json()
        print ("parsed:")
        print (parsed)
            
    except Exception as e:
        print('Error:')
        print(e)

def verifyPerson(face_id, person_group_id, person_id): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f3039523a
    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the face api
    path_to_face_verification_api = '/face/v1.0/verify/'

    payload = {
        "faceId": face_id,
        "personGroupId": person_group_id,
        "personId": person_id
    }

    try:
        # Execute the api call as a POST request. 
        # What's happening?: You're sending the data, headers and
        # parameter to the api route & saving the
        # mcs server's response to a variable.
        # Note: mcs face api only returns 1 analysis at time
        
        response = requests.post(uri_base + path_to_face_verification_api, json=payload, headers=headers)
        
        print ('Response:')
        print (response)
        # json() is a method from the request library that converts 
        # the json reponse to a python friendly data structure
        parsed = response.json()
        print ("parsed:")
        print (parsed)
            
    except Exception as e:
        print('Error:')
        print(e)

def getPersonGroups(persons_list_id = ''): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395246
    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the face api
    path_to_face_list_api = '/face/v1.0/persongroups/' + persons_list_id # in case you want to get a specific list
    # path_to_large_face_list_api = '/face/v1.0/largefacelists/'

    try:
        # Execute the api call as a POST request. 
        # What's happening?: You're sending the data, headers and
        # parameter to the api route & saving the
        # mcs server's response to a variable.
        # Note: mcs face api only returns 1 analysis at time
        
        # uri_base = 'https://westeurope.api.cognitive.microsoft.com'
        print(uri_base + path_to_face_list_api)

        response = requests.get(uri_base + path_to_face_list_api,
                                headers=headers)
        
        print ('Response:')
        print (response)
        # json() is a method from the request library that converts 
        # the json reponse to a python friendly data structure
        parsed = response.json()
        print ("parsed:")
        print (parsed)
            
        # display the image analysis data
        print (response.status_code)
        print ("response.status_code:")

    except Exception as e:
        print('Error:')
        print(e)
        # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/5a157b68d2de3616c086f2cc
        # 409: already exists

def getFaceLists(faceListId = ''): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f3039524c
    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the face api
    path_to_face_list_api = '/face/v1.0/facelists/' + faceListId
    # path_to_large_face_list_api = '/face/v1.0/largefacelists/'

    try:
        # Execute the api call as a POST request. 
        # What's happening?: You're sending the data, headers and
        # parameter to the api route & saving the
        # mcs server's response to a variable.
        # Note: mcs face api only returns 1 analysis at time
        
        # uri_base = 'https://westeurope.api.cognitive.microsoft.com'
        print(uri_base + path_to_face_list_api)

        response = requests.get(uri_base + path_to_face_list_api,
                                headers=headers)
        
        print ('Response:')
        print (response)
        # json() is a method from the request library that converts 
        # the json reponse to a python friendly data structure
        parsed = response.json()
        print ("parsed:")
        print (parsed)
            
        # display the image analysis data
        print (response.status_code)
        print ("response.status_code:")

    except Exception as e:
        print('Error:')
        print(e)
        # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/5a157b68d2de3616c086f2cc
        # 409: already exists

def addFaceList(faceListId, name, userData): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f3039524b
    # Request parameters 
    # these parameters tell the api I want to detect a face and a smile
    params = {
        "name": name,
        "userData": userData
    }

    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the face api
    path_to_face_list_api = '/face/v1.0/facelists/' + faceListId
    # path_to_large_face_list_api = '/face/v1.0/largefacelists/' + largeFaceListId

    try:
        # Execute the api call as a POST request. 
        # What's happening?: You're sending the data, headers and
        # parameter to the api route & saving the
        # mcs server's response to a variable.
        # Note: mcs face api only returns 1 analysis at time

        payload = params
        
        # uri_base = 'https://westeurope.api.cognitive.microsoft.com'
        print(uri_base + path_to_face_list_api)

        response = requests.put(uri_base + path_to_face_list_api,
                                json=payload,
                                # body=payload,
                                # params=payload,
                                headers=headers)
        
        print ('Response:')
        print (response)
        # json() is a method from the request library that converts 
        # the json reponse to a python friendly data structure
        # parsed = response.json()
        # print ("parsed:")
        # print (parsed)
            
        # display the image analysis data
        print (response.status_code)
        print ("response.status_code:")

    except Exception as e:
        print('Error:')
        print(e)
        # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/5a157b68d2de3616c086f2cc
        # 409: already exists

def addPersonGroup(personGroupId, name, userData): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f3039524b
    # Request parameters 
    # these parameters tell the api I want to detect a face and a smile
    params = {
        "name": name,
        "userData": userData
    }

    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the face api
    path_to_face_list_api = '/face/v1.0/persongroups/' + personGroupId
    # path_to_large_face_list_api = '/face/v1.0/largefacelists/' + largeFaceListId

    try:
        # Execute the api call as a POST request. 
        # What's happening?: You're sending the data, headers and
        # parameter to the api route & saving the
        # mcs server's response to a variable.
        # Note: mcs face api only returns 1 analysis at time

        payload = params
        
        # uri_base = 'https://westeurope.api.cognitive.microsoft.com'
        print(uri_base + path_to_face_list_api)

        response = requests.put(uri_base + path_to_face_list_api,
                                json=payload,
                                # body=payload,
                                # params=payload,
                                headers=headers)
        
        print ('Response:')
        print (response)
        # json() is a method from the request library that converts 
        # the json reponse to a python friendly data structure
        # parsed = response.json()
        # print ("parsed:")
        # print (parsed)
            
        # display the image analysis data
        print (response.status_code)
        print ("response.status_code:")

    except Exception as e:
        print('Error:')
        print(e)
        # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/5a157b68d2de3616c086f2cc
        # 409: already exists

def addPersonToPersonGroup(personGroupId, name, userData): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395249

    # The training task is an asynchronous task (seconds to minutes, depends on the number of person entries and their faces). Use checkTrainingStatus to check training status.

    # Request parameters 
    # The detection options for MCS Face API check MCS face api 
    # documentation for complete list of features available for 
    # detection in an image
    # these parameters tell the api I want to detect a face and a smile
    params = {
        "name": name,
        "userData": userData
    }
    # route to the face api
    path_to_face_api = '/face/v1.0/persongroups/' + personGroupId + '/persons'
    # path_to_face_api = '/face/v1.0/findsimilars'

    # Request headers
    # for locally stored image files use
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    try:
        # Execute the api call as a POST request. 
        # What's happening?: You're sending the data, headers and
        # parameter to the api route & saving the
        # mcs server's response to a variable.
        # Note: mcs face api only returns 1 analysis at time

        response = requests.post(uri_base + path_to_face_api,
                                json=params, 
                                headers=headers)
        
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
    # Request parameters 
    # The detection options for MCS Face API check MCS face api 
    # documentation for complete list of features available for 
    # detection in an image
    # these parameters tell the api I want to detect a face and a smile

    # Request headers
    # for locally stored image files use
    # 'Content-Type': 'application/octet-stream'
    headers = {
        'Content-Type': 'application/octet-stream', # OR 'application/json' with: "url": "http://example.com/1.jpg"
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the face api
    path_to_face_api = '/face/v1.0/persongroups/' + personGroupId + '/persons/' + personId + '/persistedFaces' # + '[?userData][&targetFace]'
    # open jpg file as binary file data for intake by the MCS api

    with open(filename, 'rb') as f:
        print(f)
        img_data = f.read()
    try:
        # Execute the api call as a POST request. 
        # What's happening?: You're sending the data, headers and
        # parameter to the api route & saving the
        # mcs server's response to a variable.
        # Note: mcs face api only returns 1 analysis at time

        # trump: bc644c9b-516b-4f00-92ac-a3201d6b3d2a

        response = requests.post(uri_base + path_to_face_api,
                                data=img_data,
                                headers=headers)
        
        print ('Response:')
        # json() is a method from the request library that converts 
        # the json reponse to a python friendly data structure
        parsed = response.json()
            
        # display the image analysis data
        print (parsed)

    except Exception as e:
        print('Error:')
        print(e)

def train(personGroupId): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395249

    # The training task is an asynchronous task (seconds to minutes, depends on the number of person entries and their faces). Use checkTrainingStatus to check training status.

    # Request parameters 
    # The detection options for MCS Face API check MCS face api 
    # documentation for complete list of features available for 
    # detection in an image
    # these parameters tell the api I want to detect a face and a smile
    params = { }
    # route to the face api
    path_to_face_api = '/face/v1.0/persongroups/' + personGroupId + '/train'
    # path_to_face_api = '/face/v1.0/findsimilars'

    # Request headers
    # for locally stored image files use
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    try:
        # Execute the api call as a POST request. 
        # What's happening?: You're sending the data, headers and
        # parameter to the api route & saving the
        # mcs server's response to a variable.
        # Note: mcs face api only returns 1 analysis at time

        response = requests.post(uri_base + path_to_face_api,
                                json=params, 
                                headers=headers)
        
        print ('Response:')
        print (response)

    except Exception as e:
        print('Error:')
        print(e)

def checkTrainingStatus(personGroupId): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395246
    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    # route to the face api
    path_to_face_api = '/face/v1.0/persongroups/' + personGroupId + '/training'
    # path_to_large_face_list_api = '/face/v1.0/largefacelists/'

    try:
        # Execute the api call as a POST request. 
        # What's happening?: You're sending the data, headers and
        # parameter to the api route & saving the
        # mcs server's response to a variable.
        # Note: mcs face api only returns 1 analysis at time
        
        # uri_base = 'https://westeurope.api.cognitive.microsoft.com'

        response = requests.get(uri_base + path_to_face_api,
                                headers=headers)
        
        print ('Response:')
        print (response)
        # json() is a method from the request library that converts 
        # the json reponse to a python friendly data structure
        parsed = response.json()
        print ("parsed:")
        print (parsed)
            
        # display the image analysis data
        print (response.status_code)
        print ("response.status_code:")

    except Exception as e:
        print('Error:')
        print(e)
        # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/5a157b68d2de3616c086f2cc
        # 409: already exists

def identify(faceIds): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395239
    # Request parameters 
    # The detection options for MCS Face API check MCS face api 
    # documentation for complete list of features available for 
    # detection in an image
    # these parameters tell the api I want to detect a face and a smile
    params = {
        "faceListId": "meetup_persons_list",
        "faceIds": faceIds,
        "maxNumOfCandidatesReturned": 1,
        "confidenceThreshold": 0.5
    }
    # route to the face api
    path_to_face_api = '/face/v1.0/identify'
    # path_to_face_api = '/face/v1.0/findsimilars'

    # Request headers
    # for locally stored image files use
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    try:
        # Execute the api call as a POST request. 
        # What's happening?: You're sending the data, headers and
        # parameter to the api route & saving the
        # mcs server's response to a variable.
        # Note: mcs face api only returns 1 analysis at time

        response = requests.post(uri_base + path_to_face_api,
                                json=params, 
                                headers=headers)
        
        print ('Response:')
        # json() is a method from the request library that converts 
        # the json reponse to a python friendly data structure
        parsed = response.json()
            
        # display the image analysis data
        print (parsed)

    except Exception as e:
        print('Error:')
        print(e)

def findSimilars(faceIds): # https://westus.dev.cognitive.microsoft.com/docs/services/563879b61984550e40cbbe8d/operations/563879b61984550f30395239
    # Request parameters 
    # The detection options for MCS Face API check MCS face api 
    # documentation for complete list of features available for 
    # detection in an image
    # these parameters tell the api I want to detect a face and a smile
    params = {
        "faceListId": "meetup_persons_list",
        "faceIds": faceIds,
        "maxNumOfCandidatesReturned": 1,
        "mode": "matchPerson"
    }

    # route to the face api
    path_to_face_api = '/face/v1.0/findsimilars'

    # Request headers
    # for locally stored image files use
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': face_subscription_key,
    }

    try:
        # Execute the api call as a POST request. 
        # What's happening?: You're sending the data, headers and
        # parameter to the api route & saving the
        # mcs server's response to a variable.
        # Note: mcs face api only returns 1 analysis at time

        response = requests.post(uri_base + path_to_face_api,
                                json=params, 
                                headers=headers)
        
        print ('Response:')
        # json() is a method from the request library that converts 
        # the json reponse to a python friendly data structure
        parsed = response.json()
            
        # display the image analysis data
        print (parsed)

    except Exception as e:
        print('Error:')
        print(e)

#Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

# detect('/Users/pshalev/Downloads/trump-twitter.jpg')
# detect('The_Avengers_Assembled.jpg')
# detect('/Users/pshalev/Dropbox/~ Shared - other MacBook/Pics/Me/Avatar1.jpg')
# detect('/Users/pshalev/Dropbox/~ Shared - other MacBook/Pics/Me/Bad hair day (1).png')
# detect('/Users/pshalev/Dropbox/~ Shared - other MacBook/Pics/Me/Bad hair day (2).png')
# detect('/Users/pshalev/Dropbox/~ Shared - other MacBook/Pics/Me/half-marathon.jpg')
# identify()

# addPersonGroup(person_group_id, person_group_name, optional_user_data)
# addPersonToPersonGroup(person_group_id, person_name, optional_user_data)
# addFaceToPerson(image_fila_local_path, person_id, person_group_id)
# addFaceToPerson("training/GameChanger.png", "d50a4f57-6c30-4c38-8bc8-b4368e41255d", "meetup_persons_list")
# train("meetup_persons_list")
# checkTrainingStatus("meetup_persons_list")

# verifyPerson(temporary_face_id_from_detect_api, trained_person_group_id, person_id)
# verifyPerson('619bc094-a5a6-499f-b6a5-10a0f8963afc', 'meetup_persons_list', 'd50a4f57-6c30-4c38-8bc8-b4368e41255d')
# verifyPerson('761373a9-c131-4866-b881-3da33aea6cc4', 'meetup_persons_list', 'd50a4f57-6c30-4c38-8bc8-b4368e41255d')
# verifyPerson('4293f9f6-fde0-4b19-b9e4-271ed018f104', 'meetup_persons_list', 'd50a4f57-6c30-4c38-8bc8-b4368e41255d')
# verifyPerson('5bfcdecb-6ef9-4f31-bcbe-eef76cfee834', 'meetup_persons_list', 'd50a4f57-6c30-4c38-8bc8-b4368e41255d')

# identify(['8311ce49-4d93-4f48-ad9d-52a1d391e963'])
# identify(['bae7af26-061c-4715-8eab-bbf045a6fdb0', '7223364e-1d14-4ee1-ad7a-d6b201274d2b'])

# findSimilars(['3e4801d5-636a-45b1-8f69-d60103059811'])







# addFaceList("meetup_sample_list" ,"meetup_sample_list", "The data used in the meetup.")
# getFaceLists('meetup_sample_list')  # {faceListId} in case you want to get a specific list
# addFace('/Users/pshalev/Downloads/trump-twitter.jpg', "meetup_sample_list") # {'persistedFaceId': '5d6d6dd6-fa98-4872-bf07-d95c1bf8b58e'}
# getPersonGroups() # getPersonGroups("meetup_persons_list")
