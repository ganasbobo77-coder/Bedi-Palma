@bot.message_handler(commands=['nuevo'])
def send_nuevo(message):
    chat_id = message.chat.id
    
    if chat_id not in historial_chats:
        historial_chats[chat_id] = set()
        
    passwords_usadas = set()
    perfiles_generados = 0
    intentos = 0
    
    while perfiles_generados < 2 and intentos < 100:
        intentos += 1
        nombre = random.choice(NOMBRES)
        apellido = random.choice(APELLIDOS)
        combinacion = (nombre, apellido)
        
        if combinacion not in historial_chats[chat_id]:
            historial_chats[chat_id].add(combinacion)
            perfiles_generados += 1
            
            sufijo = random.randint(1000, 9999)
            password = generar_password(passwords_usadas)
            
            # CORREO GENERADO
            usuario_correo = f"{nombre.lower()}{apellido.lower()}{sufijo}@outlook.com"
            
            # Mensaje individual para cada perfil con su propio botón de copia/acción
            texto_perfil = (
                f"👤 **Nombre:** `{nombre} {apellido}`\n"
                f"📧 **Correo:** `{usuario_correo}`\n"
                f"🔑 **Pass:** `{password}`"
            )
            
            # Botón que facilita copiar o usar el correo mediante un enlace de Telegram
            markup = telebot.types.InlineKeyboardMarkup()
            url_copiar = f"https://t.me/share/url?url={usuario_correo}"
            markup.add(telebot.types.InlineKeyboardButton("📋 Copiar / Usar Correo", url=url_copiar))
            
            bot.send_message(
                chat_id,
                texto_perfil,
                reply_markup=markup,
                parse_mode="Markdown"
            )

    # Botón global para generar más
    markup_global = telebot.types.InlineKeyboardMarkup()
    markup_global.add(telebot.types.InlineKeyboardButton("🔄 Generar 2 Nuevos", callback_data="generar_dos"))
    
    bot.send_message(
        chat_id,
        "👇 *¿Deseas generar más perfiles?*",
        reply_markup=markup_global,
        parse_mode="Markdown"
    )
