# technikerprojekt
technikerprojekt 2022


Aufbau
Raspberry Pi 4 mit Webcam und Gesichtserkennungs Ki
Ubuntu 20.04 server mit mysql Datenbank
React Native Handy App



Beim start des Python programs werden hinterlegete bilder der zu erkennenden personen eingelesen.
Danach wir damit begonnen auf den Kammera bilder nach Gesichtern zu suchen,
wird ein gesicht gefunden wird überprüft ob es mit einem der hinterlegten bilder übereinstimmt.
Wenn eine der hinterlegten Personen erkannt wird wird ein eintrag mit Name, Zeit und Datum in die externen geschrieben.
Zur kommunukation zwischen Datenbak und Handy App wird eine PHP API benutzt welche die letzten 10 einträge der Datenbank 
in das jason Format and die App übergint.
