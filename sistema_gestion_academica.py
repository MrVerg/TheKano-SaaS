# sistema_gestion_academica.py
import tkinter as tk
from database import SistemaDAO
from login import Login
from panel_principal import PanelPrincipal

class SistemaGestionAcademica:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión Académica CEDUC")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')
        
        # Conectar a base de datos
        self.db = SistemaDAO()
        
        # Mostrar login
        self.mostrar_login()
    
    def mostrar_login(self):
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.login = Login(self.root, self.db, self.mostrar_panel_principal)
    
    def mostrar_panel_principal(self):
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        self.panel_principal = PanelPrincipal(self.root, self.db)
    
    def run(self):
        self.root.mainloop()