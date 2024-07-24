from django.conf import settings

from app.llmModels.gemini import geminiModel 
from app.llmModels.openai import opemnAImodel

query = '''
Below is the text extracted from the prescription of a patient. From the given text, Extract medical information from the provided prescription text and output it in strict JSON format. Give the following information for each prescribed medicine:

- `name`: The name of the medicine.
- `use`: What the medicine is used for.
- `dosage`: The dosage in the prescription or the recommended dosage.
- `sideeffects`: Any side effects of the medicine.
- `working`: How the medicine works and treats the disease.
- `type`: The type of the medicine (e.g., tablet, syrup).

Additionally, include any extra information you were able to retrieve from the text under the key `extra_info`.  For `extra_info`, save the information in the format where the key is the title of the info and the value is the detail retrieved.
If the text does not provide specific details, include general recommended information.

Here's the template for the JSON structure:
```json
{
  "prescriptions": [
    {
      "name": "",
      "use": "",
      "dosage": "",
      "sideeffects": "",
      "working": "",
      "type": ""
    }
  ],
  "extra_info": {
    "key1": "value1",
    "key2": "value2"
  }
}
```
If there is no text or text provided does not seems to be medical information, return this exact string:NO_DATA.

prescription text:

'''

model = settings.MODEL
supported_models=settings.SUPPORTED_MODELS

def getMedicineInfo(extracted_image_data, ret):
    print("extracting medicine from model")

    if model==supported_models.OPENAI:
        opemnAImodel(extracted_image_data, ret, query)
    elif model==supported_models.GEMINI:
        print("geminiModel")
        geminiModel(extracted_image_data, ret, query)
    else :
        ret["status"] = 401
        ret["mssg"] = "model not supported"
        return