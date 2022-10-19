import cv2
from face_recognition.api import face_distance
import numpy as np
import face_recognition

# Importieren des Bildes von Emma Watson
imgEmma= face_recognition.load_image_file('C:\Techniker_2\Projektarbeit\Bilder\emma_watson.jpg')
imgEmma = cv2.cvtColor(imgEmma,cv2.COLOR_BGR2RGB)

#Importieren des Testbildes
imgEmmaTest= face_recognition.load_image_file('C:\Techniker_2\Projektarbeit\Bilder\emma_watson_test.jpg')
imgEmmaTest = cv2.cvtColor(imgEmmaTest,cv2.COLOR_BGR2RGB)

#gesicht erkennen 0 da es nur ein Bild ist dass man einliest
faceLoc= face_recognition.face_locations(imgEmma)[0] 

#gesicht encoden
encodeEmma = face_recognition.face_encodings(imgEmma)[0]

#die gesichtslokation sowie die farbe margenta als rahmen
cv2.rectangle(imgEmma,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)

#Ausgabe der gesichtslokation: oben rechts unten und links
#print(faceLoc) 

#Selbe testBild
faceLocTest= face_recognition.face_locations(imgEmmaTest)[0] 
encodeEmmaTest = face_recognition.face_encodings(imgEmmaTest)[0]
cv2.rectangle(imgEmmaTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)

#gesichter vergleichen und distanzen miteinander vergleichen
results = face_recognition.compare_faces([encodeEmma],encodeEmmaTest) #liste der bekannten gesichter angeben in den eckigen klammern, mit dem komma dann das was vergleicht werden soll

#viele Gesichter können sich sehr ähnlich sehen um das zu umgehen können die distanzen angegeben werden, je kleiner die distanz umso besser ist es
faceDis = face_recognition.face_distance([encodeEmma],encodeEmmaTest)

print(results,faceDis)
#ausgeben der distanz auf dem testbild
cv2.putText(imgEmmaTest,f'{results} {round(faceDis[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)

# Anzeigen des Bildes 
cv2.imshow('Emma Watson',imgEmma)
cv2.imshow('Emma Watson Test',imgEmmaTest)
cv2.waitKey(0)

