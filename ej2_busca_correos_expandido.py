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

# Se procesan los argumentos recibidos por el script en Python.
# Se captura la excepción SystemExit para poder salir con el código de salida que se pide en el ejercicio 2 y no con el código de salida que genere parser.parse_args().

try:
        args=parser.parse_args()
except SystemExit as e:
    print("La sintaxis de este script es: ej2_busca_correos_expandido.py [-r] [-t] [-d dom] [-e {d,t,c}] [-f RegExp] [-o {a,d,l}] Dir ")
    exit(20)

# Para ejecutar el script del ejercicio 1, se crea una lista que contendrá el comando a ser ejecutado y todos los argumentos que va a recibir.
# El primer elemento de esta lista determina el comando a ser ejecutado, y por tanto será el camino absoluto al script en bash del ejercicio 1 
# (esto permite independizarse del directorio corriente de trabajo).

bash_script_parametros= ['/home/garto/Documents/Obligatorio-DevOps/ej1_busca_correos.sh']


#Si el usuario a elegido que la busqueda sea recursiva, tenemos que pasarle el parametro -r al script "ej1_busca_correos.sh"
#Con el append lo colocamos al final de la linea

if args.recursivo:
        bash_script_parametros.append("-r")


#Si el usuario a elegido que la busqueda de archivos sea solo .txt , tenemos que pasarle el parametro -t parametro al script "ej1_busca_correos.sh"
#Con el append lo colocamos al final de la linea

if args.texto:
        bash_script_parametros.append("-t")

#Si el usuario a elegido que la busqueda de correos sea con determinado dominio , tenemos que pasarle el parametro -d parametro al script "ej1_busca_correos.sh"
#Con el append lo colocamos al final de la linea

if args.dominio:
        bash_script_parametros.append("-d")
        bash_script_parametros.append(args.dominio)
# La opcion d la lista la cantidad de correos para cada dominio encontrado.

        


#Si el usuario a elegido que la busqueda de correos sea con determinado dominio , tenemos que pasarle el dominio que eligio al script "ej1_busca_correos.sh".
#Con el append lo colocamos al final de la linea
#Al script "ej1_busca_correos.sh" hay que pasarle en que directorio buscar los correos por ende hay que cargarle el parametro directorio a "ej1_busca_correos.sh".
#Con el append lo colocamos al final de la linea

bash_script_parametros.append(args.directorio)

# Para obtener la salida estándar, la salida estándar de errores y el código de salida del script del ejercicio 1, se usa Popen, pasándole el
# comando con sus argumentos como una lista (cargada en la variable bash_script_parametros), donde el primer elemento es el comando y los siguientes son sus parámetros. 
# Después de esa lista, a Popen se le pasa stdout = PIPE y stderr = PIPE para poder recuperar después la salida estándar y la salida estándar de errores.

process = Popen (bash_script_parametros,stdout=PIPE,stderr= PIPE)

# Process permite ejecutar el comando solicitado y acceder a la información que produce.
# Para obtener el código de retorno, la salida estándar y la salida estándar de errores del script del ejercicio 1 
# es necesario ejecutar el método communicate de este objeto (este método causa la ejecución del ejercicio 1).
# El método communicate retorna una la salida y la entrada estándar (stdoutdata, stderrdata).
# La variable output será la salida estándar como primer elemento y la salida estándar de errores como segundo elemento.

output= process.communicate()

if process.returncode > 0:
 # Se despliega el mensaje producido por el script del ejercicio 1 por
 # la salida estándar de errores.
 # Se usa el método decode para formatear correctamente la salida para
 # ser impresa. Podría usarse en este caso también .decode('utf-8').
 print(output[1].decode(), file = sys.stderr, end="")
 # Se finaliza la ejecución del programa con el mismo código de error
 # que el script del ejercicio 1.
 exit(process.returncode)

if output[1].decode() != "":
 print(output[1].decode(), file=sys.stderr, end="")
 exit(0)

lista_correos = output[0].decode().split("\n")

lista_correos.pop(-1)
lista_correos.pop(-1)

if args.regexp != None:
    try:
        patron = re.compile(args.regexp)
    except Exception as e:
        print("La expresión regular ingresada no es correcta. Ingrese una expresión regular valida.", file=sys.stderr)
        exit(10)
    correos_filtrados = []
    # Se filtran las líneas de correos con la expresión regular indicada.
    for correo in lista_correos:
        if patron.match(correo):
            # Se adiciona el correo a la lista de correos filtrados.
            correos_filtrados.append(correo)
    # Luego de crear la lista de correos filtrados según la expresión regular, se cambia la lista original por la lista filtrada.
    #cat archivo_filtrado
    lista_correos=correos_filtrados

if args.ordenar == "a":
        lista_correos.sort(key=lambda elemento:(elemento.split("@")[0])) #Ordena los correos de la lista alfabeticamente lambda personaliza la manera en la cual se va a ordenar, en este caso se ordenara por el primer parametro antes del "@"
        for i in lista_correos:
                print(i)
        print("")

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
