import logging
import socket

import constCS
from context import lab_logging

import pickle

lab_logging.setup(stream_level=logging.INFO) 

database = {
    '1': {'name': 'Ries', 'prename': 'Patrick', 'age': 22},
    '2': {'name': 'Kai', 'prename': 'Schwank', 'age': 21}
}

#Code von clientservr.py

class Telefonauskunftsdienst:
    _logger = logging.getLogger("vs2lab.lab1.clientserver.Server")
    _serving = True

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((constCS.HOST, constCS.PORT))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  
        self.sock.settimeout(3)  
        self._logger.info("Server bound to socket " + str(self.sock))

    def serve(self):
        self.sock.listen(1)
        while self._serving: 
            try:
                (connection, address) = self.sock.accept()  
                while True:  
                    data = connection.recv(1024) 
                    if not data:
                        break
# Start von server 
                    # Asciis werden gesendet
                    sent_list = []
                    # For Each um alle Ascii Zeichen durchzugehen
                    for ascii_item in data:
                        # Füge die Übersetzen Ascii Zeichen der Liste hinzu
                        sent_list.append(chr(ascii_item))
                    # Liste wird zu einem Wort
                    sent = "".join(sent_list) 
                    # Ist das Wort ein "-" haben wir definiert: GET-ALL
                    if sent == "-":
                        # Sende die komplette Datenbank mittels Pickle
                        connection.send(pickle.dumps(database))  
                    else: 
                
                        # Leerzeichen bedeutet dass
			# Vor und einen Nachnamen haben und somit die Split funktionen 
                        # Aufrufen könne.
                        if sent.find(" ") > 0:
                            # Splitte Vor und Nachname
                            prename, lastname = sent.split(" ")
                            # For Each schleife über die Datenbank
                            for key, value in database.items():
                                # Abfrage der Werte mit upper damit Groß und Kleinschreibung ignoriert werden
                                if value["prename"].upper() == prename.upper() and value["name"].upper() == lastname.upper():
                                    # Senden der Person
                                    connection.send(pickle.dumps(value))
                        else:

			    #Fehler Situtation bzw fehlerhafte Eingabe und sende dann leere DB
                            connection.send(pickle.dumps({}))
                    sent = ""


                connection.close() 
            except socket.timeout:
                pass  
        self.sock.close()
        self._logger.info("Server down.")

class Benutzerschnittstelle:
    logger = logging.getLogger("vs2lab.a1_layers.clientserver.Client")

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((constCS.HOST, constCS.PORT))
        self.logger.info("Client connected to socket " + str(self.sock))

# Start
    # Methode um alle Personen der Datenbank zu bekommen
    # Ein "-" wird als Symbol des GET"-"ALLs gesendet.
    def get_all(self):
        self.sock.send('-'.encode('ascii'))
        data = self.sock.recv(1024)
        msg_out = pickle.loads(data)
        self.logger.info("Successfully sent.")
        return msg_out
    # Methode um eine bestimmte Personen der Datenbank zu bekommen
    # Der Vor- und Nachname wird Parameter übergeben.
    def get(self, name):
        self.sock.send(name.encode('ascii')) 
        data = self.sock.recv(1024)  
        msg_out = pickle.loads(data)
        self.logger.info("Successfully sent.")
        return msg_out




    def close(self):
        self.sock.close()
        self.logger.info("Connection closed.")
