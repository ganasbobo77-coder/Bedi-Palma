import os
import random
import string
from threading import Thread
import requests
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")

# Servidor Flask simple para mantener el puerto web abierto que exige Render
app_web = Flask('')

@app_web.route('/')
def home():
    return "¡El bot de Telegram está activo y funcionando!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

def generar_password():
    caracteres = string.ascii_letters + string.digits
    return "".join(random.choice(caracteres) for _ in range(10))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **Bot en la nube (Solo Outlook)**\n• Usa /nuevo -> Genera un perfil",
        parse_mode="Markdown"
    )

async def generar_credenciales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombres = ["Carlos", "Daniel", "Alejandro", "Jose", "David"]
    apellidos = ["Perez", "Gomez", "Lopez", "Rodriguez", "Torres"]
    
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)
    password = generar_password()
    correo = f"{nombre.lower()}.{apellido.lower()}103r03@outlook.com"
    
    context.user_data['ultimo_nombre'] = f"{nombre} {apellido}"
    context.user_data['ultimo_correo'] = correo
    context.user_data['ultima_pass'] = password

    keyboard = [
        [InlineKeyboardButton("📋 Copiar Nombre", callback_data="copiar_nombre")],
        [InlineKeyboardButton("📧 Copiar Correo", callback_data="copiar_correo")],
        [InlineKeyboardButton("🔑 Copiar Pass", callback_data="copiar_pass")],
        [InlineKeyboardButton("🔄 Generar Nuevo", callback_data="generar_nuevo")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"👤 **Nombre:** {nombre} {apellido}\n📧 **Correo:** {correo}\n🔑 **Password:** {password}",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def botones_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    datos = context.user_data

    if query.data == "copiar_nombre":
        val = datos.get('ultimo_nombre', 'N/A')
        await query.message.reply_text(f"📋 **Nombre:** `{val}`", parse_mode="Markdown")
    elif query.data == "copiar_correo":
        val = datos.get('ultimo_correo', 'N/A')
        await query.message.reply_text(f"📧 **Correo:** `{val}`", parse_mode="Markdown")
    elif query.data == "copiar_pass":
        val = datos.get('ultima_pass', 'N/A')
        await query.message.reply_text(f"🔑 **Password:** `{val}`", parse_mode="Markdown")
    elif query.data == "generar_nuevo":
        await generar_credenciales(update, context)

def main():
    if not TOKEN:
        raise ValueError("No se encontró el TOKEN en las variables de entorno.")
    
    # 1. FUERZA BRUTA: Borrar cualquier webhook colgado en los servidores de Telegram antes de arrancar
    url_delete = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook?drop_pending_updates=true"
    try:
        requests.get(url_delete)
        print("Webhook anterior eliminado correctamente de Telegram.")
    except Exception as e:
        print(f"No se pudo limpiar el webhook: {e}")

    # 2. Iniciar Flask en segundo plano para abrir el puerto de Render
    t = Thread(target=run_web)
    t.daemon = True
    t.start()

    # 3. Configurar y arrancar el bot de Telegram
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("nuevo", generar_credenciales))
    app.add_handler(CallbackQueryHandler(botones_callback))
    
    print("🤖 Iniciando bot con polling continuo...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
