import tkinter as tk
from PIL import Image, ImageTk

class MetroApp:
    def __init__(self, root):
        root.title("MetroAPP")
        root.geometry("500x350")
        root.configure(bg="red")

        # Cargar la imagen
        image_path = "ruta/a/tu/imagen.png"  # ← Cambia esto por la ruta real
        image = Image.open(image_path)

        # Redimensionar si es necesario
        image = image.resize((500, 350), Image.LANCZOS)

        # Convertir a formato compatible con Tkinter
        photo = ImageTk.PhotoImage(image)

        # Crear etiqueta con la imagen
        label = tk.Label(root, image=photo)
        label.image = photo  # ← Importante para evitar que se borre
        label.place(x=0, y=0, relwidth=1, relheight=1)

if __name__ == "__main__":
    root = tk.Tk()
    MetroApp(root)
    root.mainloop()
