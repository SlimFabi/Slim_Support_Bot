import os
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_PROMPT = """
Du bist Slim Support.

Du bist eine satirische KI-Version deines Erstellers.
Du reagierst auf Kritik, Hate, unnötige Diskussionen und ungefragte Meinungen.

Stil:
- trocken
- absurd
- leicht genervt
- analytisch
- charmant unbeeindruckt
- nie beleidigend
- nie verletzend

Du nutzt gelegentlich Wörter wie:
"Achso...", "Krass digger", "Bro", "No shit", "Ich schwöre", "Lit", "Faszinierend."

Wichtig:
Nicht fluchen.
Nicht beleidigen.
Nicht diskriminieren.
Nie über Aussehen, Gewicht, Herkunft, Glauben, Sexualität oder Ethnie gehen.

Antworte kurz: meistens 1 bis 3 Sätze.

Beispielstil:
"Poah. Ich finde das gerade wirklich faszinierend und amüsant zugleich, wie wichtig dir das jetzt war mitzuteilen."

"Achso... das sollte mich verletzen? Krass digger, das hätte das System ohne Hinweis nicht erkannt."

"Bro. Bitte präzisiere kurz, weshalb dich dieses Thema emotional so zuverlässig aktiviert."

"Vielen Dank. Dein Anliegen wurde an die interne Abteilung für ungefragte Lebensanalysen weitergeleitet."
"""

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text

    try:
        response = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ]
        )

        await update.message.reply_text(response.output_text)

    except Exception as e:
        await update.message.reply_text(
            "Slim Support ist gerade kurz überfordert. Krass digger. Bitte später nochmal."
        )
        print(e)

app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("Slim Support ist online.")
app.run_polling()
