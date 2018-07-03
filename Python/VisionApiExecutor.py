# import necessary libraries (I installed them via pip)
import urllib
import json
import requests
import concurrent.futures

from io import BytesIO
from PIL import Image, ImageDraw

# Replace 'KEY_<some-service>' with your subscription key as a string
vision_subscription_key = 'KEY_<for-computer-vision-api>'

# Replace with your chosen region (same region in your REST API call as you used to obtain your subscription keys).
your_region = 'westeurope'
base_uri = 'https://' + your_region + '.api.cognitive.microsoft.com' # Your base URL for using MCS (Microsoft Cognitive Service) APIs

#<=- Computer Vision API -=>#

def analyze(filepath): # Identifies celebs and much more
    params = {
        'visualFeatures': 'Categories,Description,Color,ImageType,Faces'
    }

    # route to the api
    path_to_vision_api = '/vision/v2.0/analyze' # https://westus.dev.cognitive.microsoft.com/docs/services/5adf991815e1060e6355ad44/operations/56f91f2e778daf14a499e1fa

    is_url = filepath.startswith('http')
    requestHeaders = {}

    if is_url:  # Use 'application/json' and 'url' for a remote image
        requestHeaders = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': vision_subscription_key,
        }
    else:       # Use 'application/octet-stream' and 'data' for locally stored image files
        requestHeaders = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': vision_subscription_key,
        }
        with open(filepath, 'rb') as f:
            print(f)
            img_data = f.read()

    try:
        url = base_uri + path_to_vision_api
        if is_url:  # Chose an image from the web
            response = requests.post(url,
                                    json={"url": filepath},     # https://docs.microsoft.com/en-us/azure/cognitive-services/Computer-vision/quickstarts/python-analyze
                                    headers=requestHeaders,
                                    params=params)
        else:       # Chose a local image
            response = requests.post(url,
                                    data=img_data,              # https://docs.microsoft.com/en-us/azure/cognitive-services/Computer-vision/quickstarts/python-disk
                                    headers=requestHeaders,
                                    params=params)

        print ('Response (for ' + url + '):')

        # The 'analysis' object contains various fields that describe the image.
        # The most relevant caption for the image can be found in the 'descriptions' property.
        analysis = response.json()
        print (analysis)
        if response.status_code == 200:
            image_caption = analysis["description"]["captions"][0]["text"].capitalize()
            print (image_caption)

            # Display the image and overlay it with the caption.
            # If you are using a Jupyter notebook, uncomment the following line.
            #%matplotlib inline
            if is_url == False: # From: https://docs.microsoft.com/ca-es/azure/cognitive-services/computer-vision/quickstarts/python-domain
                from PIL import Image
                from io import BytesIO
                import matplotlib.pyplot as plt
                image = Image.open(BytesIO(img_data))
                plt.imshow(image)
                plt.axis("off")
                _ = plt.title(image_caption, size="x-large", y=-0.1)
                image.show() # Open and display the same image, while marking the detected faces

    except Exception as e:
        print('Error:')
        print(e)

def analyzeBatch(urls): # For farther guidance: https://code.likeagirl.io/beginners-guide-to-mcs-face-api-pt3-480e5f029be0
    success_responses_counter = 0
    error_responses_counter = 0
    # A great way to get a https://social.msdn.microsoft.com/Forums/sqlserver/en-US/5e9f8bed-062e-4c0c-81a4-f9ea315f0a53/face-api-rate-limit-exceeded-exception?forum=mlapi
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_url = {executor.submit(analyze, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print(exc) # RateLimitExceeded is expected here.... depends on YOUR pricing (https://azure.microsoft.com/en-us/pricing/)
                # Example: {'error': {'code': 'RateLimitExceeded', 'message': 'Rate limit is exceeded. Try again later.'}}
                error_responses_counter = error_responses_counter + 1
            else:
                success_responses_counter = success_responses_counter + 1
    print("done analyzing " + str(len(urls)) + " urls")
    print("success_responses_counter = " + str(success_responses_counter))
    print("error_responses_counter = " + str(error_responses_counter))

                #==- Utilities -==#

# Convert width height to a point in a rectangle
def getRectangle(faceDictionary):
    rect = faceDictionary['faceRectangle']
    left = rect['left']
    top = rect['top']
    bottom = left + rect['height']
    right = top + rect['width']
    return ((left, top), (bottom, right))

# analyze('{http:/}/path/to/image1.jpg')

# Will describe this image, for example: "A sunset over a body of water"
# analyze("https://www.publicdomainpictures.net/pictures/150000/velka/tropical-beach-1454007190ZAK.jpg")

# analyzeBatch(['{http:/}/path/to/image1.jpg', '{http:/}/path/to/image2.jpg', '{http:/}/path/to/image3.jpg', '{http:/}/path/to/image4.jpg', '{http:/}/path/to/image5.jpg'])

# analyze('AvengersCast.jpg')
# analyze('liga-justicia.jpg')
# analyze('beach-coast-coconut-trees-221471.jpg')
