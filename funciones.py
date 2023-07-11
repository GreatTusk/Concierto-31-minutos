import numpy as np # Se importa numpy para trabajar con matrices

rows=10 # Se define el tamaño de las filas del lugar de eventos
columns=10 # Se define el tamaño de las columnas del lugar de eventos

asientos_0=np.arange(1,rows*columns+1).reshape(rows,columns).astype(str) # Matriz para el primer artista
asientos_1=np.arange(1,rows*columns+1).reshape(rows,columns).astype(str) # Segundo
asientos_2=np.arange(1,rows*columns+1).reshape(rows,columns).astype(str) # Tercero

matriz_matrices=np.stack([asientos_0,asientos_1,asientos_2]) # Matriz 3D que guarda todas las matrices

matriz_diccionarios=np.empty(100,dtype=object) # Matriz para guardar los diccionarios con los datos de los clientes
contador_matriz=0 # Contador para avanzar en la matriz de diccionarios y poder pasar a la siguiente persona

error="Ha ocurrido un error catastrófico." # Mensaje si se activa un bloque except

def suficiente():
    print("Se ha ingresado un dato incorrecto demasiadas veces. Abortando...")

def dato_inv(dato,vocal="o"):
    print(f"{dato} ingresad{vocal} es inválid{vocal}. Inténtelo de nuevo.") # Mensaje por defecto para cuando el usuario entregue un input inválido
      
def asientos_print(indice): # Esta función imprime las matrices según el concierto
    global matriz_matrices
    for i in range(rows):
        for j in range(columns):
            print(f"{matriz_matrices[indice][i][j]:>2s}",end=' ') # [concierto][filas][columnas]
        print()
        
def marcar_asiento(indice,asiento): # Esta funcion ocupa np.where para hallar la ubicación de un asiento en una matriz
    indices=np.where(matriz_matrices[indice] == asiento)
    fila=indices[0][0] # posición de la tupla indices correspondientes a la fila donde se halló el asiento
    columna=indices[1][0] # lo mismo para la columna
    matriz_matrices[indice][fila][columna]="X" # Se marca el asiento seleccionado con una X en [concierto][filas][columnas]
     
def eleccion_asiento(indice): # Esta función permite al usuario elegir su asiento
    global matriz_matrices
    try:
        asientos_print(indice) # Se invoca la función de imprimir los asientos para mostrarle al usuario los que están disponibles
        asiento_eleg=input("Ingrese su asiento a comprar: ")
        if not (asiento_eleg in matriz_matrices[indice]):
            dato_inv("Asiento") 
            return # Si el asiento no existe, se aborta la función
        marcar_asiento(indice,asiento_eleg) # Se invoca la función anterior para marcar el asiento seleccionado
        return int(asiento_eleg) # Se devuelve el asiento elegido, que era una str(), en forma de int() para poder usarlo después en rangos
    except:
        print(error)

def transaccion(indice,lista_compras,lista_asientos): # En esta función se hacen los cálculos para guardar las compras de cada persona
    precios=np.array([50000,100000,200000]) # Se definen los precios en una matriz [0] normales, [1] buenos, [2] premium
    maxAsiento=0 # Se inicia el contador para restringir las compras por persona
    while maxAsiento<3:
        eleccion=eleccion_asiento(indice) # Se invoca y guarda el valor retornado de la función previa
        if 0<eleccion<=20: # Se usa ese valor retornado para evaluar el precio del asiento según el rango en el que se encuentra
            lista_compras[0]+=precios[0] # Se acumulan los valores por cada compra de una persona
            lista_asientos[0][maxAsiento]=eleccion # Se guardan también los asientos comprados
        elif 20<eleccion<=70:
            lista_compras[1]+=precios[1]
            lista_asientos[1][maxAsiento]=eleccion # maxAsientos es reusado para tomar registro de cada uno de los 3 asientos que puede comprar una persona  
        elif 70<eleccion<=100:
            lista_compras[2]+=precios[2]
            lista_asientos[2][maxAsiento]=eleccion 
        maxAsiento+=1 # Se registra que se ha comprado un asiento con éxito
        if maxAsiento<3:
            try:
                continuar=int(input("¿Desea comprar otra entrada?\n1) Sí\n2) No\n")) # Se pregunta si se quiere comprar más
                match continuar: # Switch entre las alternativas
                    case 1:
                        pass # Se continúa el ciclo 
                    case 2:
                        break # Se sale del ciclo
                    case _:
                        dato_inv("Opción","a")
            except:
                print(error)
    print(f"Ha comprado {maxAsiento} asiento(s). Gracias por su compra.") # Se agradece por la compra y se muestra la cantidad de asientos comprados
    
def busqueda_r(matriz_diccionarios): # Esta función sirve para la segunda función del menú
    try:
        encontrado=False # Se empieza asumiendo que no se ha encontrado
        rut_busca=input("Ingrese su rut a buscar:\n") # Se recibe un rut, que previamente tuvo que ser ingresado en una compra
        for diccionarios in matriz_diccionarios: # Se itera sobre la matriz de diccionarios
            if diccionarios is None: # Si el diccionario aún no ha sido agregado (sigue siendo None) se salta
                continue
            elif diccionarios["Rut"]==rut_busca: # Si el rut entregado coincide con alguna entrada ["Rut"] en algún diccionario, se devuelven todos sus datos personales
                encontrado=True # Se notifica que ha sido encontrado
                print(f'Nombre: {diccionarios["Nombre"]}')
                print(f'Apellido: {diccionarios["Apellido"]}')
                print(f'Rut: {diccionarios["Rut"]}')
                print(f'Banda: {diccionarios["Banda"]}')
                print(f'Asientos comprados: {diccionarios["Asientos comprados"]}')
                print(f'Total asientos comprados: {diccionarios["Total asientos comprados"]}')
                print(f'Total gastado: ${diccionarios["Total gastado"]}')
        if not encontrado:
            dato_inv("Rut") # Se da mensaje de error si el rut no estaba en ningún diccionario
    except:
        print(error)

def validacion_pk(matriz_diccionarios,rut): # Esta función es reciclada de la anterior para comprobar si el rut proporcionado existe
    encontrado=False # Se empieza asumiendo que no se ha encontrado
    for diccionarios in matriz_diccionarios:
        if diccionarios is None: # Mismo que en la función anterior
            continue
        elif diccionarios["Rut"]==rut:
            encontrado=True # Se notifica que ha sido encontrado
    return encontrado # Se devuelve el valor de la variable. Esta va a servir para asegurarnos que no se ingresarán dos ruts iguales más adelante

'''             
def ingreso_datos(mensaje,condicion,indice):
    while True:
        nombre=input()
        condicion=condicion
        if not condicion: # El nombre debe estar compuesto de letras y tener longitud>=3 (Ej. "Leo")
            dato_inv("Nombre")
            contadores[indice]+=1
        else:
            break
        if contadores[indice]>=3:
            suficiente()
            return
    return nombre
'''
def validacion(): # Esta función guarda la primera opción del menú. Se validarán los datos del cliente antes de pasar a las compras
    global contador_matriz,primary_key,matriz_diccionarios # Se da acceso a las variables que serán necesarias
    try:
        contadores=[0,0,0,0]
        while True:
            nombre=input("Ingrese su nombre:\n")
            condicion=(len(nombre)>=3 and nombre.isalpha())
            if not condicion: # El nombre debe estar compuesto de letras y tener longitud>=3 (Ej. "Leo")
                dato_inv("Nombre")
                contadores[0]+=1
            else:
                break
            if contadores[0]>=3:
                suficiente()
                return
        while True:
            apellido=input("Ingrese su apellido:\n")
            if not (len(apellido)>=3 and apellido.isalpha()):
                dato_inv("Apellido")
                contadores[1]+=1
            else:
                break
            if contadores[1]>=3:
                suficiente()
                return
        while True:
            rut=input("Ingrese su rut sin puntos ni guion ni dígito verificador:\n")
            if not (1000000<int(rut)<30000000 and rut.isdigit() and (not validacion_pk(matriz_diccionarios,rut))): # Aquí se hace uso del valor retornado de la función validacion_pk() para asegurarnos que el rut no ha sido registrado antes
                dato_inv("Rut")
                contadores[2]+=1
            else:
                break
            if contadores[2]>=3:
                suficiente()
                return
        while True:
            try:
                banda=int(input("Ingrese el nombre del artista que va a ver:\n1) Coágulo Espátulo\n2) Joe Pino\n3) Hermanos Guarennes\n"))
                match banda: # Switch para que el usuario seleccione para qué concierto quiere comprar entradas
                    case 1:
                        banda_elegida="Coágulo Espátulo"
                        break
                    case 2:
                        banda_elegida="Joe Pino"
                        break
                    case 3:
                        banda_elegida="Hermanos Guarennes"
                        break
                    case _:
                        dato_inv("Opción","a")
                        contadores[3]+=1
                if contadores[3]>=3:
                    suficiente()
                    return
            except:
                dato_inv("Opción","a")
                contadores[3]+=1
                continue

        compras=[0,0,0] # Aquí se guardarán el total de compras por tipo de asiento. Se reincia cada vez que se invoca la función para dar paso a otra persona
        asientos_compra=[[0 for n in range(3)] for a in range(3)] # Se crea una lista 2D para guardar los asientos según el tipo
        if banda_elegida=="Coágulo Espátulo":
            transaccion(0,compras,asientos_compra) # Se invoca a transaccion(). Su primer parámetro se corresponde a la matriz 2D de los asientos, dentro de la matriz que guarda cada matriz por concierto
        elif banda_elegida=="Joe Pino":
            transaccion(1,compras,asientos_compra) # Este valor cambia según la banda elegida
        elif banda_elegida=="Hermanos Guarennes":
            transaccion(2,compras,asientos_compra) 

        diccionario = { # Se crea un diccionario para guardar todos los datos ingresados y validados hasta ahora
            "Nombre": nombre,
            "Apellido": apellido,
            "Rut": rut,
            "Banda": banda_elegida, # Se reutiliza la variable de antes, que se le había dado el rol de cambiar el valor de [concierto] en [concierto][filas][columnas]
            "Asientos comprados": asientos_compra, #[0]=normal,[1]=buenos,[2]=premium
            "Total asientos comprados": compras, #[0]=normal,[1]=buenos,[2]=premium
            "Total gastado": 0 # De momento, se deja en 0
        }
        
        total_gastado=sum(diccionario["Total asientos comprados"]) # Se suman los valores del total gastado en asientos
        diccionario["Total gastado"] = total_gastado # Y se coloca ese valor sobre la clave que habíamos dejado en 0
        
        matriz_diccionarios[contador_matriz]=diccionario # Se agrega el diccionario a la matriz de diccionarios
        contador_matriz+=1 # Se suma uno al índice de la matriz anterior, para poder pasar a la siguiente persona
        print(matriz_diccionarios)
    except:
        print(error)
                
def suma_total(matriz_diccionarios,banda): # Se define esta función para calcular la recaudación total de cada concierto
    suma=0
    for diccionarios_r in matriz_diccionarios:
        if diccionarios_r is None:
            continue # Se ignoran las entradas None dentro de la matriz
        elif diccionarios_r["Banda"]==banda: # Cuando se encuentre una entrada que corresponda a una banda, 
            suma+=diccionarios_r["Total gastado"] # se extrae el total que gastó una persona para sumarlo con todos los demás asistentes
    print(f"La recaudación total de la banda {banda} es de ${suma}") # Tras haber recorrido cada diccionario, se devuelve el total final

def menu(): # En esta función se inicia el menú para hacer uso de todas las funciones definidas hasta el momento
    global matriz_diccionarios
    print("------Compra de asientos conciertos------")
    print("Conciertos disponibles: Coágulo Espátulo, Joe Pino y Hermanos Guarennes.")
    print("Precios de los asientos: Los normales cuestan $50000, los buenos cuestan $100000 y los premium cuestan $200000.")
    activo=True
    while activo:
        print("Opciones:\n1) Comprar asiento\n2) Mostrar datos de cliente por rut\n3) Mostrar recaudación total por concierto\n4) Salir")
        try:
            eleccion=int(input("Su opción:\n"))
            match eleccion: # Switch entre las opciones disponibles
                case 1:
                    validacion() # Opción 1
                case 2:
                    busqueda_r(matriz_diccionarios) # Opción 2           
                case 3:
                    eleccion_con=int(input("Seleccione el concierto del cuál desea ver su recaudación:\n1) Coágulo Espátulo\n2) Joe Pino\n3) Hermanos Guarennes\n"))
                    match eleccion_con:
                        case 1:
                            suma_total(matriz_diccionarios,"Coágulo Espátulo")
                        case 2:
                            suma_total(matriz_diccionarios,"Joe Pino")
                        case 3:
                            suma_total(matriz_diccionarios,"Hermanos Guarennes")
                        case _:
                            dato_inv("Opción","a")
                case 4:
                    print("Gracias por su preferencia.")
                    activo=False # Se sale del programa
                case _:
                    dato_inv("Opción","a")
        except:
            print(error)
