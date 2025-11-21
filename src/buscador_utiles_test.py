from buscador_utiles import *

def test_normalizar_texto():
    print("Probando normalizar_texto...")
    assert normalizar_texto("  Hola Mundo!  ") == ['hola', 'mundo']
    assert normalizar_texto("Python-3.8") == ['python']
    assert normalizar_texto("¡Bienvenidos a la programación!") == ['bienvenidos', 'programación']

def test_procesar_url_en_indice():
    print("Probando procesar_url_en_indice...")
    indice = {}
    procesar_url_en_indice("http://example.com", "Hola Mundo", indice)
    assert indice == {
        "hola": {"http://example.com"},
        "mundo": {"http://example.com"}
    }
    procesar_url_en_indice("http://example.org", "Hola Python", indice)
    assert indice == {
        "hola": {"http://example.com", "http://example.org"},
        "mundo": {"http://example.com"},
        "python": {"http://example.org"}
    }

def test_buscar_palabra_simple():
    print("Probando buscar_palabra_simple...")
    indice = {
        "hola": {"http://example.com", "http://example.org"},
        "mundo": {"http://example.com"},
        "python": {"http://example.org"}
    }
    assert buscar_palabra_simple("hola", indice) == {"http://example.com", "http://example.org"}
    assert buscar_palabra_simple("mundo", indice) == {"http://example.com"}
    assert buscar_palabra_simple("python", indice) == {"http://example.org"}
    assert buscar_palabra_simple("java", indice) == set()

def test_buscar_palabras_or():
    print("Probando buscar_palabras_or...")
    indice = {
        "hola": {"http://example.com", "http://example.org"},
        "mundo": {"http://example.com"},
        "python": {"http://example.org"}
    }
    assert buscar_palabras_or("hola mundo", indice) == {"http://example.com", "http://example.org"}
    assert buscar_palabras_or("hola python", indice) == {"http://example.com", "http://example.org"}
    assert buscar_palabras_or("mundo python", indice) == {"http://example.com", "http://example.org"}
    assert buscar_palabras_or("java python", indice) == {"http://example.org"}

def test_buscar_palabras_and():
    print("Probando buscar_palabras_and...")
    indice = {
        "hola": {"http://example.com", "http://example.org"},
        "mundo": {"http://example.com"},
        "python": {"http://example.org"}
    }
    assert buscar_palabras_and("hola mundo", indice) == {"http://example.com"}
    assert buscar_palabras_and("hola python", indice) == {"http://example.org"}
    assert buscar_palabras_and("mundo python", indice) == set()
    assert buscar_palabras_and("java python", indice) == set()

def test_procesar_url_en_indice_top_n():
    print("Probando procesar_url_en_indice_top_n...")
    indice = {}
    procesar_url_en_indice_top_n("http://example.com", "Hola Mundo Hola", indice, 1)
    assert indice == {
        "hola": {"http://example.com"}
    }
    procesar_url_en_indice_top_n("http://example.org", "Hola Hola Python Python Python Basura", indice, 2)
    assert indice == {
        "hola": {"http://example.com", "http://example.org"},
        "python": {"http://example.org"}
    }

def test_calcula_estadisticas_indice():
    print("Probando calcula_estadisticas_indice...")
    indice = {
        "hola": {"http://example.com", "http://example.org", "http://test.com"},
        "mundo": {"http://example.com"},
        "python": {"http://example.org", "http://python.org", "http://test.com"},
        "programacion": {"http://example.com", "http://example.org"},
        "codigo": {"http://test.com"}
    }
    num_palabras, num_urls, promedio_urls_por_palabra = calcula_estadisticas_indice(indice)
    assert num_palabras == 5
    assert num_urls == 4
    # Total de URLs distintas: 10
    # Promedio: 10 / 5 = 2.0
    assert abs(promedio_urls_por_palabra - 2.0) < 1e-6

test_normalizar_texto()
#test_procesar_url_en_indice()
#test_buscar_palabra_simple()
#test_buscar_palabras_or()
#test_buscar_palabras_and()
#test_procesar_url_en_indice_top_n()
#test_calcula_estadisticas_indice()
print("Todas las pruebas funcionaron correctamente.")