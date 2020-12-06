#/usr/bin/python3
# -*- coding: utf-8 -*-

#ej2_busca_correos_expandido.py [-r] [-t] [-d dom] [-e {d,t,c}] [-f RegExp] [-o {a,d,l}] Dir


#La funcion Popen del moduulo subprocess permite ejecutar comandos de Linux
#en python y PIPE permite manejar la salida estandar y entrada estandar de errores. 
from subprocess import Popen, PIPE
import sys #Permite  acceder a los parametros recibidos
import re #Permite manejar expreciones regulares
import argparse #Permite interpretar los parametros recibidos.

parser = argparse.ArgumentParser()

parser.add_argument("-r", "--recursivo", help="Busca los arvhivos en forma recursiva a partir del directorio pasado como paramentro.", action="store_true")

parser.add_argument("-t","--texto",help="Busca solo los arvhivos regulares no ocultos con extencion .txt.",action="store_true")

parser.add_argument("-d","--dominio", type=str, help="Buscasolo los correos de ese dominio.")

parser.add_argument("-e","--encontrados", type=str, choices=["d","t","c"], help="Desplega cantidad de correos electronicos encontrados por dominio (opcion d) \
por cantidad de dominios diferentes encontrados opcion (t) y con la opcion (c) despliega la cantidad de correos como la cantidad de dominios diferentes encontrados.")

parser.add_argument("-f", "--regexp", help="Despliega y contabiliza solo correos electronicos que cumplan con la exprecion regular precedida del parametro (-f).")

parser.add_argument("-o","--ordenar",type=str, choices=["a","d","l"],help="Ordena la salida de correos, con la opcion (o) ordena los correos aflabeticamente, con la opcion (d) \
ordena los correos por alfabeticamente creciente por dominio y con la opcion (l) ordena los correos por su largo de caracteres en forma creciente.")

parser.add_argument("directorio",type=str,help="Directorio donde se va a hacer la busqueda.")

# Se procesan los argumentos recibidos por el script en Python en la variable args.
# Se captura la excepción SystemExit para poder salir con el código de salida que se pide en el ejercicio 2 y no con el código de salida que genere parser.parse_args().

try:
        args=parser.parse_args()
except SystemExit as e:
    print("La sintaxis de este script es: ej2_busca_correos_expandido.py [-r] [-t] [-d dom] [-e {d,t,c}] [-f RegExp] [-o {a,d,l}] Dir ")
    exit(20)

# Para ejecutar el script del ejercicio 1, se crea una lista que contendrá el comando a ser ejecutado y todos los argumentos que va a recibir.
# El primer elemento de esta lista determina el comando a ser ejecutado, y por tanto será el camino absoluto al script en bash del ejercicio 1 

bash_script_parametros= ['/home/garto/Documents/Obligatorio-DevOps/ej1_busca_correos.sh']

#En lo siguientes IF segun con que parametros el usuario a ejecutado el script de python se iran agregando al final de la lista bash_script_parametros.
#Estos parametros se iran agegando con append ya que lo agraga al final de la linea de la lista bash_script_parametros.

if args.recursivo:
        bash_script_parametros.append("-r")

if args.texto:
        bash_script_parametros.append("-t")

#En el caso que el usuario agrege el parametro -d obligatoriamente tiene que agregar un dominio.
if args.dominio:
        bash_script_parametros.append("-d")
        bash_script_parametros.append(args.dominio)

#Obligatoriamente tiene que ejecutarse con un directorio para iniciar la busqueda ya que el ej1_busca_correos.sh es demandante con este parametro..

bash_script_parametros.append(args.directorio)

# Para obtener la salida estándar, la salida estándar de errores y el código de salida del script del ejercicio 1, se usa la funcion Popen, pasándole el
# comando con sus argumentos como una lista (cargada en la variable bash_script_parametros), donde el primer elemento es el comando y los siguientes son sus parámetros. 
# Luego esa lista, a Popen se le pasa stdout = PIPE y stderr = PIPE como argumento  para poder recuperar después la salida estándar y la salida estándar de errores.

process = Popen (bash_script_parametros,stdout=PIPE,stderr= PIPE)

# Process es un objeto que permite ejecutar la funcion solicitada (Popen) y acceder a la información que produce.
# Esta informacion nos permite obtener el código de retorno, la salida estándar y la salida estándar de errores del script del ejercicio 1.

# Al ejecutar el método communicate de este objeto se ejecuta el comando que existe en la lista bash_script_parametros.
# Este retorna una la salida y la entrada estándar (stdoutdata, stderrdata).
# La variable output será la salida estándar y la salida estándar de errores.

output= process.communicate()

#Este if process.retunrcode retorna el codigo de retorno (exit code) del script ej1_busca_correos.sh que fue ejecutado anteriormente.
#Si cumple la condicion de que el codigo sea distinto de 0 se despliega el mensaje que produjo el script del ejericio 1 por la salida standar de errores.
#Se utiliza el metodo decode para formatear la salida standard de errores al ser impresa.
# Se finaliza la ejecución del programa con el mismo código de error que el script del ejercicio 1.
#Si este es 0 significa que no hay error.

if process.returncode > 0:
  print(output[1].decode(), file = sys.stderr, end="")
#Se finaliza la ejecucion del programa con el mismo codigo de error que el script 1.
 exit(process.returncode)

#Verificamos que se recibio la informacion por la entrada estandar de errores.
#Muestra el mensaje que genera el script 1 por su salida estandar de errores en caso de que no existan archivos para listar.
if output[1].decode() != "":
 print(output[1].decode(), file=sys.stderr, end="")
 exit(0)

#En esta lista_correos se cargan todos los correos que enviados por el output del ejercicio1.        
lista_correos = output[0].decode().split("\n")

#Se le borran los ultimos 2 elementos de la lista ya que no son necesarios para continuar con este script.
lista_correos.pop(-1)
lista_correos.pop(-1)

#Una vez ya ejecutado y recibido el output del ejercicio1, si el script 2 recibe el parametro "-f"
 #se ejecuta el siguiente IF.
#Este realiza una transformacion de la exprecion regular ingresada y la ingresa a la variable "patron".
#Si la exprecion regular ingresada no es correcta despliega un mensaje de error sobre la misma
 #por la salida standar de erorres utilizando el codigo de salida 10.
if args.regexp != None:
    try:
        patron = re.compile(args.regexp)
    except Exception as e:
        print("La expresión regular ingresada no es correcta. Ingrese una expresión regular valida.", file=sys.stderr)
        exit(10)
  #Se crea la lista de los correos filtrados.
    correos_filtrados = []
    # Se filtran las líneas de correos con la expresión regular indicada.
    for correo in lista_correos:
        if patron.match(correo):
            # Se adiciona el correo a la lista de correos filtrados.
            correos_filtrados.append(correo)
    # Luego de crear la lista de correos filtrados según la expresión regular, se cambia la lista original por la lista filtrada.
    #cat archivo_filtrado
    lista_correos = correos_filtrados

#Una vez que se tiene la nueva lista de correos con los correos filtrados (si es que se le ingresa el parametro -f)
 #si el parametro -o fue ingresado con la opcion a (-oa) entra en el siguiente IF.
#Este IF ordena los correos alfabeticamente separando por elementos tomando como separador el @ siendo 0 el correo
 # y 1 el dominio.
#La funcion lamda esta asociada al parametro key, lo que nos permite definir los valores a ser usados por el sort.
#En este caso la funcion lambda esta tomando el parametro incial (0) que corresponde a los correos 
 # ya que utilizamos el metodo .split separando cada string de cada posicion de la lista, tomando como separador el @ 
 # para luego ser ordenados por el sort.
#Luego imprime la lista de correos ordenada alfabeticamente respetando el formato de 1 correo por linea.

if args.ordenar == "a":
        lista_correos.sort(key=lambda elemento:(elemento.split("@")[0]))
        for i in lista_correos:
                print(i)
        print("")
#Esta IF funciona exactamente que el anterior pero con la diferencia de que este ordena aflabeticamente por DOMINIO.
elif args.ordenar == "d":
        lista_correos.sort(key=lambda elemento:(elemento.split("@")[1])) #Ordena los dominios de los correos de la lista alfabeticamente
        for i in lista_correos:
                print(i)
        print("")
        
elif args.ordenar == "l":
        lista_correos.sort(key=len) #Con key=len se ordenaran los elementos de la lista por el largo de manera acendente
        for i in lista_correos:
                print(i)
        print("")
        print("Cantidad de correos electrónicos encontrados en el directorio",args.directorio,":",len(lista_correos),"\n")
        

if args.encontrados == "d":          
        dominios_cant = {}
        print("Reporte cantidad de correos encontrados por dominio:")
       
        for correo in lista_correos:
                dominio=correo.split("@")[1]
                if dominio not in dominios_cant:
                        dominios_cant[dominio] = 1
                else:
                        dominios_cant[dominio] += 1
        for dominio in dominios_cant:
                print (dominio,"-", dominios_cant[dominio])
        

elif args.encontrados == "t":
        lista_dominios = []
        for correo in lista_correos:
                dominio=correo.split("@")[1]
                if dominio not in lista_dominios:
                        lista_dominios.append(dominio)
        for i in lista_correos:
                print(i)
        print("Cantidad de dominios diferentes encontrados:",len(lista_dominios))

elif args.encontrados == "c":
        dominios_cant = {}
        print("Reporte cantidad de correos encontrados por dominio:")
        for correo in lista_correos:
                dominio=correo.split("@")[1]
                if dominio not in dominios_cant:
                        dominios_cant[dominio] = 1
                else:
                        dominios_cant[dominio] += 1
        for dominio in dominios_cant:
                print (dominio,"-" ,dominios_cant[dominio])
        lista_dominios = []
        for correo in lista_correos:
                dominio=correo.split("@")[1]
                if dominio not in lista_dominios:
                        lista_dominios.append(dominio)
        print("La cantidad de dominios diferentes encontrados es: " + str(len(lista_dominios))) #Con str convertimos la lista en string para que se pueda concatenar

if args.ordenar == None and args.encontrados == None and args.regexp == None:
        for i in lista_correos:
                print(i)
