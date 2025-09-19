import aiohttp
from io import BytesIO
from telegram import Update, InputFile
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters
from config import settings

class BotHandlers:
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Welcome to the Asset Handler bot! Use the /help command for information on using the bot.")

    @staticmethod
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("You can send me images and I will remove their backgrounds for you! That's it for now.")

    @staticmethod
    async def remove_bg(update: Update, context: ContextTypes.DEFAULT_TYPE):
        photo = update.message.photo[-1]
        file_id = photo.file_id
        file = await context.bot.get_file(file_id)
        file_bytes = await file.download_as_bytearray()
        
        async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()
            data.add_field("image", file_bytes, filename="photo.png", content_type="image/png")
            async with session.post(f"{settings.REMOVE_BG_URL}/image", data=data) as resp:
                processed_bytes = await resp.read()
        
        bio = BytesIO(processed_bytes)
        bio.name = "updated_image.png"
        bio.seek(0)

        await update.message.reply_document(document=InputFile(bio))

    @staticmethod
    def register_handlers(app):
        app.add_handler(CommandHandler("start", BotHandlers.start))
        app.add_handler(CommandHandler("help", BotHandlers.help))
        app.add_handler(MessageHandler(filters.PHOTO, BotHandlers.remove_bg))
