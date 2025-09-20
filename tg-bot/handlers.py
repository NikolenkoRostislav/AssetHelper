import aiohttp
from io import BytesIO
from telegram import Update, InputFile
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, ContextTypes, filters, CallbackContext
from config import settings

async def _download_yt(update: Update, context: CallbackContext, download_type: str = "video"):
        if len(context.args) == 0:
            await update.message.reply_text(f"Please provide a YouTube URL. Usage: /{download_type} <YouTube URL>")
            return

        await update.message.reply_text(f"Downloading {download_type}...")

        url = context.args[0]
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{settings.YT_DOWNLOAD_URL}/{download_type}", params={"url": url}) as resp:
                if resp.status != 200:
                    await update.message.reply_text(f"Failed to download the {download_type}.")
                    return
                download_bytes = await resp.read()

        bio = BytesIO(download_bytes)
        bio.name = "audio.mp3" if download_type == "audio" else "video.mp4"
        bio.seek(0)

        await update.message.reply_document(document=InputFile(bio))

class BotHandlers:
    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Welcome to the Asset Handler bot! Use the /help command for information on using the bot.")

    @staticmethod
    async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("You can send me images and I will remove their backgrounds for you! You can also use the /audio and /video commands with a youtube video URL to download it.")

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
    async def download_yt_audio(update: Update, context: CallbackContext):
        await _download_yt(update, context, download_type="audio")

    @staticmethod
    async def download_yt_video(update: Update, context: CallbackContext):
        await _download_yt(update, context, download_type="video")

    @staticmethod
    def register_handlers(app):
        app.add_handler(CommandHandler("start", BotHandlers.start))
        app.add_handler(CommandHandler("help", BotHandlers.help))
        app.add_handler(CommandHandler("audio", BotHandlers.download_yt_audio))
        app.add_handler(CommandHandler("video", BotHandlers.download_yt_video))
        app.add_handler(MessageHandler(filters.PHOTO, BotHandlers.remove_bg))
