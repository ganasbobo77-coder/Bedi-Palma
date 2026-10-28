import os
import random
import string
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
# La URL que te da Render para tu servicio web
WEBHOOK_URL = "https://bedi-palma-bot.onrender.com/" + TOKEN

app_web = Flask(__name__)
telegram_app = None

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

@app_web.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), telegram_app.bot)
    asyncot = telegram_app.update_queue.put(update)
    return 'ok'

@app_web.route('/')
def home():
    return "¡El bot de Telegram está activo por Webhook!"

async def setup_bot():
    global telegram_app
    telegram_app = Application.builder().token(TOKEN).build()
    
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("nuevo", generar_credenciales))
    telegram_app.add_handler(CallbackQueryHandler(botones_callback))
    
    await telegram_app.initialize()
    await telegram_app.bot.set_webhook(url=WEBHOOK_URL)
    print("🤖 Webhook configurado correctamente...")

if __name__ == "__main__":
    import asyncio
    asyncio.run(setup_bot())
    
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)
    
