import urllib.request
import threading
import time
rangos_a_unir={}
rangos_unir_comprobacion={}
print("=====================================================")
print("CREADOR JHOAN BARRERA")
print("=====================================================")
extension=input("ESCRIBE LA EXTENSION DEL ARCHIVO: ")
def peso_archivo_rangos_unir(url):

	c=urllib.request.urlopen(url)

	c=int(c.getheader('Content-Length'))
	print("TAMAÑO DEL ARCHIVO",c)

	c=int(c//50)+1
	d=c
	for i in range(50):
		if i==0:
			rangos_a_unir[0]=c
		else:

			rangos_a_unir[(c-d)+1]=c
		c=c+d
	print(rangos_a_unir)
	iniciar_descarga_paralela(url,rangos_unir_comprobacion)

def descarga_rangos(url,a,b):
	
	data= urllib.request.Request(url)

	data.add_header('Range',f'bytes={str(a)}-{str(b)}' )

	data=urllib.request.urlopen(data)
	#try:
	data=data.read()
	rangos_unir_comprobacion[a]=data
	print(len(rangos_unir_comprobacion))

	#except:
	#	rangos_unir_comprobacion[a]=data

	

def reconstruccion_datos(rangos):
	while True:
		
		
		if len(rangos)==50:
			print("==============")
			print("claves")
			print("===========")
			print(rangos.keys())

			print("===========")
			print("RANGOS ORDENADOS")
			print("==============")
			lista_rangos_ordenados=sorted(rangos)
			with open("archivo_descargado.{}".format(extension), "wb") as f:
				for i in range(len(lista_rangos_ordenados)):
					f.write(rangos[lista_rangos_ordenados[i]])

			break
		

def iniciar_descarga_paralela(url,rangos_unir_comprobacion):
	a=0
	for i in rangos_a_unir:
		try:
			thread=threading.Thread(target=descarga_rangos, args=(url,i,rangos_a_unir[i],))
			thread.start()
		except:
			thread=threading.Thread(target=descarga_rangos, args=(url,i,rangos_a_unir[i],))
			thread.start()
			print("HUBO ERROR")
		a+=1
		time.sleep(1.5)
	thread2=threading.Thread(target=reconstruccion_datos, args=(rangos_unir_comprobacion,))
	thread2.start()



peso_archivo_rangos_unir(f"{input('ESCRIBE TU URL: ')}")
