from telegram import Update
from telegram.ext import Application
from config import settings
from handlers import BotHandlers

def main():
    app = Application.builder().token(settings.API_KEY).build()
    BotHandlers.register_handlers(app)

    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
