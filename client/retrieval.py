#!/usr/bin/env python
# bot para manejar la respuesta del usuario despues de estar en un estado determinado
from telegram import (ReplyKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import logging
#importando lo de apache thrift
import sys
#apache thrift genera la carpeta 'gen-py' la renombre como 'genpy' y la importe aca
from genpy.bot import Publish
from genpy.bot.ttypes import *

#importando librerias core de apache thrift
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

#funcion range() genera una lista de numeros, en este caso, Gender =0
GENDER, PHOTO, LOCATION, PROPUESTA,BIO = range(5)
# estrategia de accion: 1.mensaje de bienvenida. 2-proponemos una alternitiva a la pregunta. 3- recibimos informacion, 4- agradecemos
def propuesta(bot, update):
    user = update.message.from_user
    logger.info("la opcion fue: %s" % ( update.message.text))
    bot.sendMessage(update.message.chat_id, text='Como preguntarias acerca del horario de atencion? ')
    return BIO

def start(bot, update):
    reply_keyboard = [['Horario', 'precios', 'Otro']]

    bot.sendMessage(update.message.chat_id,
                    text='*Hola* _esto es solo para entrenar, favor escoge la instruccion que quieras_ '
                         'Envia /cancel para terminar la conversacion.\n\n'
                         'Escoge un tema:',
                    reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
                    parse_mode='Markdown', disable_web_page_preview=True
                    )
    return PROPUESTA


def bio(bot, update):
    user = update.message.from_user
    logger.info("la respuesta es %s: %s" % (user.first_name, update.message.text))
    sendQuestion(user.first_name, update.message.text)
    bot.sendMessage(update.message.chat_id,
                    text='muchas gracias por tu ayuda %s.' % (user.first_name))

    return ConversationHandler.END


def cancel(bot, update):
    user = update.message.from_user
    logger.info("User %s canceled the conversation." % user.first_name)
    bot.sendMessage(update.message.chat_id,
                    text='Bye! I hope we can talk again some day.')

    return ConversationHandler.END


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

#funcion para enviar la informacion
def sendQuestion(usr,qt):
    logger.info("!!!!!!!!!!!!!!!!!!!!!!!! entrando a guardar !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    user= str(usr)
    quest = str(qt)
    #logger.info(type(user_tmp))
    #logger.info(type(question_tmp))
    try:
    	#hacemos la conexion
    	transport = TSocket.TSocket('localhost', 9090)
    	transport = TTransport.TFramedTransport(transport)
    	protocol = TBinaryProtocol.TBinaryProtocol(transport)
    	#creamos nuestro cliente
    	client = Publish.Client(protocol)
    	transport.open()

    	question = Question()
        question.id = 1000
        #colocamos el usuario
    	question.user = user
        #metemos el twit
    	question.question = quest
    	#hacemos las llamadas al sistema
    	client.save(question)

    	transport.close()

    except Thrift.TException, tx:
    	print '%s' % (tx.message)

def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater("token")

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={
            PROPUESTA: [RegexHandler('^(Horario|precios|Otro)$', propuesta)],

            BIO: [MessageHandler([Filters.text], bio)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
