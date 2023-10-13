import cv2
from pyzbar import pyzbar

async def get_code(image):
    try:
        image = cv2.imread(image)
        barcode = pyzbar.decode(image)
        bdata = barcode[0].data.decode("utf-8")
        
        return [0, int(bdata)]
    except Exception as e:
        
        return [1, e]