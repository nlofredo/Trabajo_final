import os
import funcion



##### REALIZAMOS UNA CLASS PARA DEFINIR COLORES PARA DETERMINADAS IMPRESIONES POR PANTALLA ######################

class bcolors:
    OK = '\033[92m' #VERDE
    ATENCION = '\033[93m' #AMARILLO
    ERROR = '\033[91m' #ROJO
    RESET = '\033[0m' #RESET COLOR
    
#################################################



##################### INICIO MENU ##################################################################
# Para la documentación:
# Se importa la librería OS a los fines del borrado de pantalla con la sentencia  os.system('cls').
# Se crean 2 funciones con el Menu Principal y el Menu Secundario, dando opciones en cada uno de ellos para su elección por el usuario.
# Dentro de cada opción, se ejecutan la funciones pertinentes.
########




def menu():
    os.system('cls')
    print (bcolors.OK + "MENU DE OPCIONES\n")
    print ("\t1 - Actualización de datos")
    print ("\t2 - Visualización de datos")
    print ("\t3 - Más Opciones")
    print (bcolors.ATENCION + "\t4 - Salir")
    
def menu2():
    os.system('cls')
    print (bcolors.OK +"OPCION DE VISUALIZACION DE DATOS\n")
    print ("\t1 - Resumen")
    print ("\t2 - Gráfico de ticker")
    print (bcolors.ATENCION + "\t3 - Salir")
    
def menu3():
    os.system('cls')
    print (bcolors.OK + "MÁS OPCIONES\n")
    print ("\t1 - Documentacion del programa")
    print (bcolors.ATENCION + "\t2 - Salir")



while True:
    # Mostramos el menu principal
    menu()
    # solicituamos una opción al usuario
    opcionMenu = input("Ingrese su opcion, por favor >> ")
    if opcionMenu=="1":
        print ("")
        input("Has pulsado la opción 1...\npulsa una tecla para continuar")
        funcion.actualizacion()
        input("Pulsa una tecla para volver al menu principal...")
    elif opcionMenu=="2":
        print ("")
        input("Has pulsado la opción 2...\npulsa una tecla para continuar")
        
        while True:
            # Mostramos el menu secundario
            menu2()
            # solicituamos una opción al usuario
            opcionMenu2 = input("Ingrese su opcion, por favor >> ")
            if opcionMenu2=="1":
                print ("")
                input("Has pulsado la opción 1...\npulsa una tecla para continuar")
                funcion.detalle()
                input("Pulsa una tecla para volver al menu principal...")
            elif opcionMenu2=="2":
                print ("")
                input("Has pulsado la opción 2...\npulsa una tecla para continuar")
                funcion.grafico()
                input("Pulsa una tecla para volver al menu principal...")
            elif opcionMenu2=="3":
                break
            else:
                print ("")
                input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")
    
    elif opcionMenu=="3":
        print ("")
        input("Has pulsado la opción 3...\npulsa una tecla para continuar")
        while True:
            # Mostramos el menu secundario
            menu3()
            # solicituamos una opción al usuario
            opcionMenu3 = input("Ingrese su opcion, por favor >> ")
            if opcionMenu3=="1":
                print ("")
                input("Has pulsado la opción 1...\npulsa una tecla para continuar")
                funcion.documentacion()
                input("Pulsa una tecla para volver al menu principal...")
            elif opcionMenu3=="2":
                break
            else:
                print ("")
                input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")
    elif opcionMenu=="4":
        print("Ud. se encuentra fuera del programa")
        break
    else:
        print ("")
        input("No has pulsado ninguna opción correcta...\npulsa una tecla para continuar")
        
        
        
###################### FIN DEL MENU ##################################################################