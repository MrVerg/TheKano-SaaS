"""
Script para listar los modelos disponibles con tu API key de Gemini
"""
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
print(f"API Key: {api_key[:20]}...")

genai.configure(api_key=api_key)

print("\nListando modelos que soportan generateContent:\n")

try:
    models = genai.list_models()
    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            print(f"MODELO: {model.name}")
            print(f"  Descripcion: {model.description}")
            print()
except Exception as e:
    print(f"Error al listar modelos: {e}")
