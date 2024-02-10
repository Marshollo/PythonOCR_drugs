import requests
import pytesseract
from PIL import Image


# loading the image
def load_image(photo):
    image = Image.open(photo)
    text = pytesseract.image_to_string(image)
    print(text)
    text_stripped = text.strip()
    return text_stripped

def search_drug_info(drug_name):
    url = f"https://api.fda.gov/drug/label.json?search=openfda.brand_name:{drug_name}&limit=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'results' in data and data['results']:
            result = data['results'][0]
            drug_info = {
                'brand_name': result.get('openfda', {}).get('brand_name', ['Unknown'])[0],
                'generic_name': result.get('openfda', {}).get('generic_name', ['Unknown'])[0],
                'dosage': result.get('dosage_forms_and_strengths', 'Unknown'),
                'route': result.get('route', 'Unknown'),
                'indication': result.get('indications_and_usage', 'Unknown')
            }
            return drug_info
    return None

if __name__ == "__main__":
    drug_name = load_image("lek3.png")
    drug_info = search_drug_info(drug_name)
    if drug_info:
        print("Drug Information:")
        print(f"Brand Name: {drug_info['brand_name']}")
        print(f"Generic Name: {drug_info['generic_name']}")
        print(f"Dosage: {drug_info['dosage']}")
        print(f"Route: {drug_info['route']}")
        print(f"Indication: {drug_info['indication']}")
    else:
        print(f"No information found for drug: {drug_name}")