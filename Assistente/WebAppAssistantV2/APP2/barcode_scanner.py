import cv2
from pyzbar.pyzbar import decode
import numpy as np
import base64

def barcode_scanner(frame):
    product_barcode = None

    # Decodifique a string base64 para bytes
    frame_bytes = base64.b64decode(frame)

    # Converta os bytes em um array numpy
    frame_array = np.fromstring(frame_bytes, np.uint8)

    # Decodifique o array numpy usando cv2.imdecode()
    frame_image = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

    if frame_image is not None:
        barcode = decode(frame_image)

        if barcode:
            for codes in barcode:
                if codes.data:
                    product_barcode = codes.data.decode('utf-8')
                    break
    return product_barcode