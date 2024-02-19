import os
import shutil
import re

EXTENSIONES_VIDEO = [".mp4", ".mkv", ".avi", ".mpeg"]
EXTENSIONES_COMPRESS = [".rar", ".zip"]

EXTENSIONES = EXTENSIONES_VIDEO + EXTENSIONES_COMPRESS

CARPETA_PELIS = ""
CARPETA_SERIES = ""
CARPETA_PROCESADOS = ""

def listar_elementos(ruta, nivel_maximo):
    archivos_encontrados = []

    for raiz, directorios, archivos in os.walk(ruta):
        nivel = raiz[len(ruta) + len(os.path.sep):].count(os.path.sep)
        if nivel <= nivel_maximo:
            for archivo in archivos:
                archivo_ruta = os.path.join(raiz, archivo)
                archivos_encontrados.append((nivel, archivo_ruta))
        else:
            continue
        if nivel == nivel_maximo:
            del directorios[:]

    archivos_encontrados.sort(reverse=True)  # Ordenar de mayor a menor profundidad
    return archivos_encontrados

def extraer_datos_archivos(ruta_archivo):

    # print(f"**************************************")
    # print(f"Nivel: {nivel}, Archivo: {archivo_ruta}")

    nombre_archivo = os.path.basename(ruta_archivo)
    nombre_sin_extension, extension = os.path.splitext(nombre_archivo)
    
    # Si el nombre del archivo contiene el sufijo ".partn", extraer el número de parte
    numero_parte = 0
    match_part = re.search(r'\.part(\d+)', nombre_sin_extension)
    if match_part:
        nombre_sin_extension = nombre_sin_extension.replace(match_part.group(), '')
        numero_parte = match_part.group(1)

    # print("Nombre del archivo:", nombre_sin_extension)
    # print("Extensión:", extension)

    # if 'numero_parte' in locals() and numero_parte != 0:
    #     print("Número de parte:", numero_parte)

    return nombre_sin_extension, extension, numero_parte

def hay_archivo_con_extension(carpeta):
    archivos = os.listdir(carpeta)
    for archivo in archivos:
        if os.path.splitext(archivo)[1].lower() in EXTENSIONES:
            return True
    return False

def organizar_pelis_y_series(origin, destiny):

    # Crear carpetas para películas y series
    ROUTE_DESTINY = destiny
    CARPETA_PELIS = os.path.join(ROUTE_DESTINY, "PELIS")
    CARPETA_SERIES = os.path.join(ROUTE_DESTINY, "Series")
    CARPETA_PROCESADOS = os.path.join(ROUTE_DESTINY, "Procesadas")
    os.makedirs(CARPETA_PELIS, exist_ok=True)
    os.makedirs(CARPETA_SERIES, exist_ok=True)
    os.makedirs(CARPETA_PROCESADOS, exist_ok=True)

    # return CARPETA_PELIS, CARPETA_SERIES, CARPETA_PROCESADOS

    archivos_encontrados = listar_elementos(origin, 5)
    for nivel, ruta_archivo in archivos_encontrados:

        if os.path.exists(ruta_archivo):

            nombre, extension, parte = extraer_datos_archivos(ruta_archivo)
            
            print(f"ruta_archivo: {ruta_archivo} ")
            
            archivo = ""
            if parte != 0:
                archivo = nombre + ".part" + parte + extension
                print(f"nombre: {nombre}.part{parte}{extension} ")
            else:
                archivo = nombre + extension
                print(f"nombre: {nombre}{extension} ")
            
            carpeta_padre = os.path.dirname(ruta_archivo)
            print(f"carpeta_padre: {carpeta_padre} ")
            nombre_carpeta_padre = os.path.basename(carpeta_padre)
            print(f"nombre_carpeta_padre: {nombre_carpeta_padre} ")

            # get Permisos originales
            permisos_originales = os.stat(ruta_archivo).st_mode
            print(f"Permisos originales: {permisos_originales}")

            # VIDEO
            if extension.lower() in EXTENSIONES:
                carpeta_peli = os.path.join(CARPETA_PELIS, nombre)
                os.makedirs(carpeta_peli, exist_ok=True)
                
                # if os.path.exists(carpeta_peli + "/" + archivo):
                #     shutil.rmtree(carpeta_peli + "/" + archivo)

                shutil.move(ruta_archivo, os.path.join(carpeta_peli, archivo))
                print(f"Organizada película: {nombre}")

                os.chmod(os.path.join(carpeta_peli), permisos_originales)
                os.chmod(os.path.join(carpeta_peli, archivo), permisos_originales)

                # procesados
                if not hay_archivo_con_extension(carpeta_padre):
                    print(f"carpeta para procesar: {carpeta_padre}")

                    print(f"carpeta para procesar destino: {CARPETA_PROCESADOS}/{nombre}")

                    if carpeta_padre != origin:
                        if os.path.exists(CARPETA_PROCESADOS + "/" + nombre_carpeta_padre):
                            shutil.rmtree(CARPETA_PROCESADOS + "/" + nombre_carpeta_padre)

                        shutil.move(carpeta_padre, CARPETA_PROCESADOS)
                # else:
                #     print(f"carpeta para procesar: {carpeta_padre}")
        
        print(f"******************************************** ")

# ROUTES_ORIGINS = ["/media/PRUEBA_ORGANIZER/ORIGEN1", "/media/PRUEBA_ORGANIZER/ORIGEN2", "/media/PRUEBA_ORGANIZER/OTHER"]
ROUTES_ORIGINS = ["/media/CLEANS/ToClean"]
ROUTE_DESTINY = "/media/CLEANS/cleaned"

if __name__ == "__main__":    
    # create_destiny_folders(ROUTE_DESTINY)

    for ruta_archivos in ROUTES_ORIGINS:
        organizar_pelis_y_series(ruta_archivos, ROUTE_DESTINY)