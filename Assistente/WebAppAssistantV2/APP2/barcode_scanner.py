import cv2
from pyzbar.pyzbar import decode


capture_webcam = cv2.VideoCapture(0)


#Equanto a webcam estiver aberta
while capture_webcam.isOpened():
    
    sucess, frame = capture_webcam.read()

    barcode = decode(frame) #Decodificando o código de barras
     
    frame = cv2.flip(frame, 1)  #Invertendo a imagem como espelho
    cv2.putText(frame,"Pressione 'e' para sair", (0, 400), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2) #Escrevendo na tela


    if not barcode:
        pass

    else:
        for codes in barcode:
            # Se o barcode não for vazio
            if codes.data != "":
                cv2.putText(frame,f"{codes.data.decode('utf-8')} Adicionado a dispensa", (0, 50), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,255,0), 2) #Escrevendo o código de barras na tela
                print(f"\033[92m{codes.data}\033[0m") #Mostrando o código de barras
                break
  
    cv2.imshow("Webcam", frame) #Mostrando a imagem da webcam
    if cv2.waitKey(1) == ord("e") or cv2.waitKey(1)== ord("E"): #Se a tecla "e" ou E  for pressionada
                                                                # Termina a execução
        break