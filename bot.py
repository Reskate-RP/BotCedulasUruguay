#cndefOnTop



import logging
import pandas as pd
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Configuración del logging para ver los mensajes en la consola
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Token de tu bot. Reemplaza 'TOEKN DE TELEGRAM' con el token de tu bot.
TOKEN = 'TOKEN DE TELEGRAM'

# Leer el archivo CSV
df = pd.read_csv('cedulas.csv', header=None, names=['Cedula', 'Nombre', 'Apellido'])

# Preprocesamiento para asegurar que los datos sean cadenas
df['Nombre'] = df['Nombre'].fillna('').apply(str)
df['Apellido'] = df['Apellido'].fillna('').apply(str)

# Función para buscar en el DataFrame
def search_in_csv(query):
    query_parts = query.lower().split()
    matched_records = df.apply(lambda row: all(part in (row['Nombre'].lower() + ' ' + row['Apellido'].lower()) for part in query_parts), axis=1)
    matched_records = df[matched_records]
    
    if matched_records.empty:
        return ['No se encontraron coincidencias. Contactate a @eldgm para mas informacion.']
    else:
        # Construir mensajes con los resultados encontrados
        base_message = 'Resultados:\n'
        messages = []
        current_message = base_message
        for index, row in matched_records.iterrows():
            line = f"{row['Nombre']} {row['Apellido']} - Cédula: {row['Cedula']}\n"
            if len(current_message) + len(line) > 4096:
                messages.append(current_message)
                current_message = base_message + line
            else:
                current_message += line
        messages.append(current_message)  # Agrega el último mensaje
        return messages

# Definir la función que manejará los mensajes del comando /search
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text('Por favor envía el nombre completo y apellido después del comando. Ejemplo: /search John Luciano Andrada Cuello')
        return

    query = ' '.join(context.args)
    results = search_in_csv(query)
    for result in results:
        await update.message.reply_text(result)

# Inicializar la aplicación de Telegram
application = Application.builder().token(TOKEN).build()

# Añadir el handler para el comando /search
application.add_handler(CommandHandler('search', search))

# Iniciar el bot
if __name__ == '__main__':
    application.run_polling()



#https://t.me/eldgm