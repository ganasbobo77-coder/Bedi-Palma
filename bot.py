import os
import random
import string
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# Usamos la variable de entorno para proteger tu token en la nube
TOKEN = os.getenv("TOKEN")

def generar_password():
    caracteres = string.ascii_letters + string.digits + "!@#"
    return "".join(random.choice(caracteres) for _ in range(10))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 **Bot en la Nube (Solo Outlook)**\n\n"
        "• Usa /nuevo -> Genera un perfil con correo @outlook.com.",
        parse_mode="Markdown"
    )

async def generar_credenciales(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nombres = ["Carlos", "Daniel", "Alejandro", "Mateo", "Lucas", "David", "Adrian", "Gabriel", "Samuel", "Julian"]
    apellidos = ["Perez", "Gomez", "Lopez", "Rodriguez", "Martinez", "Sanchez", "Fernandez", "Ramirez", "Torres", "Flores"]
    
    nombre_elegido = random.choice(nombres)
    apellido_elegido = random.choice(apellidos)
    
    numero = random.randint(100, 999)
    dominio = "outlook.com"
    correo = f"{nombre_elegido.lower()}.{apellido_elegido.lower()}{numero}@{dominio}"
    password = generar_password()
    
    context.user_data['ultimo_nombre'] = f"{nombre_elegido} {apellido_elegido}"
    context.user_data['ultimo_correo'] = correo
    context.user_data['ultima_pass'] = password

    texto = (
        "✨ **Nuevos datos (Solo Outlook):**\n\n"
        f"👤 **Nombre:** `{nombre_elegido} {apellido_elegido}`\n"
        f"📧 **Correo:**\n`{correo}`\n\n"
        f"🔑 **Contraseña:**\n`{password}`\n\n"
        "*(Toca los botones de abajo para copiar cada dato)*"
    )
    
    teclado = [
        [InlineKeyboardButton("📋 Copiar Nombre", callback_data="copiar_nombre")],
        [InlineKeyboardButton("📋 Copiar Correo", callback_data="copiar_correo")],
        [InlineKeyboardButton("🔑 Copiar Contraseña", callback_data="copiar_pass")],
        [InlineKeyboardButton("🔄 Generar Otro", callback_data="generar_nuevo")]
    ]
    reply_markup = InlineKeyboardMarkup(teclado)
    
    await update.message.reply_text(texto, parse_mode="Markdown", reply_markup=reply_markup)

async def botones_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    datos = context.user_data
    
    if query.data == "copiar_nombre":
        val = datos.get('ultimo_nombre', 'N/A')
        await query.message.reply_text(f"📋 **Nombre:**\n`{val}`", parse_mode="Markdown")
    elif query.data == "copiar_correo":
        val = datos.get('ultimo_correo', 'N/A')
        await query.message.reply_text(f"📋 **Correo:**\n`{val}`", parse_mode="Markdown")
    elif query.data == "copiar_pass":
        val = datos.get('ultima_pass', 'N/A')
        await query.message.reply_text(f"🔑 **Contraseña:**\n`{val}`", parse_mode="Markdown")
    elif query.data == "generar_nuevo":
        await generar_credenciales(update, context)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("nuevo", generar_credenciales))
    app.add_handler(CallbackQueryHandler(botones_callback))

    print("🤖 Bot en la nube iniciado...")
    app.run_polling()
      
