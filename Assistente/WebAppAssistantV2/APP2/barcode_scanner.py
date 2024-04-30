"""
@brief Este módulo contém funções para a decodificação de códigos de barras a partir de imagens.

Este módulo é projetado para analisar strings codificadas que representam imagens, 
descodificá-las para encontrar códigos de barras e retornar as informações contidas nesses códigos. 
É útil em aplicações que necessitam de processamento de imagem para reconhecimento de códigos de barras em diversos formatos.

@details A função `barcode_scanner` converte uma string para um array numpy, que então é transformado. 
Utilizando a biblioteca OpenCV e Pyzbar, a função analisa a imagem para detectar e descodificar códigos de barras. 
Os códigos descodificados são retornados como strings. Se nenhum código for encontrado, a função retorna None.

@note Se ocorrer uma falha durante o processo de descodificação da imagem ou durante a detecção de códigos de barras, 
mensagens de erro são impressas para ajudar na diagnóstico do problema.
"""

import cv2
from pyzbar.pyzbar import decode
import numpy as np
import base64


def barcode_scanner(frame):
    """
    @brief Analisa um frame codificado para detectar códigos de barras presentes numa imagem.
    @details Esta função converte uma string codificada em base64 para um array numpy, que é então decodificado para uma imagem.
    Utilizando a biblioteca OpenCV e Pyzbar, a função analisa a imagem para detectar e descodificar códigos de barras.
    
    @param frame {string} String codificada em correspondente à imagem a ser analisada.
    
    @return Retorna o código de barras descodificado como uma string ou None se nenhum código de barras for detectado.

    @note Se ocorrer uma exceção durante a análise da imagem, uma mensagem de erro é impressa
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