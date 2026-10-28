import os
import random
import string
import threading
import telebot
from flask import Flask

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

# Servidor Flask en el hilo principal para cumplir con el puerto web que exige Render
app_web = Flask('')

@app_web.route('/')
def home():
    return "¡El bot de Telegram está activo y funcionando 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

def generar_password():
    caracteres = string.ascii_letters + string.digits
    return "".join(random.choice(caracteres) for _ in range(10))

# Almacén temporal de datos por usuario para los botones
ultimos_datos = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "🤖 **Bot en la nube (Solo Outlook)**\n• Usa /nuevo -> Genera un perfil", 
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['nuevo'])
def send_nuevo(message):
    nombres = ["Carlos", "Daniel", "Alejandro", "Jose", "David"]
    apellidos = ["Perez", "Gomez", "Lopez", "Rodriguez", "Torres"]
    
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    password = generar_password()
    correo = f"{nombre.lower()}.{apellido.lower()}103r03@outlook.com"
    
    chat_id = message.chat.id
    ultimos_datos[chat_id] = {
        "nombre": f"{nombre} {apellido}",
        "correo": correo,
        "pass": password
    }

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("📋 Copiar Nombre", callback_data="copiar_nombre"))
    markup.add(telebot.types.InlineKeyboardButton("📧 Copiar Correo", callback_data="copiar_correo"))
    markup.add(telebot.types.InlineKeyboardButton("🔑 Copiar Pass", callback_data="copiar_pass"))
    markup.add(telebot.types.InlineKeyboardButton("🔄 Generar Nuevo", callback_data="generar_nuevo"))

    bot.send_message(
        chat_id,
        f"👤 **Nombre:** {nombre} {apellido}\n📧 **Correo:** {correo}\n🔑 **Password:** {password}",
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    chat_id = call.message.chat.id
    datos = ultimos_datos.get(chat_id, {"nombre": "N/A", "correo": "N/A", "pass": "N/A"})
    
    if call.data == "copiar_nombre":
        bot.send_message(chat_id, f"📋 **Nombre:** `{datos['nombre']}`", parse_mode="Markdown")
    elif call.data == "copiar_correo":
        bot.send_message(chat_id, f"📧 **Correo:** `{datos['correo']}`", parse_mode="Markdown")
    elif call.data == "copiar_pass":
        bot.send_message(chat_id, f"🔑 **Password:** `{datos['pass']}`", parse_mode="Markdown")
    elif call.data == "generar_nuevo":
        send_nuevo(call.message)
        
    bot.answer_callback_query(call.id)

    if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("No se encontró el TOKEN en las variables de entorno.")

    # Borrar cualquier webhook viejo en Telegram antes de arrancar el polling
    try:
        bot.remove_webhook()
        print("Webhook anterior eliminado con éxito de Telegram.")
    except Exception as e:
        print(f"Aviso al limpiar webhook: {e}")

    # 1. Arrancar el bot de Telegram en un hilo secundario independiente
    t_bot = threading.Thread(target=lambda: bot.infinity_polling(skip_pending=True))
    t_bot.daemon = True
    t_bot.start()
    print("🤖 Bot iniciado en segundo plano...")

    # 2. Arrancar Flask en el hilo principal para atender el puerto web de Render
    print("🌐 Iniciando servidor web Flask...")
    run_web()
