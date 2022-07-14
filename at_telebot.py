from ast import If
import telebot

import AudioSegment


# Создаем экземпляр бота
bot = telebot.TeleBot('952446042:AAH3IlkWj7DNVjPrWZjlzA80aS-w22bS45g')

# Функция, обрабатывающая команду /start
@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Аудио бот связи. Пришлите аудио файл, я пришлю текст в ответ)')

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, 'Вы написали: ' + message.text)
    bot.send_message(message.chat.id, 'бот не может обработать больше 20 мб.: ' + message.text)

@bot.message_handler(content_types=["audio"])
def handle_audio(message):    
    file_info = bot.get_file(message.audio.file_id)
    m_size = round(file_info.file_size/1000000,2)
    file_name = message.audio.file_name
    bot.send_message(message.chat.id, 'Вы прислали audio '+ file_name+'; '+str(m_size)+'Mb')
    # ограничение апи https://core.telegram.org/bots/api#getfile
    if  m_size > 20: 
        bot.send_message(message.chat.id, ' не могу скачать больше 20 мб :-( ')
    else:
        downloaded_file = bot.download_file(file_info.file_path)        
        src = '{0}{1}{2}'.format('tmp','\\',file_name)
        with open(src,'wb') as new_file:
            new_file.write(downloaded_file)
        
        bot.send_message(message.chat.id, 'начало обработки '+ message.audio.file_name)
        
        rezult = AudioSegment.audio_to_text(src)
        bot.send_message(message.chat.id, 'Результат \n'+ rezult)


# Запускаем бота
print('Запуск бота')
bot.polling(none_stop=True, interval=0)