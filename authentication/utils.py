from PIL import Image
import pytesseract

def extract_text_from_image(image):
    try:
        img = Image.open(image)
        text = pytesseract.image_to_string(img)
        return text
    except Exception as e:
        return str(e)



