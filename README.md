<!DOCTYPE html>
<html>

<body>
	<h1>SERVER.py</h1>
	<p>El archivo SERVER.py se utiliza para iniciar un servidor y permitir la conexión con los clientes a través de sockets.</p>
	<p>Para ejecutarlo, es necesario tener Python 3 instalado.</p>
	<h3>Instalación:</h3>
	<ol>
		<li>Descargar el archivo SERVER.py</li>
		<li>Abrir la terminal en el directorio donde se encuentra el archivo.</li>
		<li>Ejecutar el siguiente comando: python3 SERVER.py</li>
	</ol>
	<h3>Parámetros a modificar:</h3>
	<ul>
		<li>En la línea 12 se debe modificar el valor de HOST por la dirección IP del equipo donde se ejecuta el servidor.</li>
		<li>En la línea 13 se debe modificar el valor de PORT por el número de puerto que se desee utilizar para la conexión.</li>
	</ul>
	<h3>Uso:</h3>
	<p>El servidor se iniciará y se quedará esperando conexiones entrantes. Cuando un cliente se conecte, se imprimirá en la terminal la dirección IP y el puerto del cliente.</p>
  <hr>

<h1>CLIENT.py</h1>
<p>El archivo CLIENT.py se utiliza para conectarse a un servidor a través de sockets y enviar comandos para ser ejecutados en el equipo donde se ejecuta el servidor.</p>
<p>Para ejecutarlo, es necesario tener Python 3 instalado.</p>
<h3>Instalación:</h3>
<ol>
	<li>Descargar el archivo CLIENT.py</li>
	<li>Abrir la terminal en el directorio donde se encuentra el archivo.</li>
	<li>Ejecutar el siguiente comando: python3 CLIENT.py</li>
</ol>
<h3>Parámetros a modificar:</h3>
<ul>
	<li>En la línea 11 se debe modificar el valor de HOST por la dirección IP del equipo donde se ejecuta el servidor.</li>
	<li>En la línea 12 se debe modificar el valor de PORT por el número de puerto que se utiliza para la conexión.</li>
</ul>
<h3>Uso:</h3>
<p>Una vez que se inicia el cliente, se conectará automáticamente con el servidor especificado. Luego, se le pedirá al usuario que ingrese un comando para ser ejecutado en el servidor. El resultado de la ejecución del comando será enviado de vuelta al cliente y se imprimirá en la terminal.</p>
</body>
</html>
