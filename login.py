# login.py
import tkinter as tk
from tkinter import messagebox

class Login:
    def __init__(self, root, db, callback_success):
        self.root = root
        self.db = db
        self.callback_success = callback_success
        
        self.mostrar_login()
    
    def mostrar_login(self):
        # Limpiar ventana
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Crear frame principal
        main_frame = tk.Frame(self.root, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # Título
        titulo = tk.Label(main_frame, text="CEDUC", font=("Arial", 24, "bold"), bg='#f0f0f0', fg='#2c3e50')
        titulo.pack(pady=(0, 30))
        
        # Frame de login
        login_frame = tk.Frame(main_frame, bg='white', relief='raised', bd=1)
        login_frame.pack(pady=20, ipadx=20, ipady=20)
        
        # Etiquetas y campos
        tk.Label(login_frame, text="Usuario", font=("Arial", 12), bg='white').grid(row=0, column=0, sticky='w', pady=(10, 5))
        self.usuario_entry = tk.Entry(login_frame, font=("Arial", 12), width=30)
        self.usuario_entry.grid(row=1, column=0, padx=10, pady=(0, 10))
        
        tk.Label(login_frame, text="Contraseña", font=("Arial", 12), bg='white').grid(row=2, column=0, sticky='w', pady=(10, 5))
        self.password_entry = tk.Entry(login_frame, font=("Arial", 12), width=30, show="*")
        self.password_entry.grid(row=3, column=0, padx=10, pady=(0, 10))
        
        # Botón de acceso
        login_btn = tk.Button(login_frame, text="Acceder", font=("Arial", 12), 
                             command=self.verificar_login, bg='#3498db', fg='white', width=15)
        login_btn.grid(row=4, column=0, pady=20)
        
        # Centrar frame de login
        main_frame.pack_propagate(False)
    
    def verificar_login(self):
        usuario = self.usuario_entry.get()
        password = self.password_entry.get()
        
        # Verificar contra base de datos
        usuario_bd = self.db.verificar_usuario(usuario, password)
        
        if usuario_bd:
            self.callback_success()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")