import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from datetime import datetime
import busqueda_IA as modulo_IA  # Importamos el grafo y la función

FRANJAS_HORARIAS = [
    (7, 0, 9, 0),
    (18, 0, 20, 0)
]
FACTOR_NORMAL = 1.0
FACTOR_HORA_PUNTA = 1.2

class MetroApp:
    def __init__(self, root):
        root.title("MetroAPP")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.configure(bg="white")

        half_screen_width = screen_width // 2
        header = tk.Frame(root, bg="red", height=60)
        header.pack(side="top", fill="x")
        titulo = tk.Label(header, text="Mapa Metro CDMX", bg="red", fg="white",
                          font=("Arial", 20, "bold"))
        titulo.pack(pady=10)

        frame_controles = tk.Frame(root, bg="white", width=300)
        frame_controles.pack(side="left", fill="both", expand=True)

        estaciones = list(modulo_IA.Graph.nodes)

        frame_controles.grid_columnconfigure(1, weight=1)

        tk.Label(frame_controles, text="Inicio ruta:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.estacion_inicio = ttk.Combobox(frame_controles, values=estaciones)
        self.estacion_inicio.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_controles, text="Final ruta:", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.estacion_destino = ttk.Combobox(frame_controles, values=estaciones)
        self.estacion_destino.grid(row=1, column=1, padx=5, pady=5)

        hora_actual = datetime.now().strftime("%H:%M")
        tk.Label(frame_controles, text="Hora salida (HH:MM):", bg="white").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.hora_salida = tk.StringVar(value=hora_actual)
        self.hora_entry = ttk.Entry(frame_controles, textvariable=self.hora_salida, width=10)
        self.hora_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.status_label = tk.Label(frame_controles, text="Afluencia:", bg="lightyellow")
        self.status_label.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")


        self.es_discapacitado_var = tk.BooleanVar(value=modulo_IA.es_discapacitado if hasattr(modulo_IA, 'es_discapacitado') else False)
        self.check_discapacidad = ttk.Checkbutton(frame_controles, text="Movilidad reducida", variable=self.es_discapacitado_var, command=self.toggle_discapacidad)
        self.check_discapacidad.grid(row=4, column=0, columnspan=2, pady=5, sticky="w")
        self.status_label = tk.Label(frame_controles, text="Estaciones de dificil acceso: {Chapultepec, Insurgentes, Etiopia,\n Eugenia, Division del Norte, Coyoacan,\n Lazaro Cardenas}", bg="lightyellow")
        self.status_label.grid(row=5, column=0, columnspan=2, pady=5, sticky="ew")

        calcular_btn = tk.Button(frame_controles, text="Calcular ruta", command=self.calcular_ruta)
        calcular_btn.grid(row=6, column=0, columnspan=2, pady=10, sticky="ew")

        self.resultado_label = tk.Label(frame_controles, text="", wraplength=250, anchor="center", justify="center", bg="white")
        self.resultado_label.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")

        self.tiempo_label = tk.Label(frame_controles, text="", wraplength=250, anchor="center", justify="center", bg="white")
        self.tiempo_label.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")


        image_path = "Metro.png"
        image = Image.open(image_path)
        image_width, image_height = image.size
        max_width = int(screen_width // 2)
        max_height = int(screen_height)
        ratio = min(max_width / image_width, max_height / image_height)
        new_width = int(image_width * ratio)
        new_height = int(image_height * ratio)
        image = image.resize((new_width, new_height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(root, image=photo, bg="white")
        label.image = photo
        label.pack(side="right", expand=True)

    def toggle_discapacidad(self):
        modulo_IA.es_discapacitado = self.es_discapacitado_var.get()
        print(f"Penalizacion de accesibilidad: {'Activada' if modulo_IA.es_discapacitado else 'Desactivada'}")


    def hora_punta(self, hora_str):
        try:
            h, m = map(int, hora_str.split(':'))
            tiempo = h * 60 + m
            if not(0 <= h <= 23 and 0 <= m <= 59):
                raise ValueError("Hora/minuto fuera de rango.")
            for inicio_h, inicio_m, fin_h, fin_m in FRANJAS_HORARIAS:
                inicio_min = inicio_h * 60 + inicio_m
                fin_min = fin_h * 60 + fin_m
                if inicio_min <= tiempo < fin_min:
                    return FACTOR_HORA_PUNTA, "Hora punta"
            return FACTOR_NORMAL, "Afluencia normal"
        except ValueError as e:
            messagebox.showerror("Error de hora", f"Formato invalido: {e}, usa HH:MM")
            return None, None
            

    def calcular_ruta(self):
        inicio = self.estacion_inicio.get()
        destino = self.estacion_destino.get()
        hora_str = self.hora_salida.get()
        if not(inicio and destino and hora_str):
            self.resultado_label.config(text="Debe rellenar los campos de origen, destino y hora de salida.")
            self.tiempo_label.config(text="")
            return
        factor, estado = self.hora_punta(hora_str)
        if factor is None:
            return
        modulo_IA.factor_hora = factor
        self.status_label.config(text=f"Afluencia: {estado}")
        try:
            camino, tiempo_total = modulo_IA.calcular_ruta(inicio, destino)
            self.resultado_label.config(text=f"Camino: {' → '.join(camino)}")
            self.tiempo_label.config(text=f"Tiempo total: {tiempo_total:} min")
        except nx.NetworkXNoPath:
            self.resultado_label.config(text="No existe ruta entre estas estaciones")
            self.tiempo_label.config(text="")
        except Exception as e:
            self.resultado_label.config(text=f"Error inesperado: {e}")
            self.tiempo_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    MetroApp(root)
    root.mainloop()
