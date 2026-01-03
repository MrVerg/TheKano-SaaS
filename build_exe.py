import os
import subprocess
import sys

def build_executable():
    print("🚀 Iniciando proceso de construcción...")
    
    # Check if PyInstaller is installed
    try:
        import PyInstaller
        print("✅ PyInstaller detectado.")
    except ImportError:
        print("❌ PyInstaller no está instalado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # Define the main file
    main_file = "main_flet_moderno.py"
    
    # Define the output name
    app_name = "TheKanoApp"
    
    # Define additional data files (if any)
    # Format: "source;destination" (Windows)
    # We don't have specific assets folder yet, but if we did:
    # add_data = "--add-data 'assets;assets'"
    
    # PyInstaller command arguments
    pyinstaller_args = [
        sys.executable, "-m", "PyInstaller",
        "--noconfirm",
        "--onefile",  # Create a single executable file
        "--windowed", # Hide the console window (GUI app)
        "--name", app_name,
        "--clean",
        # Include essential modules explicitly if needed (usually PyInstaller finds them)
        "--hidden-import", "pymysql",
        "--hidden-import", "fpdf",
        "--hidden-import", "google.generativeai",
        main_file
    ]
    
    print(f"📦 Ejecutando comando: {' '.join(pyinstaller_args)}")
    
    try:
        subprocess.check_call(pyinstaller_args)
        print("\n✅ ¡Construcción exitosa!")
        print(f"📂 El ejecutable se encuentra en la carpeta 'dist': dist/{app_name}.exe")
        print("ℹ️  Nota: Asegúrate de tener XAMPP corriendo antes de ejecutar la aplicación.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error durante la construcción: {e}")

if __name__ == "__main__":
    build_executable()
