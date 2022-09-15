from flask import Flask, request, render_template

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from flask import Flask, request, render_template
# import requests, os, time
# from azure.cognitiveservices.vision.computervision import ComputerVisionClient
# from msrest.authentication import CognitiveServicesCredentials
# from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
# from dotenv import load_dotenv

# load_dotenv()


app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# def get_text(image_url, computervision_client):
#     # Open local image file
#     read_response = computervision_client.read(image_url, raw=True)
#     # Get the operation location (URL with an ID at the end)
#     read_operation_location = read_response.headers["Operation-Location"]
#     # Grab the ID from the URL
#     operation_id = read_operation_location.split("/")[-1]
#     # Retrieve the results 
#     while True:
#         read_result = computervision_client.get_read_result(operation_id)
#         if read_result.status.lower() not in ["notstarted", "running"]:
#             break
#         time.sleep(1)
#     # Get the detected text
#     text = ""
#     if read_result.status == OperationStatusCodes.succeeded:
#         for page in read_result.analyze_result.read_results:
#             for line in page.lines:
#                 # Get text in each detected line and do some fixes to the structure
#                 if (not text) or text[-1].strip() == "." or text[-1].strip() == ":":
#                     text = text + "\n" + line.text
#                 else:
#                     text = text + " " + line.text
#     text = text.replace(" .", ".").replace(" ,", ",").replace(" :", ":")
#     return text

# def detect_language(text, key, region, endpoint):
#     # Use the Translator detect function
#     path = "/detect"
#     url = endpoint + path
#     # Build the request
#     params = {
#         "api-version": "3.0"
#     }
#     headers = {
#     "Ocp-Apim-Subscription-Key": key,
#     "Ocp-Apim-Subscription-Region": region,
#     "Content-type": "application/json"
#     }
#     body = [{
#         "text": text
#     }]
#     # Send the request and get response
#     request = requests.post(url, params=params, headers=headers, json=body)
#     response = request.json()
#     # Get language
#     language = response[0]["language"]
#     # Return the language
#     return language


# key = "paste-your-key-here"
# endpoint = "paste-your-endpoint-here"

# from azure.ai.textanalytics import TextAnalyticsClient
# from azure.core.credentials import AzureKeyCredential

# # Authenticate the client using your key and endpoint 
# def authenticate_client():
#     ta_credential = AzureKeyCredential(key)
#     text_analytics_client = TextAnalyticsClient(
#             endpoint=endpoint, 
#             credential=ta_credential)
#     return text_analytics_client

# client = authenticate_client()

# # Example method for detecting sensitive information (PII) from text 
# def pii_recognition_example(client):
#     documents = [
#         "The employee's SSN is 859-98-0987.",
#         "The employee's phone number is 555-555-5555."
#     ]
#     response = client.recognize_pii_entities(documents, language="en")
#     result = [doc for doc in response if not doc.is_error]
#     for doc in result:
#         print("Redacted Text: {}".format(doc.redacted_text))
#         for entity in doc.entities:
#             print("Entity: {}".format(entity.text))
#             print("\tCategory: {}".format(entity.category))
#             print("\tConfidence Score: {}".format(entity.confidence_score))
#             print("\tOffset: {}".format(entity.offset))
#             print("\tLength: {}".format(entity.length))
# pii_recognition_example(client)



# def translate(text, source_language, target_language, key, region, endpoint):
#     # Use the Translator translate function
#     url = endpoint + "/translate"
#     # Build the request
#     params = {
#         "api-version": "3.0",
#         "from": source_language,
#         "to": target_language
#     }
#     headers = {
#         "Ocp-Apim-Subscription-Key": key,
#         "Ocp-Apim-Subscription-Region": region,
#         "Content-type": "application/json"
#     }
#     body = [{
#         "text": text
#     }]
#     # Send the request and get response
#     request = requests.post(url, params=params, headers=headers, json=body)
#     response = request.json()
#     # Get translation
#     translation = response[0]["translations"][0]["text"]
#     # Return the translation
#     return translation

@app.route('/predict', methods=['POST'])
def index_post():
    # Read the values from the form
    # image_url = request.form['image']
    # target_language = request.form['language']

    input_text = request.form["PII_text"]
    input_text = [input_text]
    
    # print("Hello 123",input_text)
    # Load the values from .env
    # key = os.getenv("418561caa90e41d2b6358ef66939aaa2")
    key = "418561caa90e41d2b6358ef66939aaa2"
    # region = os.getenv("COG_SERVICE_REGION")
    # endpoint = os.getenv("https://paea2ievata001.cognitiveservices.azure.com/")
    endpoint = "https://paea2ievata001.cognitiveservices.azure.com/"
    # COG_endpoint = os.getenv("COG_SERVICE_ENDPOINT")
    

    def authenticate_client():
        ta_credential = AzureKeyCredential(key)
        text_analytics_client = TextAnalyticsClient(
                endpoint=endpoint, 
                credential=ta_credential)
        return text_analytics_client

    client = authenticate_client()

    def pii_recognition_example(client, input_text):
        documents = [
    #         """Patient needs to take 100 mg of ibuprofen, and 3 mg of potassium. Also needs to take
    #         10 mg of Zocor
    #         Patient needs to take 50 mg of ibuprofen, and 2 mg of Coumadin.""",
            "The employee's SSN is 859-98-0987.",
            "The employee's phone number is 555-555-5555.",
            "Sagar phone number is 8913354122 and he is living in Bangalore for next 14 daya",
            "Sagar's PAN number is YCNLJ8072A and Adhar card number is 123476456253"
        ]
        response = client.recognize_pii_entities(input_text, language="en")
        result = [doc for doc in response if not doc.is_error]
        for doc in result:
            print("Redacted Text: {}".format(doc.redacted_text))
            for entity in doc.entities:
                print("Entity: {}".format(entity.text))
                print("\tCategory: {}".format(entity.category))
                print("\tConfidence Score: {}".format(entity.confidence_score))
                print("\tOffset: {}".format(entity.offset))
                print("\tLength: {}".format(entity.length))
        output_text = doc.redacted_text
        return output_text

    masked_text = pii_recognition_example(client, input_text)

    # Authenticate Computer Vision client
    # computervision_client = ComputerVisionClient(COG_endpoint, CognitiveServicesCredentials(key))

    # Extract text
    # text = get_text(image_url, computervision_client)
    
    # Detect language
    # language = detect_language(text, key, region, endpoint)

    # Translate text
    # translated_text = translate(text, language, target_language, key, region, endpoint)

    # Call render template
    return render_template(
        'results.html',
        translated_text=masked_text,
        original_text=input_text,
        # target_language=target_language
    )
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)