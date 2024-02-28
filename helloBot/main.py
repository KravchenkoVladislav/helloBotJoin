from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    ChatJoinRequestHandler,
    CallbackQueryHandler,
    ContextTypes,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    filters
)
import json

TOKEN = '7022108285:AAF5_fO6kFWppkLLtCR0Mat9tzl_JhNkWxA'

def load_posts_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

posts = load_posts_from_json('posts.json')

async def send_post(context: CallbackContext):
    chat_id = context.job.chat_id
    post = posts.pop(0)  # Видаляємо перший пост з масиву

    markup = InlineKeyboardMarkup([[InlineKeyboardButton("ЧАТ СО МНОЙ 💰", url="https://t.me/your_username")]])

    if post['type'] == 'text':
        await context.bot.send_message(chat_id, post['text'], reply_markup=markup)

    posts.append(post)  # Повторно додаємо пост для циклічного використання

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Привет')

async def chat_join_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [['Я НАСТОЯЩИЙ']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await context.bot.send_video_note(
        chat_id=update.chat_join_request.from_user.id,
        video_note=open('media/videoseka.mp4', 'rb'),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Мoй канал 💎", url="https://t.me/+qwTNaE6uxiVkMjMy")]])
    )
    await context.bot.send_message(
        chat_id=update.chat_join_request.from_user.id,
        text="\nЯ давно в сфере блогов и могу сказать точно - проблема ботов очень мешает видеть настоящую статистику \n\nЯ хочу точно видеть сколько людей приходит по факту, поэтому боты мне тут не нужны \n\nПодтверди по кнопке ниже что ты настоящий пользователь, и тогда сможешь продолжить пользоватся каналом",
        reply_markup=reply_markup
    )

async def confirm_join(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text
    if text == 'Я НАСТОЯЩИЙ':
        chat_id = '-1002094781489'  # ID вашого каналу
        user_id = update.message.from_user.id

        # Бот має бути адміністратором у каналі з правом на додавання користувачів
        await context.bot.approve_chat_join_request(chat_id, user_id)

             # Відправити повідомлення користувачу про успішне приєднання

        await update.message.reply_text(
            "ПРОВЕРКА УСПЕШНО ПРОЙДЕНА ✅",
            reply_markup = ReplyKeyboardRemove()
        )
        await update.message.reply_text(
            "Рахмет что доверяешь мне и становишься частью  нового лучшего будущего! Буду рад помочь тебе увидеть, что ты на самом деле можешь всё, главное захотеть. \n\nНиже есть кнопка, она ведёт на мой канал, там ты можешь видеть информацию и обьявления, а так же много отзывов людей которые уже со мной поработали!\n\nНе медли, переходи по кнопке, тебя ждёт много интересного",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Мой канал 💎", url="https://t.me/+qwTNaE6uxiVkMjMy")]])
        )
        await update.message.reply_text(
            "\nВижу ты заинтересовался моим каналом и у тебя много вопросов! Именно для таких как ты я это все и сделал - собрал серьезную команду профессионалов! Именно для таких как ты - чтобы люди могли жить так как они того заслужили ⭐\n\nУверен у тебя все еще много вопросов - можешь задать их мне лично, кнопка, чтобы перейти в чат со мной -  ниже⬇\n",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ЧАТ СО МНОЙ 💰", url="https://t.me/your_username")]])
        )
        await update.message.reply_text(
            "\nРад что ты заинтересовался моими условиями, это правильный путь к серьезным результатам!\n\nУже многие осуществили свои мечты и цели, теперь твоя очередь, ты 100% это заслужил \n\nНе нужно ждать завтра, начинай прямо сейчас! ⬇Подробнее - по кнопке ниже⬇",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ЧАТ СО МНОЙ 💰", url="https://t.me/your_username")]])
        )


        chatUser = update.message.chat.id
        context.job_queue.run_repeating(send_post, interval=86400, first=0, chat_id=chatUser)
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(ChatJoinRequestHandler(chat_join_request))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_join))
    application.add_handler(CallbackQueryHandler(confirm_join, pattern='^confirm_join$'))

    application.run_polling()

if __name__ == '__main__':
    main()
