from telegram.ext import Filters, Updater, ConversationHandler
from telegram.ext import CommandHandler, MessageHandler

num_letter = {'а': (0, 273), 'б': (274, 669), 'в': (670, 1118), 'г': (1119, 1540), 'д': (1541, 1976), 'е': (1977, 2020),
              'ж': (), 'з': (), 'и': (), 'й': (), 'к': (), 'л': (), 'м': (), 'н': (), 'о': (), 'п': (), 'р': (),
              'с': (), 'т': (), 'у': (), 'ф': (), 'х': (), 'ц': (), 'ч': (), 'э': (), 'ю': (), 'я': ()}

file = open('words.txt', encoding='utf=8')
words = [word.strip() for word in file.readlines()]
said_words = []


def start(bot, update):
    update.message.reply_text(
        "Привет! Я - бот, который может поиграть с тобой и проверить твою эрудицию.\n"
        "Чтобы узнать больше, напиши /help")
    return 'next'


def help(bot, update):
    update.message.reply_text("Я умею играть в различные игры: угадай город по картинке, "
                              "угадай песню по проигрышу, угадай фильм по смайликам и просто игра в слова.\n"
                              "Чтобы начать играть и  узнать о каждой игре по подробней, введи /city, чтобы начать"
                              " играть в угадай город, /song - угадай песню, "
                              "/film - угадай фильм и /word - слова.")
    return 'next'


def word(bot, update):
    global said_words, words
    text = update.message.text
    check = text.split()
    if len(check) != 1:
        update.message.reply_text("1")
        return 'word'
    check = check[0]
    if text not in words:
        update.message.reply_text("2")
        return 'word'
    if text in said_words:
        update.message.reply_text("3")
        return 'word'
    if said_words:
        check_true = said_words[-1]
        if check_true[-1] in ['ь', 'ъ', 'ы']:
            check_true = check_true[:-2]
        if check[0] != check_true[-1]:
            update.message.reply_text('4')
            return 'word'
    said_words.append(check)
    last_letter = check[-1]
    if last_letter in ['ь', 'ъ', 'ы']:
        last_letter = check[-2]
    start, end = num_letter[last_letter]
    num = start
    is_new_word = True
    while True:
        if num != len(words):
            if last_letter != 'я':
                if num > end:
                    is_new_word = False
                    break
            new_w = words[num]
            if new_w not in said_words:
                if new_w[-1] in ['ь', 'ъ', 'ы']:
                    num += 1
                else:
                    break
            else:
                num += 1
    if is_new_word:
        update.message.reply_text(words[num])
        said_words.append(words[num])
    else:
        update.message.reply_text("Я не могу придумать слово на эту букву. Ты победил")
    return 'word'


def music(bot, update):
    bot.send_audio(chat_id=1, audio=open('test.mp3', 'rb'))

def next(bot, update):
    text = update.message.text
    update.message.reply_text('Можешь начинать)')
    return text


def stop(bot, update):
    update.message.reply_text('Надоела эта игра? Можешь поиграть в другую. Если забыл команды, напиши /help')
    return 'next'


conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={
        'next': [MessageHandler(Filters.text, next)],
        'word': [MessageHandler(Filters.text, word)],
        'film': [MessageHandler(Filters.text, film)]
    },

    fallbacks=[CommandHandler('help', help), CommandHandler('stop', stop)]
)


def main():
    updater = Updater("751928601:AAHS6wZvrywpZOXB2LJQm_TzqjGFJc2uWq0")
    dp = updater.dispatcher
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
