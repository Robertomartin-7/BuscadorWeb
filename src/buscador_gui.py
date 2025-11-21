# buscador_gui.py (versión final y completa, con top-N opcional)
# Este fichero contiene la interfaz gráfica y las funciones de ayuda.
# Los alumnos NO necesitan modificar este fichero.

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import webbrowser
import requests
from bs4 import BeautifulSoup
import threading
import sys

try:
    from buscador_utiles import (
        procesar_url_en_indice,
        procesar_url_en_indice_top_n,  
        buscar_palabra_simple,
        buscar_palabras_and,
        buscar_palabras_or,
        calcula_estadisticas_indice
    )
except ImportError:
    messagebox.showerror("Error", "No se pudo encontrar el fichero 'buscador_utiles.py' o las funciones necesarias no están definidas.")
    sys.exit(1)

URLS_WIKIPEDIA = [
    # Ciencia y Tecnología
    'https://es.wikipedia.org/wiki/Inteligencia_artificial', 'https://es.wikipedia.org/wiki/ADN', 'https://es.wikipedia.org/wiki/Agujero_negro',
    'https://es.wikipedia.org/wiki/Teor%C3%ADa_de_la_relatividad', 'https://es.wikipedia.org/wiki/Tabla_peri%C3%B3dica_de_los_elementos',
    'https://es.wikipedia.org/wiki/Computaci%C3%B3n_cu%C3%A1ntica', 'https://es.wikipedia.org/wiki/Fotos%C3%ADntesis',
    'https://es.wikipedia.org/wiki/Volc%C3%A1n', 'https://es.wikipedia.org/wiki/Sistema_solar', 'https://es.wikipedia.org/wiki/Programaci%C3%B3n_inform%C3%A1tica',
    'https://es.wikipedia.org/wiki/Internet', 'https://es.wikipedia.org/wiki/Tel%C3%A9fono_m%C3%B3vil', 'https://es.wikipedia.org/wiki/Autom%C3%B3vil',
    'https://es.wikipedia.org/wiki/Microscopio', 'https://es.wikipedia.org/wiki/Telescopio_espacial_Hubble', 'https://es.wikipedia.org/wiki/Estaci%C3%B3n_Espacial_Internacional',
    'https://es.wikipedia.org/wiki/Genoma_humano', 'https://es.wikipedia.org/wiki/Calentamiento_global', 'https://es.wikipedia.org/wiki/Placa_tect%C3%B3nica',
    'https://es.wikipedia.org/wiki/Agua', 'https://es.wikipedia.org/wiki/C%C3%A9lula_(biolog%C3%ADa)', 'https://es.wikipedia.org/wiki/Evoluci%C3%B3n_biol%C3%B3gica',
    'https://es.wikipedia.org/wiki/Dinosauria', 'https://es.wikipedia.org/wiki/Vacuna', 'https://es.wikipedia.org/wiki/Electricidad',
    # Historia
    'https://es.wikipedia.org/wiki/Imperio_romano', 'https://es.wikipedia.org/wiki/Antiguo_Egipto', 'https://es.wikipedia.org/wiki/Revoluci%C3%B3n_Industrial',
    'https://es.wikipedia.org/wiki/Primera_Guerra_Mundial', 'https://es.wikipedia.org/wiki/Segunda_Guerra_Mundial', 'https://es.wikipedia.org/wiki/Guerra_Fr%C3%ADa',
    'https://es.wikipedia.org/wiki/Renacimiento', 'https://es.wikipedia.org/wiki/Ilustraci%C3%B3n_(%C3%A9poca)', 'https://es.wikipedia.org/wiki/Revoluci%C3%B3n_francesa',
    'https://es.wikipedia.org/wiki/Ruta_de_la_seda', 'https://es.wikipedia.org/wiki/Imperio_incaico', 'https://es.wikipedia.org/wiki/Civilizaci%C3%B3n_maya',
    'https://es.wikipedia.org/wiki/Descubrimiento_de_Am%C3%A9rica', 'https://es.wikipedia.org/wiki/Ca%C3%ADda_del_Muro_de_Berl%C3%ADn',
    'https://es.wikipedia.org/wiki/Peste_negra', 'https://es.wikipedia.org/wiki/Reforma_protestante', 'https://es.wikipedia.org/wiki/Invasi%C3%B3n_musulmana_de_la_pen%C3%ADnsula_ib%C3%A9rica',
    'https://es.wikipedia.org/wiki/Gutenberg', 'https://es.wikipedia.org/wiki/Imprenta', 'https://es.wikipedia.org/wiki/C%C3%B3digo_de_Hammurabi',
    'https://es.wikipedia.org/wiki/Agricultura', 'https://es.wikipedia.org/wiki/Escritura', 'https://es.wikipedia.org/wiki/Rueda',
    'https://es.wikipedia.org/wiki/Feudalismo', 'https://es.wikipedia.org/wiki/Capitalismo',
    # Arte y Cultura
    'https://es.wikipedia.org/wiki/Leonardo_da_Vinci', 'https://es.wikipedia.org/wiki/Cervantes', 'https://es.wikipedia.org/wiki/William_Shakespeare',
    'https://es.wikipedia.org/wiki/Pintura_del_Antiguo_Egipto', 'https://es.wikipedia.org/wiki/Mona_Lisa', 'https://es.wikipedia.org/wiki/Don_Quijote_de_la_Mancha',
    'https://es.wikipedia.org/wiki/M%C3%BAsica_cl%C3%A1sica', 'https://es.wikipedia.org/wiki/Rock_and_roll', 'https://es.wikipedia.org/wiki/Cine',
    'https://es.wikipedia.org/wiki/Fotograf%C3%ADa', 'https://es.wikipedia.org/wiki/Arquitectura_g%C3%B3tica', 'https://es.wikipedia.org/wiki/Parten%C3%B3n',
    'https://es.wikipedia.org/wiki/Wolfgang_Amadeus_Mozart', 'https://es.wikipedia.org/wiki/Ludwig_van_Beethoven', 'https://es.wikipedia.org/wiki/Vincent_van_Gogh',
    'https://es.wikipedia.org/wiki/Pablo_Picasso', 'https://es.wikipedia.org/wiki/Los_Beatles', 'https://es.wikipedia.org/wiki/Juego_de_tronos',
    'https://es.wikipedia.org/wiki/Cien_a%C3%B1os_de_soledad', 'https://es.wikipedia.org/wiki/Poes%C3%ADa',
    'https://es.wikipedia.org/wiki/Teatro', 'https://es.wikipedia.org/wiki/Escultura', 'https://es.wikipedia.org/wiki/Mitolog%C3%ADa_griega',
    'https://es.wikipedia.org/wiki/Sinfon%C3%ADa_n.%C2%BA_9_(Beethoven)', 'https://es.wikipedia.org/wiki/Guernica_(cuadro)',
    # Geografía y Sociedad
    'https://es.wikipedia.org/wiki/Gran_Muralla_China', 'https://es.wikipedia.org/wiki/Amazonas_(r%C3%ADo)', 'https://es.wikipedia.org/wiki/Monte_Everest',
    'https://es.wikipedia.org/wiki/Desierto_del_Sahara', 'https://es.wikipedia.org/wiki/Oceano_Pac%C3%ADfico', 'https://es.wikipedia.org/wiki/Ant%C3%A1rtida',
    'https://es.wikipedia.org/wiki/Filosof%C3%ADa', 'https://es.wikipedia.org/wiki/Psicolog%C3%ADa', 'https://es.wikipedia.org/wiki/Democracia',
    'https://es.wikipedia.org/wiki/Derechos_humanos', 'https://es.wikipedia.org/wiki/Organizaci%C3%B3n_de_las_Naciones_Unidas',
    'https://es.wikipedia.org/wiki/Globalizaci%C3%B3n', 'https://es.wikipedia.org/wiki/Copa_Mundial_de_F%C3%BAtbol', 'https://es.wikipedia.org/wiki/Juegos_Ol%C3%ADmpicos',
    'https://es.wikipedia.org/wiki/Pir%C3%A1mides_de_Egipto', 'https://es.wikipedia.org/wiki/Machu_Picchu', 'https://es.wikipedia.org/wiki/Coliseo_de_Roma',
    'https://es.wikipedia.org/wiki/Econom%C3%ADa', 'https://es.wikipedia.org/wiki/Idioma_espa%C3%B1ol', 'https://es.wikipedia.org/wiki/Religi%C3%B3n'
]

# --- Funciones de Ayuda (Proporcionadas) ---
def obtener_texto_de_url(url: str) -> str | None:
    try:
        respuesta = requests.get(url, timeout=15, headers={'User-Agent': 'CoolBot/0.0'})
        respuesta.raise_for_status()
        soup = BeautifulSoup(respuesta.content, 'html.parser')
        for script_o_style in soup(['script', 'style', 'header', 'footer', 'nav']):
            script_o_style.decompose()
        texto = soup.get_text(separator=' ', strip=True)
        return texto
    except requests.RequestException:
        return None

def format_bytes(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} bytes"
    elif size_bytes < 1024**2:
        return f"{size_bytes/1024:.2f} KB"
    else:
        return f"{size_bytes/(1024**2):.2f} MB"

def cargar_indice() -> dict:
    return {}

def guardar_indice(indice: dict):
    pass

# --- Lógica de la Aplicación ---
class BuscadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mi Buscador Web")
        self.root.geometry("800x600")
        
        self.indice = cargar_indice()

        # Variables de control para top-N
        self.use_topn_var = tk.BooleanVar(value=False)
        self.topn_var = tk.IntVar(value=1000)
        
        self.crear_widgets()
        self.actualizar_estado()

    def crear_widgets(self):
        frame_index = ttk.LabelFrame(self.root, text="Indexación y Estado")
        frame_index.pack(fill="x", padx=10, pady=5)
        
        ttk.Label(frame_index, text="Añadir URL:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.url_entry = ttk.Entry(frame_index, width=60)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.add_url_button = ttk.Button(frame_index, text="Indexar URL", command=self.indexar_url)
        self.add_url_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.view_index_button = ttk.Button(frame_index, text="Ver Índice", command=self.ver_indice)
        self.view_index_button.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.index_wiki_button = ttk.Button(frame_index, text="Indexar URLs de Wikipedia", command=self.indexar_wikipedia)
        self.index_wiki_button.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="e")

        # --- Opciones Top-N ---
        self.chk_topn = ttk.Checkbutton(
            frame_index,
            text="Indexar sólo más frecuentes",
            variable=self.use_topn_var,
            command=self._toggle_topn_state
        )
        self.chk_topn.grid(row=2, column=0, padx=5, pady=(0,5), sticky="w")

        ttk.Label(frame_index, text="N:").grid(row=2, column=1, padx=(5,0), pady=(0,5), sticky="w")
        # ttk.Spinbox está disponible en Tk 8.5+ (Python 3.7+). Si diera problemas, puede sustituirse por tk.Spinbox.
        self.spin_topn = ttk.Spinbox(frame_index, from_=1, to=1000, textvariable=self.topn_var, width=6)
        self.spin_topn.grid(row=2, column=1, padx=(30,5), pady=(0,5), sticky="w")
        self._toggle_topn_state()

        # Expandir columna central
        frame_index.grid_columnconfigure(1, weight=1)
        
        frame_search = ttk.LabelFrame(self.root, text="Búsqueda")
        frame_search.pack(fill="x", padx=10, pady=5)
        
        self.search_query = tk.StringVar()
        self.search_type = tk.StringVar(value="simple")
        
        ttk.Label(frame_search, text="Buscar:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.search_entry = ttk.Entry(frame_search, width=60, textvariable=self.search_query)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        ttk.Radiobutton(frame_search, text="Simple", variable=self.search_type, value="simple").grid(row=1, column=0, sticky="w")
        ttk.Radiobutton(frame_search, text="Todas (AND)", variable=self.search_type, value="and").grid(row=2, column=0, sticky="w")
        ttk.Radiobutton(frame_search, text="Alguna (OR)", variable=self.search_type, value="or").grid(row=3, column=0, sticky="w")

        self.search_button = ttk.Button(frame_search, text="Buscar", command=self.realizar_busqueda)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        frame_search.grid_columnconfigure(1, weight=1)

        frame_results = ttk.LabelFrame(self.root, text="Resultados")
        frame_results.pack(fill="both", expand=True, padx=10, pady=10)

        self.results_text = scrolledtext.ScrolledText(frame_results, wrap=tk.WORD, state="disabled")
        self.results_text.pack(fill="both", expand=True)

        self.status_label = ttk.Label(self.root, text="", anchor="w")
        self.status_label.pack(side="bottom", fill="x", padx=10)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def _toggle_topn_state(self):
        # Habilita/deshabilita el spinbox según el check
        state = "normal" if self.use_topn_var.get() else "disabled"
        try:
            self.spin_topn.configure(state=state)
        except tk.TclError:
            # En algunos temas/entornos ttk puede no aplicar, forzamos con estándar
            self.spin_topn.state([state])

    def ver_indice(self):
        if not self.indice:
            messagebox.showinfo("Índice Vacío", "El índice aún no contiene datos.")
            return

        win_indice = tk.Toplevel(self.root)
        win_indice.title("Estado Actual del Índice")
        win_indice.geometry("800x500")
        win_indice.grab_set()

        # --- INICIO DE LA MODIFICACIÓN ---
        
        # 1. Calcular todas las estadísticas
        num_palabras, num_urls, promedio_urls = calcula_estadisticas_indice(self.indice)
        size_in_bytes = sys.getsizeof(self.indice)
        formatted_size = format_bytes(size_in_bytes)
        
        # 2. Crear un texto multilínea con toda la información
        stats_text = (
            f"Tamaño estimado en memoria: {formatted_size}\n"
            f"Palabras indexadas: {num_palabras}\n"
            f"URLs totales indexadas: {num_urls}\n"
            f"Promedio URLs / palabra: {promedio_urls:.2f}"
        )

        # 3. Mostrar el texto en la etiqueta, justificado a la izquierda
        info_label = ttk.Label(win_indice, text=stats_text, font=("", 10, "bold"), justify=tk.LEFT)
        info_label.pack(pady=(10, 5), padx=10) # Añadimos padx para que no pegue al borde
        
        # --- FIN DE LA MODIFICACIÓN ---

        frame = ttk.Frame(win_indice)
        frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        cols = ('palabra', 'urls')
        tree = ttk.Treeview(frame, columns=cols, show='headings')
        tree.heading('palabra', text='Palabra')
        tree.heading('urls', text='URLs Encontradas')
        tree.column('palabra', width=150, stretch=tk.NO)
        tree.column('urls', width=2000) # Un ancho grande para forzar el scroll

        v_scroll = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        h_scroll = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        for palabra, urls in sorted(self.indice.items()):
            urls_string = ", ".join(urls)
            tree.insert("", tk.END, values=(palabra, urls_string))
            
        tree.grid(row=0, column=0, sticky='nsew')
        v_scroll.grid(row=0, column=1, sticky='ns')
        h_scroll.grid(row=1, column=0, sticky='ew')
        
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

    def indexar_url(self):
        url = self.url_entry.get().strip()
        if not url:
            return
        self.status_label.config(text=f"Indexando {url}...")
        self.root.update_idletasks()
        texto = obtener_texto_de_url(url)
        if texto:
            if self.use_topn_var.get():
                top_n = max(1, int(self.topn_var.get()))
                procesar_url_en_indice_top_n(url, texto, self.indice, top_n)
            else:
                procesar_url_en_indice(url, texto, self.indice)
            self.actualizar_estado()
            messagebox.showinfo("Éxito", f"¡URL '{url}' indexada correctamente!")
        else:
            messagebox.showerror("Error", f"No se pudo obtener el contenido de la URL '{url}'.")
        self.status_label.config(text="")

    def indexar_wikipedia(self):
        if not messagebox.askyesno("Confirmar", f"¿Quieres indexar {len(URLS_WIKIPEDIA)} URLs de Wikipedia? Esto puede tardar varios minutos."):
            return
        self.crear_ventana_progreso()
        thread = threading.Thread(target=self._worker_indexar_wiki, daemon=True)
        thread.start()

    def crear_ventana_progreso(self):
        self.progress_window = tk.Toplevel(self.root)
        self.progress_window.title("Indexando Wikipedia...")
        self.progress_window.geometry("600x150")
        self.progress_window.resizable(False, False)
        self.progress_window.grab_set()
        self.progress_window.transient(self.root)
        self.progress_bar = ttk.Progressbar(self.progress_window, orient="horizontal", length=580, mode="determinate")
        self.progress_bar.pack(pady=20)
        self.percent_label = ttk.Label(self.progress_window, text="0%")
        self.percent_label.pack()
        self.url_label = ttk.Label(self.progress_window, text="Iniciando...")
        self.url_label.pack(pady=5)

    def _worker_indexar_wiki(self):
        total_urls = len(URLS_WIKIPEDIA)
        usar_topn = self.use_topn_var.get()
        top_n = max(1, int(self.topn_var.get())) if usar_topn else None

        for i, url in enumerate(URLS_WIKIPEDIA):
            texto = obtener_texto_de_url(url)
            if texto:
                if usar_topn:
                    procesar_url_en_indice_top_n(url, texto, self.indice, top_n)
                else:
                    procesar_url_en_indice(url, texto, self.indice)
            progreso = (i + 1) / total_urls * 100
            self.root.after(0, self.actualizar_progreso, progreso, url)
        self.root.after(0, self.finalizar_indexacion_wiki)

    def actualizar_progreso(self, progreso, url_actual):
        self.progress_bar['value'] = progreso
        self.percent_label.config(text=f"{progreso:.0f}%")
        url_mostrada = url_actual if len(url_actual) < 80 else url_actual[:77] + "..."
        self.url_label.config(text=f"Procesando: {url_mostrada}")

    def finalizar_indexacion_wiki(self):
        try:
            self.progress_window.destroy()
        except Exception:
            pass
        self.actualizar_estado()
        messagebox.showinfo("Completado", "Se han indexado todas las URLs de Wikipedia.")

    def realizar_busqueda(self):
        query = self.search_query.get().strip()
        search_type = self.search_type.get()
        if not query:
            return
        if search_type == "simple":
            resultados = buscar_palabra_simple(query, self.indice)
        elif search_type == "and":
            resultados = buscar_palabras_and(query, self.indice)
        else:
            resultados = buscar_palabras_or(query, self.indice)
        self.mostrar_resultados(resultados)

    def mostrar_resultados(self, urls):
        self.results_text.config(state="normal")
        self.results_text.delete(1.0, tk.END)
        if not urls:
            self.results_text.insert(tk.END, "No se encontraron resultados.")
        else:
            self.results_text.insert(tk.END, f"Se encontraron {len(urls)} resultados:\n\n")
            for url in urls:
                self.results_text.insert(tk.END, url, (f"link_{url}",))
                self.results_text.insert(tk.END, "\n\n")
                self.results_text.tag_config(f"link_{url}", foreground="blue", underline=True)
                self.results_text.tag_bind(f"link_{url}", "<Button-1>", lambda e, u=url: self.abrir_enlace(u))
        self.results_text.config(state="disabled")

    def abrir_enlace(self, url):
        webbrowser.open_new(url)

    def actualizar_estado(self):
        num_palabras = len(self.indice)
        num_urls = len(set(url for urls in self.indice.values() for url in urls))
        modo = f" | Modo top-N={'ON' if self.use_topn_var.get() else 'OFF'}"
        if self.use_topn_var.get():
            modo += f" (N={max(1, int(self.topn_var.get()))})"
        self.status_label.config(text=f"Índice actual: {num_palabras} palabras únicas de {num_urls} URLs.{modo}")

    def on_closing(self):
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BuscadorApp(root)
    root.mainloop()
