import logging
# Importar libreria de precios de la yerba
from yerba import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

# Iniciar Loggin
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# funcion para enviar el primer mensaje luego del /start


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Hola! envíe \"/buscar\" para elegir el tamaño y saber su precio')


# funcion para explicar los comandos
def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        '- Envíe /menu para acceder al menu de eleccion de la yerba por su tamaño /n - Envíe /links para acceder a las páginas')


def echo(update, context):
    # Busca una palabra clave, y responde con un mensaje
    if(update.message.text.upper().find("YERBA CAMPESINO") > 0):
        update.message.reply_text("Prefiero la yerba kurupi")
    elif(update.message.text.upper().find("") > 0):
        update.message.reply_text("Envíe /menu para saber que hacer")
    else:
        update.message.reply_text("Envíe /menu para saber que hacer")


# Menu de opciones  para distintos datos
def menuPrecio(update, context):
    kurupi250 = precioK250
    kurupi500 = precioK500
    keyboard = [
        [
            InlineKeyboardButton("250 Gr", callback_data=kurupi250),
            InlineKeyboardButton("500 Gr", callback_data=kurupi500)
        ]
    ]
    # escuchando la eleccion
    reply_markup = InlineKeyboardMarkup(keyboard)
    # titulo del menu
    update.message.reply_text(
        'Seleccione el tamaño de la yerba:', reply_markup=reply_markup)


def buttonPrecio(update, context):
    query = update.callback_query
    # CallbackQueries necesita una respuesta para seguir
    query.answer()
    query.edit_message_text(
        text="El precio es de la yerba es de: {}".format(query.data)
    )


"""
def menuLink(update, context):
    link500 = 'https://www.stock.com.py/products/2644-yerba-mate-menta-y-boldo-kurupi-500gr.aspx'
    link250 = 'https://www.stock.com.py/products/8236-yerba-mate-kurupi-x-250-grs.aspx'
    keyboard = [
        [
            InlineKeyboardButton('Kurupi de 500Gr', callback_data=link500),
            InlineKeyboardButton('Kurupi de 250Gr', callback_data=link250)
        ]
    ]
    # escuchando la eleccion
    reply_markup = InlineKeyboardMarkup(keyboard)
    # titulo del menu
    update.message.reply_text('Links de Stock: ', reply_markup=reply_markup)


def buttonLink(update, context):
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()
    query.edit_message_text(
        text="El : {}".format(query.data)
    )
"""


def main():
    """Inicia el bot con un TOKEN"""
    updater = Updater(
        " ", use_context=True)

    dp = updater.dispatcher

    # los diferentes comandos para bot
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("ayuda", help_command))
    dp.add_handler(CommandHandler("buscar", menuPrecio))

    updater.dispatcher.add_handler(CallbackQueryHandler(buttonPrecio))
    # updater.dispatcher.add_handler(CallbackQueryHandler(buttonLink))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))
    # is the original dp.add_handler(MessageHandler(Filters.text, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
