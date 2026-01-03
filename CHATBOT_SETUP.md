# Guía de Configuración del Chatbot AI

## Paso 1: Instalar Dependencias

```bash
pip install google-generativeai python-dotenv
```

O instalar todas las dependencias:
```bash
pip install -r requirements.txt
```

## Paso 2: Obtener API Key de Google Gemini (GRATIS)

1. Ve a: https://makersuite.google.com/app/apikey
2. Inicia sesión con tu cuenta de Google
3. Haz clic en "Create API Key"
4. Copia la API key generada

## Paso 3: Configurar la API Key

1. Copia el archivo `.env.example` y renómbralo a `.env`:
   ```bash
   copy .env.example .env
   ```

2. Abre el archivo `.env` y reemplaza `tu_api_key_aqui` con tu API key real:
   ```
   GEMINI_API_KEY=AIzaSyC...tu_api_key_real_aqui
   ```

## Paso 4: ¡Listo!

El chatbot ya está configurado. Cuando ejecutes la aplicación, verás un botón flotante de chat en la esquina inferior derecha.

## Ejemplos de Uso

- "¿Cuántos docentes tenemos?"
- "Busca docentes con el nombre María"
- "Muestra las carreras disponibles"
- "Dame estadísticas del sistema"
- "Genera un reporte de [nombre del docente]"

## Solución de Problemas

### Error: "GEMINI_API_KEY no encontrada"
- Verifica que el archivo `.env` existe en la carpeta del proyecto
- Verifica que la API key está correctamente configurada en `.env`
- Reinicia la aplicación

### El chatbot no responde
- Verifica tu conexión a internet
- Verifica que la API key es válida
- Revisa los logs en la consola

## Límites del Tier Gratuito

- 60 requests por minuto
- Suficiente para uso normal del sistema
- Si necesitas más, considera el tier de pago de Google

## Privacidad

- Solo se envían consultas de texto a la API de Gemini
- No se envían datos sensibles de la base de datos
- Las respuestas se generan en tiempo real
