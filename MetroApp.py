import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from IA.metro_modelo import Graph, calcular_ruta  # Importamos el grafo y la función

class MetroApp:
    def __init__(self, root):
        root.title("MetroAPP")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f"{screen_width}x{screen_height}")
        root.configure(bg="white")

        header = tk.Frame(root, bg="red", height=60)
        header.pack(side="top", fill="x")
        titulo = tk.Label(header, text="Mapa Metro CDMX", bg="red", fg="white",
                          font=("Arial", 20, "bold"))
        titulo.pack(pady=10)

        frame_controles = tk.Frame(root, bg="white", width=300)
        frame_controles.pack(side="left", fill="y")

        estaciones = list(Graph.nodes)

        tk.Label(frame_controles, text="Inicio ruta:", bg="white").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.estacion_inicio = ttk.Combobox(frame_controles, values=estaciones)
        self.estacion_inicio.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_controles, text="Final ruta:", bg="white").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.estacion_destino = ttk.Combobox(frame_controles, values=estaciones)
        self.estacion_destino.grid(row=1, column=1, padx=5, pady=5)

        calcular_btn = tk.Button(frame_controles, text="Calcular ruta", command=self.calcular_ruta)
        calcular_btn.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")

        self.resultado_label = tk.Label(frame_controles, text="", wraplength=250, anchor="center", justify="center", bg="white")
        self.resultado_label.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        self.tiempo_label = tk.Label(frame_controles, text="", wraplength=250, anchor="center", justify="center", bg="white")
        self.tiempo_label.grid(row=4, column=0, columnspan=2, pady=10, sticky="ew")

        image_path = "/Users/rcc/Documents/IA/Metro.png"
        image = Image.open(image_path)
        image = image.resize((int(screen_width * 2 / 3), int(screen_height * 2 / 3)), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        label = tk.Label(root, image=photo, bg="white")
        label.image = photo
        label.pack(side="right", expand=True)

    def calcular_ruta(self):
        inicio = self.estacion_inicio.get()
        destino = self.estacion_destino.get()
        if inicio and destino:
            try:
                camino, tiempo_total = calcular_ruta(inicio, destino)
                self.resultado_label.config(text=f"Camino: {' → '.join(camino)}")
                self.tiempo_label.config(text=f"Tiempo total: {tiempo_total} min")
            except Exception:
                self.resultado_label.config(text="No existe ruta entre esas estaciones")
                self.tiempo_label.config(text="")
        else:
            self.resultado_label.config(text="Selecciona origen y destino")
            self.tiempo_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    MetroApp(root)
    root.mainloop()

