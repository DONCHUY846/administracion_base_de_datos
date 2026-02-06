import tkinter as tk
from tkinter import messagebox
from database import connect_to_database
from main import show_databases

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Administrador de Base de Datos")
        
        self.connection = connect_to_database()
        
        if not self.connection:
            messagebox.showerror("Error de Conexión", "No se pudo conectar a la base de datos. La aplicación se cerrará.")
            self.root.destroy()
            return

        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(padx=20, pady=20)

        self.btn_show_dbs = tk.Button(self.main_frame, text="Ver Bases de Datos", command=self.display_databases)
        self.btn_show_dbs.pack(pady=10)

    def display_databases(self):
        databases = show_databases(self.connection)
        if databases:
            db_list = "\n".join(databases)
            messagebox.showinfo("Bases de Datos", db_list)
        else:
            messagebox.showwarning("Bases de Datos", "No se encontraron bases de datos o hubo un error al obtenerlas.")

    def on_closing(self):
        if self.connection:
            self.connection.close()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = App(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
