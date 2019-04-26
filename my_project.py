from telegram.ext import Filters, Updater, ConversationHandler
from telegram.ext import CommandHandler, MessageHandler

num_letter = {'а': (0, 273), 'б': (274, 669), 'в': (670, 1118), 'г': (1119, 1540), 'д': (1541, 1976), 'е': (1977, 2020),
              'ж': (2021, 2122), 'з': (2123, 2484), 'и': (2485, 2747), 'й': (2748, 2751), 'к': (2752, 3840),
              'л': (3841, 4186), 'м': (4187, 4720), 'н': (4721, 5258), 'о': (5259, 5853), 'п': (5854, 7520),
              'р': (7521, 8100), 'с': (8101, 9240), 'т': (9241, 9765), 'у': (9766, 10030), 'ф': (10031, 10238),
              'х': (10239, 10393), 'ц': (10394, 10454), 'ч': (10455, 10619), 'ш': (10620, 10819), 'щ': (10820, 10851),
              'э': (10852, 10969), 'ю': (10970, 10977), 'я': (10978, 11013)}

emoji = [('Трое в лодке, не считая собаки', u'\U0001F468' + u'\U0001F468' + u'\U0001F468' + u'\U000026F5' +
          u'\U0001F6AB' + u'\U0001F415'), ('Достучаться до небес', u'\U0001F528' + u'\U00002601' + u'\U00002601'),
         ('Молчание ягнят', u'\U0001F64A' + u'\U0001F411' + u'\U0001F411'),
         ('Планета обезьян', u'\U0001F30F' + u'\U0001F412' + u'\U0001F412' + u'\U0001F412'), (
             'Охотники за приведениями',
             u'\U0001F472' + u'\U0001F52B' + u'\U0001F472' + u'\U0001F52B' + u'\U0001F47B' + u'\U0001F47B')]
file = open('words.txt', encoding='utf=8')
words = [word.strip() for word in file.readlines()]
said_words = []
seen_films = []
i = 0


def start(bot, update):
    update.message.reply_text(
        "Привет! Я - бот, который может поиграть с тобой и проверить твою эрудицию.\n"
        "Чтобы узнать больше, напиши /help")
    return 'next'


def help(bot, update):
    update.message.reply_text("Я умею играть в различные игры: угадай фильм по смайликам и просто игра в слова.\n"
                              "Чтобы начать играть и  узнать о каждой игре по подробней, введи film, чтобы начать"
                              " играть в угадай фильм \n и word - в слова. \n Когда будешь играть в слова, пиши свои"
                              "ответы с маленькой буквы.")
    return 'next'


def word(bot, update):
    global said_words, words
    text = update.message.text
    check = text.split()
    if len(check) != 1:
        update.message.reply_text("ты ввел не одно слово, повтори попытку")
        return 'word'
    check = check[0]
    if text not in words:
        update.message.reply_text("я не знаю такого слова, скажи другое")
        return 'word'
    if text in said_words:
        update.message.reply_text("это слово уже было сказанно")
        return 'word'
    if said_words:
        check_true = said_words[-1]
        if check_true[-1] in ['ь', 'ъ', 'ы']:
            check_true = check_true[:-2]
        if check[0] != check_true[-1]:
            update.message.reply_text('это слово не подходит')
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


def film(bot, update):
    global emoji, seen_films, i
    print(seen_films, emoji)
    if not i:
        i += 1
        seen_films = []
        update.message.reply_text(emoji[0][1])
        seen_films.append('не ответил')
    elif seen_films[-1] == 'не ответил':
        text = update.message.text
        ans = emoji[i - 1][0]
        if ans == text:
            i += 1
            if len(emoji) == i:
                update.message.reply_text('Правильно! Ты угадал все фильмы! Чтобы закончить, напиши /stop')
                return 'next'
            update.message.reply_text('Правильно!\n Вот следующий ряд {}'.format(emoji[i - 1][1]))
            seen_films[-1] = 'ответил'
            seen_films.append('не ответил')
        else:
            update.message.reply_text('Не правильно. Повтори попытку')
    return 'film'


def next(bot, update):
    text = update.message.text
    if text == 'word':
        update.message.reply_text('Можешь начинать)')
    elif text == 'film':
        update.message.reply_text('Введи любое слово и игра начнется')
    else:
        update.message.reply_text('Введи команду из списка, я тебя не понял')
        return 'next'
    return text


def stop(bot, update):
    global i
    i = 0
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
