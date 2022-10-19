from sqlite3 import Cursor
import cv2
from idna import valid_contextj
import mysql.connector
from face_recognition.api import face_distance
import numpy as np
import face_recognition
import os
from datetime import datetime
import RPi.GPIO as GPIO

GPIO.cleanup()


GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.OUT)

mydb = mysql.connector.connect(
host="85.214.122.76",
user="raspberrypilogin",
password="c6nHSG$EKBSPY*#%gohQnbkFouYZ$MKGa53hSFJ",
database="Homesecurity"
)

print("Code gestartet!")

#liste von bildern automatisch anzeigen lassen vom Ordner in dem die bilder sind
path = '/home/pi/Desktop/Projektarbeit/Bilder'
print(path)
images = []
namen = []
classNames =[]
#beinhaltet die Namen der Bilder
meineListe = os.listdir(path)

#ausgeben der Bildernamen
#print(meineListe)
for cls in meineListe:
    #current Images - Jetziges Bild anhängen im Pfad path
    #index der letzten Zeile auslesen
    lastindex = 0

    curImg = cv2.imread(f'{path}/{cls}')
    images.append(curImg)

    #namen ohne .jpg
    classNames.append(os.path.splitext(cls)[0]) 
    #print (classNames)

def findeEncodings(Bilder):
    encodeList = []
    i = 0
    for img in Bilder:
        print(i)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        #img = img.resize((500,500))
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
        i=i+1
    return encodeList


def markpunkte(name): #ab hier auch an einer Datenbank angebunden werden
    with open ('markpunkte.csv','r+') as f:
        Datenliste = f.readlines()
        namensListe = []
        GPIO.output(16,GPIO.HIGH)
        for line in Datenliste:
            entry = line.split(';')
            namensListe.append(entry[0]) # nur Namen in der Liste
            if name not in namensListe:
                name = name.split('_')[0]
                now = datetime.now()
                string_date = now.strftime('%Y-%m-%d')
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name};{string_date};{dtString}')
               
                mycursor = mydb.cursor()
                sql ="INSERT INTO Entsperlog(name,Datum,Zeit) Values (%s,%s,%s)"
                val = (name,string_date,dtString)
                mycursor.execute(sql,val)
                mydb.commit()

                print(mycursor.rowcount,"Neuer Datensatz wurde hinzugefügt")
                
                #lampe zum leuchten
                GPIO.output(16,GPIO.HIGH)
                               
                break
        
                
                

#MAIN CODE PART________________________________________________
print('gesichter einlesen')
encodeListbekannteGesichter =  findeEncodings(images)
print('Encoding beendet')

#3. Punkt matches finden
cap = cv2.VideoCapture(0)

#cap.set(cv2.CAP_PROP_FPS,5)

#true da bild frame für frame
#imgS = imageSmall damit alles flüssiger läuft
while True:
        GPIO.output(16,GPIO.LOW)
        success, img = cap.read()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS,cv2.COLOR_BGR2RGB)
        img = cv2.resize(img,(0,0),None,0.5,0.5)
        
        #da mehrere Gesichter erkannt werden können
        gesichterImFrame = face_recognition.face_locations(imgS) 

        #encoden der webcam
        encodeFrames = face_recognition.face_encodings(imgS,gesichterImFrame)
        

        #gesichter Abgleichen

        for encodeGesicht, gesichterLoc in zip(encodeFrames,gesichterImFrame):
            matches = face_recognition.compare_faces(encodeListbekannteGesichter,encodeGesicht) #Liste?
            faceDis = face_recognition.face_distance(encodeListbekannteGesichter,encodeGesicht) #gibt liste der Parameter zurück, kleinste Distanz=match
            #print("Gesichtsdistanzen")
            #print(faceDis)
            matchIndex = np.argmin(faceDis)#kleinste Distanz

            if matches[matchIndex]:
                name = classNames[matchIndex].upper() #Namen groß geschrieben
                name = name.split('_')[0]
                print(name)
                y1,x2,y2,x1=gesichterLoc
                y1,x2,y2,x1 = y1*2,x2*2,y2*2,x1*2
                cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),2) #margenta
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markpunkte(name)
                GPIO.output(16,GPIO.LOW)
                
                
                

            
            else: 
                name = ''
                #print(name)
                y1,x2,y2,x1 = gesichterLoc
                y1, x2, y2, x1 = y1*2,x2*2,y2*2,x1*2
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                GPIO.output(16,GPIO.LOW)

        cv2.imshow('Webcam',img)
        if cv2.waitKey(5) & 0xFF == 27:
            break
GPIO.output(16,GPIO.LOW)
GPIO.cleanup()
