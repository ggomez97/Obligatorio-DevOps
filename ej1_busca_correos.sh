#!/bin/bash

#ej1_busca_correos  [-r]  [-t] [-d dominio]  Directorio

#Inicializamos la variable recursivo el valor "-maxdepth 1" de manera de hacer a find no recursivo llegado el momento
#en caso de que se pase el parametro -r esta variable debera vaciarse.
recursivo="-maxdepth 1"

#Inicializamos en la variable "archivo" el caracter "*" para utilizarlo como nombre de archivo a buscar, en caso
#de utilizar el argumento "-t" se sobrescribira esta variable
archivo="*"

#Inicializamos la variable "dominio" para utilizar en el "grep", debe ser una letra mayuscula o minuscula seguida por
#cualquier combinacion de números letras mayusculas o minusculas guiones bajos y puntos. Esta se sobre escribira en caso
#de pasar el argumento "-d" por la entrada del usuario.
dominio="[A-Za-z0-9][A-Za-z0-9_.]*"

#El siguiente if comprueba que la cantidad de parametros es correcta debe ser entre 1 y 5 parametros.

if [ $# -lt 1 ] || [ $# -gt 5 ]
then
   echo "Cantidad de parámetros incorrecta, solo se recibenlos modificadores -r, -t, -d dominio y un directorio accesible en el sistema de archivos." >&2
   exit 4
fi

while getopts ":rtd:" parametro
do
    case $parametro in
        r) #Si esta presente el parametro "-r" procedemos a vacial la variable recursivo
           #de manera que find no use "-maxdepth 1"
           recursivo=""
        ;;

        t) #Busca solamente correos en archivos regulares y no ocultos con extencion .txt
           archivo="*.txt"

        ;;

        d) #Si esta presente el parametro "-d" debemos buscar los correos del dominio entrado como parametro a continuación del "-d"
           #para esto sobre escribimos la variable dominio el parametro ingresado a continuacion del "-d"

	         dominio="$OPTARG"
               #Comprobamos que el dominio ingresado no comience con punto o guión bajo./
               if echo "$dominio" | grep -q "^[._]"
               then
               echo "Debe ingresar un dominio que no comience con punto o guion" >&2
               exit 2
               fi
        ;;

        *) #Si  se  recibe  un  modificador  inválido,  se  deberá  desplegar  el  mensaje  de  error  “Modificador
           #<modificador  pasado  como parámetro> incorrecto,  solo  se  acepta -r, -t  y -d.”  por  la  salida estándar de errores
           #y se devolverá un 5 como código de retorno del script.

           echo "Modificador -$OPTARG incorrecto,  solo  se  acepta -r, -t  y -d." >&2
           exit 5

        ;;
    esac
done

#Borraremos los parametros ya usados utilizando un shift de manera de quedarnos con dos parametros en caso de haber usado un -d y con un
#parametro en caso de no haber usado el -d

shift $((OPTIND-1))

#Ahora comprobamos de no tener mas de 2 parametros, lo cual seria un error desplegariamos el mensaje por la salida estandar de errores y
#terminariamos el programa con un codigo de salida 4

if [ $# -gt 1 ]
then
   echo "Cantidad de parámetros incorrecta, solo se recibenlos modificadores -r, -t, -d dominio y un directorio accesible en el sistema de archivos." >&2
   exit 4

elif [ $# -eq 1 ]
then
   #Si S# es igual a 1 quiere decir que no se utilizo el parametro -d por lo tanto $1 es nuestro parametro directorio
   #y lo guardamos en la variable directorio
   directorio=$1
fi

#Sustituimos la variable directorio en caso de que no sea un camino absoluto utilizando removiendo "./" del comienzo
#con un sed y agregandole el "pwd" adelante
if echo "$directorio" | grep -q "^./"
then
   dirtemp=$(echo "$directorio" | sed 's/\.//')
   directorio=$(pwd)"$dirtemp"
fi

#Sustituimos la variable directorio en caso que haya sido pasada como camino relativo sin agregarle "./" delante
if ! echo "$directorio"| grep -q "^/"
then
   directorio=$(pwd)"/$directorio"
fi

#Probar que $directorio existe.
if ! test -a "$directorio"
then
echo  El directorio $directorio no existe >&2
exit 1
fi

#Prueba que el directorio es un directorio y no un archivo
if ! test -d "$directorio"
then
echo El parámetro $directorio no es un directorio >&2
exit 2
fi

#Prueba que se tenga los permisos necesarios
if ! ([ -r "$directorio" ] && [ -x "$directorio" ])
then
echo No se tienen los permisos necesarios para acceder al directorio y buscar correos >&2
exit 3
fi

#Procedemos a realizar la busqueda mediante un grep con las opciones "-o" para que busque solo las coincidencias y no toda la linea
#además un "-h" para que no me ponga como prefijo el archivo donde encontro la expreción.
#Nuestra expreción cuenta de 3 partes una que es cualquier combinacion de letras mayusculas o minusculas,
#números puntos o guiones bajos "[A-Za-z0-9_.]*", 
#seguido de un @ que no puede estar precedido de un punto o guion bajo "[A-Za-z0-9]@",
#y una tercer parte que sera la variable "$dominio" que esta precargada que no puede iniciar con punto o guion bajo
#pero luego puede seguir con cualquier combinacion de letras números puntos o guiones bajos "[^._][A-Za-z0-9_.]*"
#a no ser que se haya puesto el parametro "-d" en tal caso tendra cargado el parametro que hayamos puesto luego del "-d"
#Este grep buscara dichas expresiones en los archivos resultantes de la ejecucion del comando find en la variable "$directorio" la cual
#tiene cargado el camino absoluto al directorio que pasamos como parametro, luego vendra la variable "$recursivo" que tiene guardado "-maxdepth 1"
#y en caso de haber pasado -r estará vacia de manera que el find sea recursivo, luego viene el -name seguido de la variable "$archivo" la cual está
#precargada con ".*" para buscar en todos los archivos ya sea ocultos o no o en caso de haber pasado -t tendra cargado "*.txt" de manera de buscar solo
#los archivos no ocultos con extencion ".txt" seguido de un -type f para que busque solo archivos regulares.
#Esta salida la redireccionamos a un archivo "temp"

grep -oh "[A-Za-z0-9_.]*[A-Za-z0-9]@$dominio" $(find "$directorio" $recursivo -name "$archivo" -type f)>temp

#Comprobamos que el archivo temporal no este vacio, en caso de que este vacio saldremos con el mensaje adecuado
#y salgo un codigo de 0
if [ $(wc -l < temp) -eq 0 ]
then
   echo "No se han encontrado correos en el directorio $directorio"
   rm temp #Borramos el archivo temporal que creamos
   exit 0
fi

#Realizamos un cat de el archivo "temp" para que liste los correos que hemos encontrado
cat temp

#Imprimimos en pantalla mediante un echo La cantidad de correos encontrados en "$directorio"(camino absoluto pasado como parametro) es:
#Ejecutamos un wc -l pasandole a su entrada estandar el archivo "temp" de manera de obtener solo el numero y el archivo que pasamos para contar
#esto se podria sustituir por un "cat temp | wc -l"
echo "La cantidad de correos en "$directorio" es: "$(wc -l < temp)

#Procedemos a borrar el archivo temporal que creamos previamente
rm temp

#Salimos con codigo 0 sin errores
exit 0