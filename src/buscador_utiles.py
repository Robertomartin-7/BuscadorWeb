from collections import Counter

# Conjunto con palabras huecas (se ignoran en las búsquedas, no se indexan)
STOP_WORDS = {'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'pero', 'sus', 'le', 'ya', 'o'}

# Caracteres de puntuación
PUNTUACION = '!¡"#$%&\'()*+,-./:;<=>?¿@[\\]^_`{|}~'

def normalizar_texto(texto: str) -> list[str]:
    """
    Recibe un texto, lo limpia y devuelve una lista de palabras. En el proceso de limpieza, 
    la función:
    1. Convierte el texto a minúsculas.
    2. Quita los signos de puntuación (los caracteres contenidos en PUNTUACION).
    3.Filtra las palabras huecas (las palabras contenidas en STOP_WORDS).
    
    Ejemplo: normalizar_texto("¡Hola, Mundo!") debería devolver ['hola', 'mundo']

    Parámetros:
    texto (str): El texto a normalizar.
    
    Devuelve:
    list[str]: Una lista de palabras normalizadas.
    """
    texto = texto.lower()
    for i in PUNTUACION:
            if i in texto:
                texto = texto.replace(i, " ")

    palabras = texto.split()
    filtrado = []
    for p in palabras:
        if p not in STOP_WORDS and p.isalpha():
            #filtrado = palabras.remove(p)
            filtrado.append(p)
    return filtrado        

def procesar_url_en_indice(url: str, texto: str, indice: dict[str, set[str]]):
    """
    Recibe la URL, el texto ya extraído de esa URL y un diccionario que indexa
    URLs de páginas web usando las palabras contenidas en la web como clave.
    La función actualiza el diccionario para incluir la URL en los conjuntos asociados
    a las palabras que aparecen en el texto.
    
    Parámetros:
    url (str): La URL de la página web.
    texto (str): El texto extraído de la página web.
    indice (dict[str, set[str]]): El índice de búsqueda a actualizar.
    """
    palabras = normalizar_texto(texto)
    for p in palabras:
        if p not in indice:
            indice[p] = set()
        #indice[p].add(url)
        indice.get(p, None).add(url)
  
def buscar_palabra_simple(palabra: str, indice: dict[str, set[str]]) -> set[str]:
    """
    Recibe una única palabra de búsqueda y el índice, y devuelve
    un conjunto de URLs donde se encontró esa palabra.
    Si la palabra no está en el índice, debe devolver un conjunto vacío.
    Antes de buscarla, la palabra será normalizada.

    Parámetros:
    palabra (str): La palabra a buscar.
    indice (dict[str, set[str]]): El índice de búsqueda.

    Devuelve:
    set[str]: Un conjunto de URLs donde se encontró la palabra.
    """    
    palabra = normalizar_texto(palabra)[0]
    if palabra not in indice:
        return set()
    else:
        return indice[palabra]

def buscar_palabras_or(frase: str, indice: dict[str, set[str]]) -> set[str]:
    """
    Recibe una frase de búsqueda y el índice, y devuelve
    un conjunto de URLs donde se encuentren alguna de las palabras de la frase.
    Si ninguna de las palabras están en el índice, debe devolver un conjunto vacío.
    La función normalizará el texto de la frase antes de buscar.

    Parámetros:
    frase (str): La frase de búsqueda.
    indice (dict[str, set[str]]): El índice de búsqueda.

    Devuelve:
    set[str]: Un conjunto de URLs donde se encontraron todas las palabras.
    """    
    palabras = normalizar_texto(frase)
    res = set()
    for p in palabras:
        palabra_actual = buscar_palabra_simple(p, indice)
        res.update(palabra_actual)
    
    return res

def buscar_palabras_and(frase: str, indice: dict[str, set[str]]) -> set[str]:
    """
    Recibe una frase de búsqueda y el índice, y devuelve
    un conjunto de URLs donde se encuentren todas las palabras de la frase.
    Si ninguna de las palabras están en el índice, debe devolver un conjunto vacío.
    La función normalizará el texto de la frase antes de buscar.

    Parámetros:
    frase (str): La frase de búsqueda.
    indice (dict[str, set[str]]): El índice de búsqueda.

    Devuelve:
    set[str]: Un conjunto de URLs donde se encontraron todas las palabras.
    """

    lista = normalizar_texto(frase)
    if len(lista) == 0:
        return set()

    resultado = buscar_palabra_simple(lista[0], indice) 
    for p in lista[1:]:
        urls_palabra = buscar_palabra_simple(p, indice) 
        resultado = resultado.intersection(urls_palabra)

        if not resultado:
            break

    return resultado

def procesar_url_en_indice_top_n(url: str, texto: str, indice: dict[str, set[str]], top_n: int=1000):
    """
    Recibe la URL, el texto ya extraído de esa URL y un diccionario que indexa
    URLs de páginas web usando las palabras contenidas en la web como clave.
    La función actualiza el diccionario para incluir la URL en los conjuntos asociados
    a las 'top_n' palabras más frecuentes de entre las que aparecen en el texto.

    Parámetros:
    url (str): La URL de la página web.
    texto (str): El texto extraído de la página web.
    indice (dict[str, set[str]]): El índice de búsqueda a actualizar.
    top_n (int): Número de palabras más frecuentes a indexar.
    """
    palabras = normalizar_texto(texto)

    contador = Counter(palabras)

    top_tuplas = contador.most_common(top_n)
    top_palabras = []
    for tupla in top_tuplas:
        palabra = tupla[0]
        top_palabras.append(palabra)

    for p in top_palabras:
        if p not in indice:
            indice[p] = set()
        indice[p].add(url)

def calcula_estadisticas_indice(indice: dict[str, set[str]]) -> tuple[int, int, float]:
    """
    Recibe un índice y calcula estadísticas sobre él.

    Parámetros:
    indice (dict[str, set[str]]): El índice de búsqueda.

    Devuelve:
    tuple[int, int, float]: Una tupla con tres valores:
        - Número total de palabras indexadas.
        - Número total de URLs indexadas (sin duplicados).
        - Promedio de URLs por palabra: cuántas URLs hay indexadas para cada palabra, en promedio.
    """
    num_palabras = len(indice)
    urls_unicas = set()
    for urls in indice.values():
        urls_unicas.update(urls)
    num_urls_unicas = len(urls_unicas)

    total_urls = sum(len(urls) for urls in indice.values())
    promedio = total_urls / num_palabras if num_palabras > 0 else 0.0

    return num_palabras, num_urls_unicas, promedio
