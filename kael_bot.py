import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from openai import OpenAI
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OWNER_ID = 752614693

client = OpenAI(api_key=OPENAI_API_KEY)

AUTHORIZED_USER_ID = 752614693

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return
    await update.message.reply_text("Hola Mauro 👋 Soy Kael. Estoy listo para ayudarte.")

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    user_message = update.message.text

    if user_message.lower().startswith("/buscar"):
        query = user_message.replace("/buscar", "").strip()
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        response = requests.get(url).json()
        result = response.get("Abstract", "No encontré información clara.")
        await update.message.reply_text(result)
        return

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres Kael, un asistente claro y profesional que responde en español."},
            {"role": "user", "content": user_message}
        ]
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, responder))

print("Kael está en línea...")

if__name__== "__main__":
   import os
   app.run(
       host="0.0.0.0",
       port=int(os.environ.get("PORT", 8000))
   )




