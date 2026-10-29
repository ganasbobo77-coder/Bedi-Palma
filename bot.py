import os
import random
import string
import threading
import telebot
from flask import Flask

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)

app_web = Flask('')

@app_web.route('/')
def home():
    return "¡El bot de Telegram está activo y funcionando 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app_web.run(host='0.0.0.0', port=port)

def generar_password(passwords_usadas):
    caracteres = string.ascii_letters + string.digits
    while True:
        password = "".join(random.choice(caracteres) for _ in range(10))
        if password not in passwords_usadas:
            passwords_usadas.add(password)
            return password

# Listas masivas de nombres y apellidos
NOMBRES = [
    "Carlos", "Daniel", "Alejandro", "Jose", "David", "Mateo", "Lucas", "Adrian", "Gabriel", "Samuel",
    "Martin", "Thiago", "Valentin", "Joaquin", "Bruno", "Emiliano", "Felipe", "Dante", "Liam", "Ian",
    "Sofia", "Valentina", "Camila", "Lucia", "Mariana", "Victoria", "Martina", "Catalina", "Elena", "Valeria",
    "Sebastian", "Diego", "Nicolas", "Benjamin", "Julian", "Eduardo", "Fernando", "Ricardo", "Vicente", "Alonso",
    "Isabella", "Gabriela", "Adriana", "Natalia", "Daniela", "Ximena", "Andrea", "Paula", "Regina", "Julieta",
    "Aaron", "Alan", "Alex", "Andres", "Antony", "Axel", "Christian", "Cesar", "Dominic", "Dylan",
    "Abigail", "Alejandra", "Alice", "Alondra", "Amalia", "Amanda", "Amy", "Ana", "Anahi", "Antonia",
    "Emanuel", "Enrique", "Ernesto", "Esteban", "Fabian", "Federico", "Flavio", "Francisco", "Gael", "Giovanni",
    "Ariadna", "Ashley", "Aylen", "Belen", "Bianca", "Carla", "Carolina", "Celeste", "Clara", "Constanza",
    "Gonzalo", "Guillermo", "Gustavo", "Hector", "Hugo", "Isaac", "Ismael", "Ivan", "Jairo", "Javier",
    "Dafne", "Dalila", "Danna", "Delfina", "Denisse", "Diana", "Doris", "Dulce", "Emilia", "Emma",
    "Jesus", "Jonatan", "Jorge", "Josue", "Juan", "Kevin", "Leonardo", "Lorenzo", "Marcos", "Mario",
    "Fatima", "Florencia", "Gisela", "Guadalupe", "Ivanna", "Jazmin", "Jimena", "Karin", "Kiara", "Laila",
    "Manuel", "Maximiliano", "Matias", "Maximo", "Miguel", "Moises", "Nahuel", "Nazareno", "Noel", "Oscar",
    "Liliana", "Lourdes", "Luana", "Luciana", "Luna", "Luz", "Magdalena", "Maite", "Malena", "Marcela",
    "Pablo", "Patricio", "Pedro", "Pietro", "Rafael", "Ramon", "Raul", "Renzo", "Rodrigo", "Rogelio",
    "Margarita", "Maria", "Marta", "Melania", "Melina", "Mia", "Milagros", "Miranda", "Mireia", "Monica",
    "Ruben", "Salvador", "Santos", "Sergio", "Simon", "Tadeo", "Thiago", "Tomas", "Uriel", "Valentin",
    "Nadia", "Naomi", "Natalia", "Nathalie", "Nayeli", "Nicole", "Nidia", "Nieves", "Noelia", "Nora",
    "Vicente", "Victor", "Vito", "Yago", "Yair", "Yan", "Yandel", "Zack", "Zaid",
    "Olivia", "Olimpia", "Oriana", "Paloma", "Pamela", "Paola", "Patricia", "Paz", "Penelope", "Pilar"
]

APELLIDOS = [
    "Perez", "Gomez", "Lopez", "Rodriguez", "Torres", "Morales", "Diaz", "Castillo", "Romero", "Alvarez",
    "Jimenez", "Ruiz", "Hernandez", "Garcia", "Martinez", "Gonzalez", "Fernandez", "Sanchez", "Moreno", "Muñoz",
    "Alonso", "Gutierrez", "Navarro", "Ramos", "Gil", "Serrano", "Blanco", "Molina", "Ortega", "Delgado",
    "Castro", "Ortiz", "Rubio", "Marin", "Sanz", "Iglesias", "Medina", "Garrido", "Santos", "Cortes",
    "Lozano", "Guerrero", "Cano", "Prieto", "Mendez", "Cruz", "Calvo", "Vidal", "Leon", "Vargas",
    "Aguilar", "Arias", "Benitez", "Cabrera", "Campos", "Cardona", "Carrasco", "Carvajal", "Chavez", "Contreras",
    "Coronel", "Duarte", "Espinoza", "Estrada", "Fajardo", "Flores", "Franco", "Fuentes", "Gallardo", "Gallego",
    "Garza", "Gimenes", "Godoy", "Granados", "Guerra", "Guevara", "Heredia", "Huerta", "Hurtado", "Jaimes",
    "Jara", "Jaramillo", "Lara", "Leal", "Ledezma", "Ledesma", "Leyva", "Lira", "Macias", "Maldonado",
    "Manriquez", "Marrero", "Marroquin", "Matas", "Mateos", "Matos", "Medrano", "Mejia", "Mendoza", "Mercado",
    "Miranda", "Montero", "Montes", "Mora", "Mosquera", "Moya", "Narvaez", "Nieto", "Nunez", "Ochoa",
    "Padilla", "Palacios", "Pardo", "Paredes", "Parra", "Pascual", "Paz", "Pena", "Peralta", "Pereda",
    "Pereira", "Picado", "Pino", "Pinto", "Pizarro", "Plaza", "Ponce", "Portillo", "Pozo",
    "Prado", "Puente", "Pulido", "Quezada", "Quintana", "Quintero", "Quiroga", "Ramirez", "Rangel", "Rebolledo",
    "Redondo", "Regalado", "Rendon", "Retamal", "Reyes", "Reynoso", "Riano", "Rios", "Rivas", "Rivera",
    "Robledo", "Robles", "Roca", "Rojas", "Roldan", "Roman", "Rosales", "Rosas", "Rueda", "Saavedra",
    "Salas", "Salazar", "Salgado", "Salinas", "Salvador", "Sancho", "Sandoval", "Santana", "Santiago",
    "Sarabia", "Saura", "Sedano", "Segovia", "Sepulveda", "Serna", "Severino", "Sierra", "Silva", "Solis",
    "Soria", "Soto", "Suarez", "Talavera", "Tapia", "Tejeda", "Tellez", "Tello", "Tijerina", "Tobar",
    "Toledo", "Toro", "Torres", "Tovar", "Trejo", "Trujillo", "Uribe", "Urrutia", "Valdez", "Valdivia"
]

historial_chats = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "🤖 **Bot de Outlook**\n• Usa /nuevo -> Correos listos para copiar", 
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['nuevo'])
def send_nuevo(message):
    chat_id = message.chat.id
    
    if chat_id not in historial_chats:
        historial_chats[chat_id] = set()
        
    texto_perfiles = "📋 **Tus perfiles únicos:**\n\n"
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
            
            # Correo sin puntos y con el dominio completo dentro del bloque para copiarlo fácilmente
            correo_completo = f"{nombre.lower()}{apellido.lower()}{sufijo}@outlook.com"
            
            texto_perfiles += f"👤 **Nombre:** `{nombre} {apellido}`\n📧 **Correo:** `{correo_completo}`\n🔑 **Pass:** `{password}`\n\n"

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("🔄 Generar 2 Nuevos", callback_data="generar_dos"))

    bot.send_message(
        chat_id,
        texto_perfiles,
        reply_markup=markup,
        parse_mode="Markdown"
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "generar_dos":
        send_nuevo(call.message)
        
    bot.answer_callback_query(call.id)

if __name__ == "__main__":
    if not TOKEN:
        raise ValueError("No se encontró el TOKEN en las variables de entorno.")

    try:
        bot.remove_webhook()
        print("Webhook anterior eliminado con éxito de Telegram.")
    except Exception as e:
        print(f"Aviso al limpiar webhook: {e}")

    t_bot = threading.Thread(target=lambda: bot.infinity_polling(skip_pending=True))
    t_bot.daemon = True
    t_bot.start()
    print("🤖 Bot iniciado en segundo plano...")

    print("🌐 Iniciando servidor web Flask...")
    run_web()
