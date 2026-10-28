import os
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
PORT = int(os.environ.get("PORT", 10000))
WEBHOOK_URL = f"https://bedi-palma-bot.onrender.com/{TOKEN}"

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

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("No se encontró el TOKEN en las variables de entorno.")
    
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("nuevo", generar_credenciales))
    app.add_handler(CallbackQueryHandler(botones_callback))
    
    print("🤖 Iniciando servidor Webhook nativo en Render...")
    
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=WEBHOOK_URL
    )
    
