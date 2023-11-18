import cv2
from pyzbar import pyzbar

async def get_code(image):
    try:
        image = cv2.imread(image)
        barcodes = pyzbar.decode(image)
        for barcode in barcodes:
            btype = barcode.type
            if btype == 'QRCODE':
                pass
            else:
                bdata = barcode.data.decode("utf-8")
                return [True, bdata]
        
    except Exception as e:
        return [False, e]