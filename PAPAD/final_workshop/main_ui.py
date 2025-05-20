import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
from PIL import Image, ImageTk
from model_optimization import optimize_model
from grafo import get_grafo
import os

class OptimizationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Optimización con Pyomo")
        # Maximizar ventana por defecto
        try:
            self.attributes('-zoomed', True)
        except Exception:
            self.state('zoomed')
        self.configure(bg="#F0F4FF")

        # Para mantener referencia a la imagen y estado de índice
        self._photo = None
        self._img_index = 0
        self._img_paths = [f"image{i}.png" for i in range(1,5)]

        # Estilos
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TLabel', background='#F0F4FF', font=('Arial', 11), foreground='#333')
        style.configure('Header.TLabel', background='#F0F4FF', font=('Arial', 14, 'bold'), foreground='#0D47A1')
        style.configure('Accent.TButton', background='#1976D2', foreground='white',
                        font=('Arial', 11, 'bold'), padding=6)
        style.map('Accent.TButton',
                  background=[('active', '#1565C0'), ('disabled', '#90CAF9')])
        style.configure('File.TFrame', background='#E3F2FD', relief='groove', padding=10)

        self._create_widgets()

    def _create_widgets(self):
        # --- Sección de archivos ---
        ttk.Label(self, text="Configuración de Archivos CSV", style='Header.TLabel') \
            .grid(row=0, column=0, columnspan=3, pady=(15, 5))

        files_frame = ttk.Frame(self, style='File.TFrame')
        files_frame.grid(row=1, column=0, columnspan=3, padx=20, pady=10, sticky='ew')
        files_frame.columnconfigure(1, weight=1)

        archivos = [
            ("Centros CSV", "resources/centros.csv"),
            ("Clientes CSV", "resources/clientes.csv"),
            ("Costos CSV",   "resources/costos.csv"),
            ("Plantas CSV",  "resources/plantas.csv"),
            ("Productos CSV","resources/productos.csv"),
        ]
        self.file_vars = {}
        for idx, (label, default) in enumerate(archivos):
            ttk.Label(files_frame, text=label).grid(row=idx, column=0, sticky='w', padx=5, pady=4)
            var = tk.StringVar(value=default)
            ttk.Entry(files_frame, textvariable=var).grid(row=idx, column=1, sticky='ew', padx=5, pady=4)
            ttk.Button(files_frame, text="Seleccionar", style='Accent.TButton',
                       command=lambda v=var: self._browse_file(v)) \
                .grid(row=idx, column=2, padx=5)
            self.file_vars[label] = var

        ttk.Button(self, text="Ejecutar Optimización", style='Accent.TButton',
                   command=self._run_optimization) \
            .grid(row=2, column=0, columnspan=3, pady=15)

        ttk.Separator(self, orient='horizontal') \
            .grid(row=3, column=0, columnspan=3, sticky='ew', padx=20, pady=10)

        # --- Sección inferior: dividido en 3 ---
        bottom_frame = ttk.Frame(self)
        bottom_frame.grid(row=4, column=0, columnspan=3, sticky='nsew', padx=20, pady=10)
        bottom_frame.grid_columnconfigure(0, weight=1, uniform='cols')
        bottom_frame.grid_columnconfigure(1, weight=1, uniform='cols')
        bottom_frame.grid_rowconfigure(0, weight=1, uniform='rows')
        bottom_frame.grid_rowconfigure(1, weight=1, uniform='rows')

        # Izquierda: resultados completos
        self.left_output = scrolledtext.ScrolledText(
            bottom_frame, wrap='word', font=('Consolas', 10), bg='#FFFFFF', fg='#000000', relief='ridge'
        )
        self.left_output.grid(row=0, column=0, rowspan=2, sticky='nsew', padx=(0,10))

        # Derecha arriba: texto de grafo
        self.right_text = scrolledtext.ScrolledText(
            bottom_frame, wrap='word', font=('Consolas', 10), bg='#FFFFFF', fg='#000000', relief='ridge'
        )
        self.right_text.grid(row=0, column=1, sticky='nsew', padx=(0,0), pady=(0,5))

        # Derecha abajo: imagen y botón
        img_frame = ttk.Frame(bottom_frame)
        img_frame.grid(row=1, column=1, sticky='nsew')
        img_frame.grid_rowconfigure(0, weight=1)
        img_frame.grid_rowconfigure(1, weight=0)
        img_frame.grid_columnconfigure(0, weight=1)

        self.image_label = ttk.Label(
            img_frame, background='#FFFFFF', relief='ridge', anchor='center'
        )
        self.image_label.grid(row=0, column=0, sticky='nsew')

        self.next_btn = ttk.Button(img_frame, text="Siguiente Imagen", style='Accent.TButton',
                                   command=self._next_image)
        self.next_btn.grid(row=1, column=0, pady=5)

        # Ajuste expansión root
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

    def _browse_file(self, var):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if path:
            var.set(path)

    def _run_optimization(self):
        self.left_output.delete('1.0', tk.END)
        self.right_text.delete('1.0', tk.END)
        self._img_index = 0

        rutas = {k: v.get() for k, v in self.file_vars.items()}
        try:
            costo, plant_to_center, center_to_client, model = optimize_model(rutas)

            # Izquierda
            self.left_output.insert(tk.END, f"Costo total = ${costo:.2f}\n\n")
            self.left_output.insert(tk.END, "Desde las Plantas a los Centros:\n")
            for row in plant_to_center:
                self.left_output.insert(tk.END, f"{row}\n")
            self.left_output.insert(tk.END, "\nDesde los Centros a los Clientes:\n")
            for row in center_to_client:
                self.left_output.insert(tk.END, f"{row}\n")

            # Texto grafo
            grafo_lines = get_grafo(model)
            for line in grafo_lines:
                self.right_text.insert(tk.END, f"{line}\n")

            # Cargar primera imagen
            self._load_image()

        except Exception as e:
            self.right_text.insert(tk.END, f"Error: {e}")

    def _load_image(self):
        path = self._img_paths[self._img_index]
        if os.path.exists(path):
            img = Image.open(path)
            # Usar LANCZOS para compatibilidad en Pillow
            resample = getattr(Image, 'Resampling', Image).LANCZOS
            img = img.resize((360, 240), resample)
            self._photo = ImageTk.PhotoImage(img)
            self.image_label.configure(image=self._photo)
        else:
            self.image_label.configure(text="Imagen no encontrada", image='')

    def _next_image(self):
        self._img_index = (self._img_index + 1) % len(self._img_paths)
        self._load_image()

if __name__ == "__main__":
    app = OptimizationApp()
    app.mainloop()
