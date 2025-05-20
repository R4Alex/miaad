import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
# Import your Pyomo optimization function here
# For example: from my_pyomo_model import optimize_model
from my_pyomo_model import optimize_model  

class OptimizationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Optimización con Pyomo")
        self.geometry("700x650")
        self._create_widgets()

    def _create_widgets(self):
        files = [
            ("Centros CSV", "centros.csv"),
            ("Clientes CSV", "clientes.csv"),
            ("Costos CSV", "costos.csv"),
            ("Plantas CSV", "plantas.csv"),
            ("Productos CSV", "productos.csv"),
        ]
        self.file_vars = {}
        for idx, (label, default) in enumerate(files):
            ttk.Label(self, text=label).grid(row=idx, column=0, sticky="w", padx=5, pady=5)
            var = tk.StringVar(value=default)
            entry = ttk.Entry(self, textvariable=var, width=50)
            entry.grid(row=idx, column=1, padx=5, pady=5)
            btn = ttk.Button(self, text="Browse", command=lambda v=var: self._browse_file(v))
            btn.grid(row=idx, column=2, padx=5, pady=5)
            self.file_vars[label] = var

        run_btn = ttk.Button(self, text="Ejecutar Optimización", command=self._run_optimization)
        run_btn.grid(row=len(files), column=0, columnspan=3, pady=10)

        ttk.Label(self, text="Resultados:").grid(row=len(files)+1, column=0, sticky="w", padx=5)
        self.output = scrolledtext.ScrolledText(self, width=80, height=20)
        self.output.grid(row=len(files)+2, column=0, columnspan=3, padx=5, pady=5)

    def _browse_file(self, var):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")])
        if path:
            var.set(path)

    def _run_optimization(self):
        self.output.delete(1.0, tk.END)
        centros = self.file_vars["Centros CSV"].get()
        clientes = self.file_vars["Clientes CSV"].get()
        costos = self.file_vars["Costos CSV"].get()
        plantas = self.file_vars["Plantas CSV"].get()
        productos = self.file_vars["Productos CSV"].get()
        try:
            cost, allocations = optimize_model(centros, clientes, costos, plantas, productos)
            self.output.insert(tk.END, f"Costo = {cost:.2f}\n")
            for plant, center, product, amount in allocations:
                self.output.insert(tk.END, f"Planta {plant} a Centro {center}, Producto {product}: {amount:.2f}\n")
        except Exception as e:
            self.output.insert(tk.END, f"Error al ejecutar la optimización:\n{e}")

if __name__ == "__main__":
    app = OptimizationApp()
    app.mainloop()

