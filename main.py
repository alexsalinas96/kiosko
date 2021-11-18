"""
productos = {
        "caramelo" : [1, 5, 100],
        "alfajor": [2, 15, 20],
        "vino": [3, 200, 10],
	    "agua": [7, 100, 60],
	    "mayonesa": [8, 55, 35],
	    "yogurt": [9, 25, 50],
        "harina" : [4, 70, 100],
        "jabon": [5, 15, 20],
        "lavandina": [6, 120, 40],
        "detergente": [10, 100, 20],
	    "fosforos": [11, 50, 50],
	    "vela": [12, 10, 50] 
}
"""
# Import json para leer el archivo
import json

# Import Tabulate para imprimir los productos de forma mas ordenada
from tabulate import tabulate 

# Data ahora es el diccionario a manejar adentro del programa
f = open("productos.json")
dicc = json.load(f)

#close el archivo original
f.close()

# Hay que usar la funcion "Dump" para actualizar el archivo json
#  json_object["d"] = 100 -> aca se actualiza el "D" al nuevo valor 100
#  a_file = open("sample_file.json", "w") -> se abre el archivo devuelta, pero ahora en modo "write"
#  json.dump(json_object, a_file) -> aca se usa dump, el primer argumento es el objecto json que ya teniamos, 
#                                   y el segundo argumento es el archivo que abrimos devuelta pero con write
#  a_file.close() -> se cierra el archivo despues de actualizar



# ---------------------------- Funciones Globales ----------------------------------------
def precio(dicc, producto):
    ''' Devuelve el precio del producto seleccionado
    '''
 
 #Falta agregar que pasa si el producto no esta en el dicc
 # o tal vez de eso se encarga otra funcion, lo que haria (creo) 
 # que todo lo de abajo no sea necesario

    try:
        #Checkeo si existe ese producto dentro de Comestibles
        if producto in dicc:
            return dicc[producto][1]

    except:
        return "Algo salio mal, pruebe devuelta"


def mostrarProductos(dicc):

    """ Muestra TODOS los productos dentro del archivo, incluidos los precios y stock
        Usamos el paquete "tabulate"
    """

    listaTabular = []

    for producto in dicc:
        listaTabular.append([producto, dicc[producto][1], dicc[producto][2]])
    
    print(tabulate(listaTabular, headers=['Producto', 'Precio ($)', 'Stock']))
    
    
    '''
    print("-------------------------------")
    espacio()

    for producto in dicc:

        print(f"{producto} - ${dicc[producto][1]} ")
        print(f"Stock disponible: cantidad {dicc[producto][2]} ")
        espacio()


    print("-------------------------------")
    '''

def sacarStock(dicc, producto, cantidad):
    
    """ Saca Stock del producto seleccionado
    """  
   
    # Abrir para actualizarlo
    f = open("productos.json", "w")

    dicc[producto][2] = dicc[producto][2] - cantidad

    #actualizo el archivo json y lo cierro.
    json.dump(dicc, f)

    f.close()

def productoExiste(dicc,producto):
    '''Returns True si existe el producto, False si no'''
    
    if producto in dicc:
        return True
    return False 

def saberStock(dicc,producto):
    '''Devuelve la cantidad de stock del producto seleccionado'''
    
    return dicc[producto][2] 

def espacio():
    '''Usar para dejar un espacio entre prints'''
    print()

# ---------------------------- Funciones Usuario ------------------------------------------

def usuarioRun():
    #terminar variable para que siga el programa hasta que el usuario haga el "checkout"
    terminar = False
    total = 0
    ticket = []

    while terminar == False:

        usuarioInput = input("Sabe lo que quiere comprar (si/no): ").lower()
        espacio()
        #Fijar que haya escrito si o no
        #if usuarioInput != "no" or usuarioInput != "si":
        #   continue

        #No sabe lo que quiere comprar
        if usuarioInput == "no":
            mostrarProductos(dicc)
            espacio()
            continue

        #Si sabe lo que quiere comprar    
        elif usuarioInput == "si":
            # contador de errores 
            errorNombreProducto = 0

            productoComprar = input("Ingrese el nombre del producto: ").lower()
        
            while not productoExiste(dicc, productoComprar):
                productoComprar = input('Fijese de escribir bien el nombre del producto: ').lower()

                errorNombreProducto += 1
                if errorNombreProducto >= 3:
                    espacio()
                    print("Por favor ingrese uno de los productos disponibles: ")
                    espacio()
                    mostrarProductos(dicc)
                    espacio()
                    errorNombreProducto = 0
                    continue

            cantidad = int(input("Cuantos quiere comprar?: "))
                
            # Si el usuario entra un numero mayor al stock disponible
            while saberStock(dicc,productoComprar) < cantidad:

                print("solo hay", saberStock(dicc,productoComprar))

                cantidad = int(input("por favor ingrese un valor menor o igual: "))
                

            # agrego el producto y cantidad al "ticket" para despues sacar stock de cada 1
            # el ticket va a ser una "lista de listas", cada producto y cantidad su propia lista
            ticket.append([productoComprar,cantidad])

            total = precio(dicc, productoComprar) * cantidad + total
            
            print(f"Su total actual es de ${total}") 
            
        else: 
            print("escriba si o no")
            continue

        continuarInput = input("Desea seguir comprando? (si/no): ").lower()

        while continuarInput != "si" and continuarInput  != "no":
            print("Solo escribir Si o No")
            espacio()
            continuarInput = input("Desea seguir comprando? (si/no): ").lower() 

        if continuarInput == "si":
            continue
        elif continuarInput == "no":
            espacio()

            print("Su compra final es: ")
            for item in ticket:
                print(f"{item[1]} {item[0]}(s)")

            print(f"Precio final: ${total}")
            
            cancelar = input("Escriba 'Fin' si esta seguro de la compra o 'Cancelar' para borrar la compra (fin/cancelar): ").lower()
            
            while cancelar != "fin" and cancelar != "cancelar":
                cancelar = input("Ingrese 'Finalizar' o 'Cancelar': ")

            terminar == True
            break
            
    if cancelar == "fin":
        #Loop para sacar stock de cada producto del ticket     
        for item in ticket:
            # 1 por ahora, mas adelante va a ser dependiendo cuantos compre de cada 1
            sacarStock(dicc, item[0], item[1])
        print(f"Su total es ${total}")
        print("Gracias por comprar!")

    else:
        print("Se cancelo la compra.")


# ---------------------------- Funciones Administrador ------------------------------------------
def agregarStock(dicc, producto, cantidad):

    """ Solo cambia la cantidad de stock del producto seleccionado
    """

    # Abrir para actualizarlo
    f = open("productos.json", "w")

    dicc[producto][2] = dicc[producto][2] + cantidad

    #actualizo el archivo json y lo cierro.
    json.dump(dicc, f)

    f.close()

def agregarProducto(dicc, producto, precio, cantidad):
    
    ''' Se agrega un producto totalmente nuevo al json. El id es lo que seria el identificador de cada
    producto si fuera un kiosko real, por eso se necesita que cada id sea diferente. Como estamos 
    haciendo el diccionario/json de forma ordenada, basta con saber cual es el id del ultimo producto
    y sumarle 1
    '''

    # para agarrar el ultimo elemento del diccionario -> list(dicc)[-1]
    ultimoProducto = list(dicc)[-1]

    ultimoId = dicc[ultimoProducto][0] + 1 # necesitamos que sea un nuevo id, por eso agrego el +1

    # Abrir para actualizarlo
    f = open("productos.json", "w")

    # Agrego el nuevo producto al diccionario
    dicc[producto] = [ultimoId,precio,cantidad]

    #actualizo el archivo json y lo cierro.
    json.dump(dicc, f)

    f.close()

def eliminarProducto(dicc, producto):
   
    """ borra el key-value completamente del archivo
    """
    
    # Abrir para actualizarlo
    f = open("productos.json", "w")

    # Borra el "objeto". En python el key-value es un objeto, y por eso se puede borrar con del
    # otra forma seria usando .pop -> dicc.pop(producto) 
    del dicc[producto]

    #actualizo el archivo json y lo cierro.
    json.dump(dicc, f)

    f.close() 

#def checkIfNumber(x):


def adminRun():
    
    print("(1) Agregar producto nuevo")
    print("(2) Agregar Stock")
    print("(3) Eliminar producto")
    espacio()

    userInput = input("Que desea hacer: ").lower()

    while userInput != "1" and userInput != "2" and userInput != "3":
        userInput =  input("Elija 1, 2 o 3: ").lower()

    # Agregar producto nuevo
    if userInput == "1":
        
        productoNuevo = input("Escriba el nombre del producto: ").lower()

        # Si el producto ya esta agregado, entra a este while y le pregunta devuelta
        while productoExiste(dicc, productoNuevo):
            print("Ese producto ya existe, escriba uno que no este")
            espacio()
            productoNuevo = input("Escriba el nombre del producto: ").lower()
       

        stockNuevo = input(f"Escriba la cantidad a agregar de {productoNuevo}: ")

        while not stockNuevo.isnumeric():
            stockNuevo = input(f"La cantidad a agregar debe ser un numero: ")

        '''
        # Uso este try except para que no se rompa el programa si el usuario no ingresa un numero
        # Preferimos que se agreguen 0 para que el programa pueda continuar. No pudimos solucionar
        # la forma de solo aceptar un numero
        try:
            stockNuevo = int(stockNuevo)
        except:
            print("Debe escribir un numero entero. Se agregaran 0 del producto, puede modificarlo cuando quiera")
            stockNuevo = 0
        '''
        
        precioNuevo = input(f"Escriba el precio de {productoNuevo}: $")
        espacio()

        while not precioNuevo.isnumeric():
            print("El precio debe ser un numero!")
            espacio()
            precioNuevo = input(f"Escriba el precio de {productoNuevo}: $")

        '''
        # Uso este try except para que no se rompa el programa si el usuario no ingresa un numero
        try:
            precioNuevo = int(precioNuevo)
        except:
            print("Debe escribir un numero entero. El producto vale $0, puede modificarlo cuando quiera")
            precioNuevo = 0
        '''
        # Una vez listo, se agrega el producto
        agregarProducto(dicc, productoNuevo, precioNuevo, stockNuevo)
        print(f"{productoNuevo} se agrego correctamente")

    elif userInput == "2":

        producto = input("Ingrese el producto a agregar stock: ").lower()

        while not productoExiste(dicc, producto): 
            producto = input(f"{producto} no existe. Ingrese un producto que si este: ").lower()
        
        stockNuevo = input("Ingrese la cantidad a agregar: ")

        try:
            stockNuevo = int(stockNuevo)
        except:
            print("No ingreso un numero, el producto quedara con la misma cantidad. Intente denuevo.")
            stockNuevo = 0
        
        if stockNuevo != 0:
            agregarStock(dicc, producto, stockNuevo)
            print(f"Ahora hay de {producto} {saberStock(dicc, producto)} en stock")

    elif userInput == "3":

        producto = input("Escriba el nombre del producto a eliminar: ").lower()

        while not productoExiste(dicc, producto):
            producto = input("Ese producto no existe, escriba uno que si este: ")
        
        seguro = input(f"{producto} va a ser eliminado definitivamente, esta seguro (si/no): ").lower()
        
        while seguro != "si" and seguro != "no":

            seguro = input("Solo escriba 'si' o 'no': ").lower()

        if seguro == "si":
            eliminarProducto(dicc, producto)
            print(f"{producto} se elimino correctamente")
        else:
            print(f"{producto} no se eliminara")
            


#----------------------------- Programa Principal ----------------------------------------



print("Bienvenido")
espacio()
userInput = input("Es un usuario o un Administrador? (user/admin): ").lower()
espacio()

while userInput != "user" and  userInput != "admin":
    userInput = input("Escriba 'user' o 'admin': ").lower()

'''

# Si el que maneja el programa es un usuario
if userInput == "user":

    #terminar variable para que siga el programa hasta que el usuario haga el "checkout"
    terminar = False
    total = 0
    ticket = []

    while terminar == False:

        usuarioInput = input("Sabe lo que quiere comprar (si/no): ").lower()
        espacio()
        #Fijar que haya escrito si o no
        #if usuarioInput != "no" or usuarioInput != "si":
        #   continue

        #No sabe lo que quiere comprar
        if usuarioInput == "no":
            mostrarProductos(dicc)
            espacio()
            continue

        #Si sabe lo que quiere comprar    
        elif usuarioInput == "si":
            # contador de errores 
            errorNombreProducto = 0

            productoComprar = input("Ingrese el nombre del producto: ").lower()
        
            while not productoExiste(dicc, productoComprar):
                productoComprar = input('Fijese de escribir bien el nombre del producto: ').lower()

                errorNombreProducto += 1
                if errorNombreProducto >= 3:
                    espacio()
                    print("Por favor ingrese uno de los productos disponibles: ")
                    espacio()
                    mostrarProductos(dicc)
                    espacio()
                    errorNombreProducto = 0
                    continue

            cantidad = int(input("Cuantos quiere comprar?: "))
                
            # Si el usuario entra un numero mayor al stock disponible
            while saberStock(dicc,productoComprar) < cantidad:

                print("solo hay", saberStock(dicc,productoComprar))

                cantidad = int(input("por favor ingrese un valor menor o igual: "))
                

            # agrego el producto y cantidad al "ticket" para despues sacar stock de cada 1
            # el ticket va a ser una "lista de listas", cada producto y cantidad su propia lista
            ticket.append([productoComprar,cantidad])

            total = precio(dicc, productoComprar) * cantidad + total
            
            print(f"Su total actual es de ${total}") 
            
        else: 
            print("escriba si o no")
            continue

        continuarInput = input("Desea seguir comprando? (si/no): ").lower()

        while continuarInput != "si" and continuarInput  != "no":
            print("Solo escribir Si o No")
            espacio()
            continuarInput = input("Desea seguir comprando? (si/no): ").lower() 

        if continuarInput == "si":
            continue
        elif continuarInput == "no":
            terminar == True
            break
            

    #Loop para sacar stock de cada producto del ticket     
    for item in ticket:
        # 1 por ahora, mas adelante va a ser dependiendo cuantos compre de cada 1
        sacarStock(dicc, item[0], item[1])


    print(f"Su total es ${total}")
    print("Gracias por comprar!")

# Si el que maneja el programa es un administrador
else:
    print("(1) Agregar producto nuevo")
    print("(2) Agregar Stock")
    print("(3) Eliminar producto")
    espacio()

    userInput = input("Que desea hacer: ").lower()

    while userInput != "1" and userInput != "2" and userInput != "3":
        userInput =  input("Elija 1, 2 o 3: ").lower()

    # Agregar producto nuevo
    if userInput == "1":
        
        productoNuevo = input("Escriba el nombre del producto: ").lower()

        # Si el producto ya esta agregado, entra a este while y le pregunta devuelta
        while productoExiste(dicc, productoNuevo):
            print("Ese producto ya existe, escriba uno que no este")
            espacio()
            productoNuevo = input("Escriba el nombre del producto: ").lower()
       

        stockNuevo = input(f"Escriba la cantidad a agregar de {productoNuevo}: ")

        # Uso este try except para que no se rompa el programa si el usuario no ingresa un numero
        # Preferimos que se agreguen 0 para que el programa pueda continuar. No pudimos solucionar
        # la forma de solo aceptar un numero
        try:
            stockNuevo = int(stockNuevo)
        except:
            print("Debe escribir un numero entero. Se agregaran 0 del producto, puede modificarlo cuando quiera")
            stockNuevo = 0
        
        
        precioNuevo = input(f"Escriba el precio de {productoNuevo}: $")
        
        # Uso este try except para que no se rompa el programa si el usuario no ingresa un numero
        try:
            precioNuevo = int(precioNuevo)
        except:
            print("Debe escribir un numero entero. El producto vale $0, puede modificarlo cuando quiera")
            precioNuevo = 0
        
        # Una vez listo, se agrega el producto
        agregarProducto(dicc, productoNuevo, precioNuevo, stockNuevo)

    elif userInput == "2":

        producto = input("Ingrese el producto a agregar stock: ").lower()

        while not productoExiste(dicc, producto): 
            producto = input(f"{producto} no existe. Ingrese un producto que si este: ").lower()
        
        stockNuevo = input("Ingrese la cantidad a agregar: ")

        try:
            stockNuevo = int(stockNuevo)
        except:
            print("No ingreso un numero, el producto quedara con la misma cantidad. Intente denuevo.")
            stockNuevo = 0
        
        if stockNuevo != 0:
            agregarStock(dicc, producto, stockNuevo)
            print(f"Ahora hay de {producto} {saberStock(dicc, producto)} en stock")

    elif userInput == "3":

        producto = input("Escriba el nombre del producto a eliminar: ").lower()

        while not productoExiste(dicc, producto):
            producto = input("Ese producto no existe, escriba uno que si este: ")
        
        seguro = input(f"{producto} va a ser eliminado definitivamente, esta seguro (si/no): ").lower()
        
        while seguro != "si" and seguro != "no":

            seguro = input("Solo escriba 'si' o 'no': ").lower()

        if seguro == "si":
            eliminarProducto(dicc, producto)
            print(f"{producto} se elimino ")
        else:
            print(f"{producto} no se eliminara")
            

     

'''  
if userInput == "user":
    usuarioRun()
else:
    adminRun()
# ------------ Testing Program / Functions--------------------------

#mostrarProductos(dicc)