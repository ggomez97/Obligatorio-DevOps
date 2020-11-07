#!/bin/bash

#ej1_busca_correos  [-r]  [-t] [-d dominio]  Directorio

#Cargamos en la variable recursivo el valor "-maxdepth 1" de manera de hacer a find no recursivo llegado el momento
#en caso de que se pase el parametro -r esta variable debera vaciarse.

recursivo="-maxdepth 1"
archivo="[a-zA-Z0-9\._-]*"
dominio="[a-zA-Z0-9\._]*.$"

#El siguiente if comprueba que la cantidad de parametros es correcta debe ser entre 1 y 5 parametros.

if [ $# -lt 1 ] || [ $# -gt 5 ]
then
   echo "Cantidad de parametros incorrecta solo se aceptan los parametros [-r] [-t] [-d dominio] Directorio" >&2
   exit 4
fi

while getopts "rtd:" parametro
do
    case $parametro in
        r) #Si esta presente el parametro "-r" procedemos a vacial la variable recursivo
           #de manera que find no use "-maxdepth 1"
           recursivo=""
        ;;

        t) #Busca solamente correos en archivos regulares y no ocultos con extencion .txt
           echo "pasaste parametro -t"
           archivo="*.txt"

        ;;

        d) #Si esta presente el parametro "-d" debemos buscar los correos del dominio entrado como parametro a continuación del "-d"
           #para esto guardaremos en la variable dominio el parametro ingresado a continuacion del "-d"

	         dominio="$OPTARG"
        ;;

        *) #Si  se  recibe  un  modificador  inválido,  se  deberá  desplegar  el  mensaje  de  error  “Modificador
           #<modificador  pasado  como parámetro> incorrecto,  solo  se  acepta -r, -t  y -d.”  por  la  salida estándar de errores
           #y se devolverá un 5 como código de retorno del script.

           echo "Modificador $parametro incorrecto,  solo  se  acepta -r, -t  y -d.”" >&2
           exit 5

        ;;
    esac
done

#Borraremos los parametros ya usados utilizando un shift de manera de quedarnos con dos parametros en caso de haber usado un -d y con un
#parametro en caso de no haber usado el -d

shift $((OPTIND-1))

#Ahora comprobamos de no tener mas de 2 parametros, lo cual seria un error desplegariamos el mensaje por la salida estandar de errores y
#terminariamos el programa con un codigo de salida 6

if [ $# -gt 1 ]
then
   echo "La cantidad de parametros es incorrecta solo se reciben los parametros [-r] [-t] [-d dominio] Directorio" >&2
   exit 6

elif [ $# -eq 1 ]
then
   #Si S# es igual a 1 quiere decir que no se utilizo el parametro -d por lo tanto $1 es nuestro parametro directorio
   #y lo guardamos en la variable directorio
   directorio=$1
fi

#Transformamos la variable directorio en caso de que no sea un camino absoluto utilizando "pwd"

if ! echo "$1"| grep -q "^/"
then
directorio=$(pwd)"/$1"
fi

#Probar que $directorio es un directorio y que tenemos permisos


find "$recursivo" "$archivo" "$directorio" | egrep -o "^[a-zA-Z0-9\._]*@$dominio"

#PRUEBAS
echo "recursivo $recursivo dominio $dominio directorio $directorio"