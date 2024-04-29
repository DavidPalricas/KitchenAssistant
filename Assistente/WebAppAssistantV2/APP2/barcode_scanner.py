import cv2
from pyzbar.pyzbar import decode
import numpy as np
import base64


def barcode_scanner(frame):
    """
    Analisa um frame codificado para detectar códigos de barras presentes numa imagem.

    @param frame {string} String codificada em correspondente à imagem a ser analisada.
    
    @return Retorna o código de barras descodificado como uma string ou None se nenhum código de barras for detectado.

    @exception Se ocorrer uma exceção durante a análise da imagem, uma mensagem de erro é impressa
    """
    product_barcode = None

    # Descodifique a string base64 para bytes
    frame_bytes = base64.b64decode(frame)

    # Converta os bytes em um array numpy
    frame_array = np.fromstring(frame_bytes, np.uint8)

    # Decodifique o array numpy usando cv2.imdecode()
    frame_image = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)

    if frame_image is not None:
        barcode = decode(frame_image)

        print(f"Código de barras do produto: {barcode}")

        if barcode:
            for codes in barcode:
                if codes.data:
                    product_barcode = codes.data.decode('utf-8')
                    break
           
    return product_barcode