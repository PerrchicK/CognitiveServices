# import necessary libraries, you need to have previously installed # these via pip 
import urllib
import json
import requests
import concurrent.futures

from io import BytesIO
from PIL import Image, ImageDraw
# Replace 'KEY_x' with your subscription key as a string
vision_subscription_key = '<YOUR_API_KEY>'

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your subscription keys.
# For example, if you obtained your subscription keys from the westus region, replace 
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
# a free trial subscription key, you should not need to change this region.
uri_base = 'https://westeurope.api.cognitive.microsoft.com'

def analyzeBatch(urls):
    # for url in urls: 
    #     analyze(url)

    success_responses_counter = 0
    error_responses_counter = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_to_url = {executor.submit(analyze, url): url for url in urls}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
            except Exception as exc:
                print(exc)
                error_responses_counter = error_responses_counter + 1
            else:
                success_responses_counter = success_responses_counter + 1
    print("done analyzing " + str(len(urls)) + " urls")
    print("success_responses_counter = " + str(success_responses_counter))
    print("error_responses_counter = " + str(error_responses_counter))

def analyze(filepath): # https://docs.microsoft.com/en-us/azure/cognitive-services/Computer-vision/quickstarts/python-analyze
    params = {
        'visualFeatures': 'Categories,Description,Color,ImageType,Faces'
    }

    # route to the face api
    path_to_vision_api = '/vision/v2.0/analyze'
    # open jpg file as binary file data for intake by the MCS api

    is_url = filepath.startswith('http')
    # Request headers
    headers = {}
    # print(is_url)
    if is_url:
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': vision_subscription_key,
        }
    else:
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': vision_subscription_key,
        }
        with open(filepath, 'rb') as f:
            print(f)
            img_data = f.read()

    try:
        # Execute the api call as a POST request. 
        # What's happening?: You're sending the data, headers and
        # parameter to the api route & saving the
        # mcs server's response to a variable.
        # Note: mcs face api only returns 1 analysis at time

        url = uri_base + path_to_vision_api
        if is_url:
            response = requests.post(url,
                        json={"url": filepath},
                        headers=headers,
                        params=params)
        else:
            response = requests.post(url,
                                    data=img_data,
                                    headers=headers,
                                    params=params)

        print ('Response (for ' + url + '):')
        # The 'analysis' object contains various fields that describe the image. The most
        # relevant caption for the image is obtained from the 'descriptions' property.
        analysis = response.json()
        image_caption = analysis["description"]["captions"][0]["text"].capitalize()
        print (analysis)
        # print (image_caption)

        # Display the image and overlay it with the caption.
        # If you are using a Jupyter notebook, uncomment the following line.
        #%matplotlib inline
        if is_url == False:
            from PIL import Image
            from io import BytesIO
            import matplotlib.pyplot as plt
            image = Image.open(BytesIO(img_data))
            plt.imshow(image)
            plt.axis("off")
            _ = plt.title(image_caption, size="x-large", y=-0.1)

    except Exception as e:
        print('Error:')
        print(e)


# analyzeBatch(['https://www.themarysue.com/wp-content/uploads/2015/05/Avengers-Age-of-Ultron-Team-Poster.jpg', 'https://www.themarysue.com/wp-content/uploads/2015/05/Avengers-Age-of-Ultron-Team-Poster.jpg', 'https://cdn.mos.cms.futurecdn.net/JQsTuGusR22dhxNcwS9ePC-1200-80.jpg', 'https://www.themarysue.com/wp-content/uploads/2015/05/Avengers-Age-of-Ultron-Team-Poster.jpg'])

# analyze("https://image.shutterstock.com/image-photo/kiev-ukraine-march-31-2015-260nw-275940803.jpg")

# analyze('AvengersCast.jpg')
# analyze('Yoav_Toussia_Cohen.jpg')
# analyze('liga-justicia.jpg')