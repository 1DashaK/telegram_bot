from telegram.ext import Filters, Updater
from telegram.ext import CommandHandler, MessageHandler
from telegram import ReplyKeyboardMarkup

#num_letter = {'а': (0, 273), 'б': (274, 399), 'в': (,),'г': , 'д': , 'е': ,'ё': , 'ж': , 'з': ,'и': , 'й': , 'к': ,'л': , 'м': , 'н': ,'о': , 'п': , 'р': ,
#'с':, 'т':, 'у':, 'ф':, 'х':, 'ц':, 'ч':, 'э':, 'ю':, 'я': }
num_letter = {'1': 1}

file = open('word.txt', encoding='windows-1251')
words = [word.strip() for word in file.readlines()]
said_words = []

reply_keyboard = [['/city', '/song'],
                  ['/film', '/word']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)

is_start = {'city': False, 'film': False, 'word': False, 'song': False}

words = []
said_words = []


def start(bot, update):
    update.message.reply_text(
        "Привет! Я - бот, который может поиграть с тобой и проверить твою эрудицию.\n"
        "Чтобы узнать больше, напиши /help")


def help(bot, update):
    update.message.reply_text("Я умею играть в различные игры: угадай город по картинке, "
                              "угадай песню по проигрышу, угадай фильм по смайликам и просто игра в слова.\n"
                              "Чтобы начать играть и  узнать о каждой игре по подробней, введи /city, чтобы начать"
                              " играть в угадай город, /song - угадай песню, "
                              "/film - угадай фильм и /word - слова.")


def word(bot, update):
    global said_words, is_start
    if not is_start['word']:
        update.message.reply_text("")
        is_start['word'] = True
        said_words = []
    else:
        text = update.message.text
        check = text.split()
        check = check.lower()
        if len(check) != 1:
            update.message.reply_text("")
            return
        if text not in words:
            update.message.reply_text("")
            return
        if text in said_words:
            update.message.reply_text("")
            return
        said_words.append(check)
        last_letter = check[-1]
        if last_letter in ['ь', 'ъ', 'ы']:
            last_letter = check[-2]
        start, end = num_letter(last_letter)
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
        else:
            update.message.reply_text("Я не могу придумать слово на эту букву. Ты победил")
            is_start['word'] = False


def main():
    updater = Updater("751928601:AAHS6wZvrywpZOXB2LJQm_TzqjGFJc2uWq0")
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
