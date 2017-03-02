import csv
PATH = 'notas.csv'


def exportar_html(d_notas):
	"""Crea un archivo en formato html. Recibe un diccionario de listas y crea un archivo con formato html listando los contenidos de las listas,
	agrupados por valor"""
	with open("notas.html","w") as html:
		html = open('notas.html','w')
		html.write('<!DOCTYPE HTML>\n<html>\n\t<head>\n\t\t<title>Listado de notas</title>\n\t</head>\n\t<body>\n\t\t<h1>Listado de notas</h1>\n')
		for etiqueta,notas in d_notas.items():
			if etiqueta == '':
				etiqueta = 'Sin Etiqueta'
			html.write('\t\t<h2>{}</h2>\n\t\t<ul>\n'.format(etiqueta))
			for nota in notas:
				html.write('\t\t\t<li>{}</li>\n'.format(nota))
			html.write('</ul>')
		html.write('\t</body>\n</html>')
		print('\nHTML creado exitosamente')


def escribir_notas(f, d_notas):
	""" Escribe un archivo con lo datos de un diccionario. Recibe un diccionario de notas on el formato {etiqueta1:[nota1,nota2,...],...} y un handler del archivo notas.csv abierto en modo write. Escribe el archivo completo a partir del diccionario de notas"""
	for etiqueta,notas in d_notas.items():
		for nota in notas:	
			f.write(etiqueta + "|" + nota + "\n")


def eliminar_nota(d_notas):
	"""Elimina notas del diccionario. Recibe un diccionario de listas y después de preguntar al usuario elimina la nota elegida,
	 que puede ser parte de un valor o el único valor de la clave (lo cual significa que se elimina también la clave). Devuelve el diccionario modificado y después
	 escribe el diccionario en el archivo pisando el antiguo archivo"""
	if d_notas != {}:
		print("\nListado de etiquetas:")
		for etiqueta in d_notas:
			if etiqueta == "":
				print("-Sin etiqueta (para ingresar a esta opción presione enter)")
			else:
				print("-{}".format(etiqueta))
		etiqueta_eliminar = input('\nIngrese la etiqueta de donde quiera eliminar una nota: ')
		if etiqueta_eliminar in d_notas:
			i = 0
			if etiqueta_eliminar != "":
				print('[{}]'.format(etiqueta_eliminar))
			else:
				print('[Sin etiqueta]')
			for nota in d_notas[etiqueta_eliminar]:
				i+=1
				print('{}. {}'.format(i,nota))
			#No podemos usar verificador_input_numerico porque el usuario tiene la opcion de ingresar un texto vacío para cancelar
			while True:
				posicion_nota_eliminar = input('\nEscoga entre las opciones mostradas, o presione enter para cancelar: ')
				if posicion_nota_eliminar == "":
					print("\nEliminación cancelada exitosamente.")
					return d_notas
				if posicion_nota_eliminar.isdigit():
					if int(posicion_nota_eliminar) > 0 and int(posicion_nota_eliminar) <= i:
						break
				print("\nValor ingresado inválido")
			print('{}. {}'.format(i,d_notas[etiqueta_eliminar][int(posicion_nota_eliminar)-1]))
			confirmacion = verificador_input_numerico("\nIngrese un 1 para confirmar la eliminación y un 0 para cancelarla: ",0,1)
			if confirmacion == 1:
				d_notas[etiqueta_eliminar].pop(int(posicion_nota_eliminar)-1)
				if not(d_notas[etiqueta_eliminar]):
					d_notas.pop(etiqueta_eliminar)
				with open(PATH,'w') as f: #no hace falta salvar la excepción FileNotFound pues en el menú principal el archivo es creado
					escribir_notas(f, d_notas)	
				print('\nNota eliminada')
			else:
				print("\nEliminación cancelada exitosamente.")
		else:
			print('\nEtiqueta no encontrada.')
	else:
		print('\nNo hay notas para eliminar')
	return d_notas


def buscar_notas(d_notas):
	"""Muestra notas que contengan la palabra buscada. Recibe un diccionario de notas con el formato {etiqueta1:[nota1,nota2,...],...}, 
	le pide al usuario un texto a buscar y muestra todas las notas que contiene dicho texto (sin discriminar mayusculas y minusculas) agrupadas por etiqueta."""
	if d_notas !={}:
		texto_buscado = input('Ingrese el texto a buscar: ')
		encontrado = False #flag para indicar si mostro algo por pantalla
		primera_nota = True #flag para mostrar la clave no mas de una vez
		for etiqueta,notas in d_notas.items():
			for nota in notas:
				if texto_buscado.lower() in nota.lower():
					if primera_nota:	
						if etiqueta == '':
							etiqueta = '\nSin Etiqueta'
						print('\n[{}]'.format(etiqueta))
					print('- {}'.format(nota))
					primera_nota = False 
					encontrado = True
			primera_nota = True
		if not(encontrado):
			print('\nNo se encontró ninguna nota que contenga "{}".'.format(texto_buscado))	
	else:
		print('\nNo hay notas para buscar')


def listar_notas(d_notas):
	"""Muestra por pantalla un diccionario. Recibe un diccionario de notas con el formato {etiqueta1:[nota1,nota2,...],...} 
	y muestra todas los valores de dichas listas agrupadas por clave"""
	if d_notas != {}:
		for etiqueta,notas in d_notas.items():
			if etiqueta == '':
				etiqueta = 'Sin Etiqueta'
			print('\n[{}]'.format(etiqueta))
			for nota in notas:
				print('-{}'.format(nota))
	else:
		print('\nNo hay notas para listar')

def agregar_nota_al_diccionario(diccionario, etiqueta, nota):
	"""Agrega una nota y una etiqueta asociada a un diccionario. Recibe un diccionario de notas con el formato {etiqueta1:[nota1,nota2,...],...}, una etiqueta y una nota asociada.
	En el caso que la etiqueta ya sea clave del diccionario recibido, simplemente agrega a la lista de valores de dicha clave la nota pasada por parametro.
	En caso que la etiqueta no sea clave del diccionario, se crea dicha clave con una lista cuyo unico valor es la nota recibida.
	Por ultimo devuelve el diccionario modificado"""
	if etiqueta in diccionario:
		diccionario[etiqueta].append(nota.rstrip("\n"))
	else:
		diccionario[etiqueta] = [nota.rstrip("\n")]
	return diccionario


def agregar_nota(d_notas):
	"""Agrega notas al diccionario y también las escribe en el archivo. Recibe un diccionario de notas con el formato {etiqueta1:[nota1,nota2,...],...}. 
	Pide al usuario una nota y una etiqueta (de una sola palabra, no admite espacios), y agrega al diccionario dicha nota. 
	En caso que la etiqueta ya sea una clave del diccionario, agrega la nota como un nuevo elemento de la lista que tiene por valor. 
	Si la etiqueta no esta en el diccionario, la agrega y pone como valor una lista cuyo unico elemento es la nota ingresada por el usuario. 
	Escribe la nota en el archivo que abre en modo 'a'."""
	nota = input("\nIngrese la nota: ")
	while True:
		etiqueta = input("\nIngrese una etiqueta de una sola palabra o presione enter para no agregarle etiqueta: ")
		if " " not in etiqueta:
			break
		print("No se admiten espacios")
	with open(PATH,'a') as f:	
		f.write(etiqueta + "|" + nota + "\n")
	print("\nNota agregada correctamente!")
	return agregar_nota_al_diccionario(d_notas,etiqueta,nota) 


def verificador_input_numerico(mensaje, minimo, maximo):
	"""Verifica un valor ingresado como numero dentro de un rango. Recibe un mensaje (cadena), un numero minimo y un numero maximo (enteros). Muestra el mensaje recibido por parametro por pantalla y espera hasta que el usuario 
	ingrese un numero entero que este entre los valores minimo y maximo (incluidos). En caso de no ingresar un numero, o que el ingresado este fuera del rango, vuelve a pedirlo.
	Finalmente devuelve el numero ingresado por el usuario."""
	while True:
		try:
			numero = int(input(mensaje))
			if numero >= minimo and numero <= maximo:
				break
			print("\nIngresaste un número que no esta entre las opciones".format(minimo,maximo))
		except ValueError:
			print("\nValor ingresado incorrecto")
	return numero


def guardar_notas_como_dic(f,d_notas):
	"""Guarda los datos de un archivo csv como diccionario. Recibe un handler del archivo notas.csv y un diccionario de notas con el formato {etiqueta1:[nota1,nota2,...],...}. Lee el archivo y guarda cada nota como un elemento de la lista asociada a la etiqueta correspondiente."""
	reader = csv.reader(f,delimiter='|')
	for linea in reader:
		if len(linea) != 2:
			raise IndexError("El formato en el cual fueron guardadas las notas en notas.csv no es el correcto. La forma correcta es etiqueta|nota, guardando una nota por linea. Por favor, cambia el nombre de dicho archivo o vacialo.")
		if not(linea[0] in d_notas):
			d_notas[linea[0]] = [linea[1].rstrip('\n')]
		else:
			d_notas[linea[0]].append(linea[1])
	return d_notas
		

def menu_principal():
	"""Función de presentación del programa de notas. Imprime un mensaje de bienvenida, y pide al usuario que ingrese una función."""
	d_notas = {}
	try:
		f = open(PATH,'r')
		d_notas = guardar_notas_como_dic(f,d_notas)
	except FileNotFoundError: #en caso que no exista previamente el archivo
		f = open(PATH,'w')
	finally:
		f.close()	
	while True:
		print("\nBienvenido a Barbara Keep!")
		accion = verificador_input_numerico("\nEscoja una de las siguientes acciones:\n1-Agregar nota\n2-Ver listado completo\n3-Buscar notas\n4-Eliminar una nota\n5-Exportar HTML\n0-Salir\n\n", 0, 5)
		if accion == 0:
			break
		elif accion == 1:
			d_notas = agregar_nota(d_notas)
		elif accion == 2:
			listar_notas(d_notas)
		elif accion == 3:
			buscar_notas(d_notas)
		elif accion == 4:
			d_notas = eliminar_nota(d_notas)
		elif accion == 5:
			exportar_html(d_notas)

			

menu_principal()