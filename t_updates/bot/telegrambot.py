# Telegram Bot
from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, CallbackContext, Dispatcher, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.update import Update
from telegram.bot import Bot
from . import telegramcalendar
from . import utils
from . import messages

from ..models import Order, Product
from django.db.models import Q
import requests


reply_keyboard = [
    [KeyboardButton(text="/getBill"), KeyboardButton(text="/getOffers"), KeyboardButton(text="/techUpdates"), KeyboardButton(text="/about")]]


def start(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    first_name = update.effective_chat.first_name
    last_name = update.effective_chat.last_name
    bot.send_message(chat_id=update.effective_chat.id,
                     text=f"Hello {first_name} {last_name} !! Welcome To TechNFG", reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True, one_time_keyboard=False, input_field_placeholder='Please Select Option'),)


def getOffers(update: Update, context: CallbackContext):
    offers = Product.objects.filter(Q(badge__contains="sale"))
    for i in offers[:10]:
        bot: Bot = context.bot
        bot.send_photo(chat_id=update.effective_chat.id, photo=i.images1, caption=f"<b>{i.title}</b>\n\n<b>Price :</b> {i.price}\n\n<b>Description :</b>\n\t\t\t\t{i.shortDesc}\n\n<a href='http://127.0.0.1:8000/single_product/{i.id}'>🛒 Buy Now on TechNFG</a>",
                       parse_mode='html', reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False, input_field_placeholder='Please Select Option'),)


def techUpdates(update: Update, context: CallbackContext):
    n = "https://newsapi.org/v2/everything?q=apple&from=2022-01-31&to=2022-01-31&sortBy=popularity&apiKey=26ae9ce94adb461eb4cb147a43eb88c1"

    resp = requests.get(n)
    newsapi = resp.json()

    nData = []
    for i in newsapi['articles']:
        nData.append(i)
    for x in nData[:10]:
        # print()
        bot: Bot = context.bot
        bot.send_photo(chat_id=update.effective_chat.id, photo=x['urlToImage'], caption=f"{x['title']}\n\n<b>Details :</b> {x['description']}\n\n<a href='{x['url']}'>📰 Read More</a>",parse_mode='html', reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, one_time_keyboard=False, input_field_placeholder='Please Select Option'),)


def sendPhoto(update: Update, context: CallbackContext):
    photo = open('./static/img/techNFG.png', 'rb')
    send_caption = '<b>About NFG ℹ️ : \n\nThis is a bot built by Python developer of Northfox Group and this bot is for sending every bill and new information to every customer of TechNFG. \n\n<a href="https://mailto:northfoxgroup@hotmail.com">✉️ Mail Us</a> \n\n☎️ Call Us : +919033717372\n\n<a href="https://princu09.github.io">🌎 Support</a></b>'

    bot: Bot = context.bot
    bot.send_photo(chat_id=update.effective_chat.id, photo=photo,
                   caption=send_caption, parse_mode='html', reply_markup=ReplyKeyboardMarkup(
                       reply_keyboard, resize_keyboard=True, one_time_keyboard=False, input_field_placeholder='Please Select Option'
                   ),)


def getBill(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    bot.send_message(chat_id=update.effective_chat.id,
                     text="Please Select a date: \n", reply_markup=telegramcalendar.create_calendar())


def fetchBill(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    mobile = update.message.contact.phone_number[2:]
    bill = Order.objects.filter(date=_billDate).filter(mobile=mobile)
    if len(bill) == 0:
        bot.send_message(chat_id=update.effective_chat.id, text="No Bill Data Available", reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True, one_time_keyboard=False, input_field_placeholder='Please Select Option'
        ))
    else:
        bot.send_message(chat_id=update.effective_chat.id, text=f"Bill ID : {bill[0].id}\nOrder Items : {bill[0].order_Items}\nAmmount : {bill[0].amount}\nPayment Mode : {bill[0].payment_method}\nDate : {bill[0].date}\n\nhttp://127.0.0.1:8000/view_bill/{bill[0].id}", reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, resize_keyboard=True, one_time_keyboard=False, input_field_placeholder='Please Select Option'
        ))

    # f"http://127.0.0.1:8000/view_bill/{bill[0].id}"


def inline_handler(update, context):
    query = update.callback_query
    (kind, _, _, _, _) = utils.separate_callback_data(query.data)
    if kind == messages.CALENDAR_CALLBACK:
        inline_calendar_handler(update, context)


def inline_calendar_handler(update, context):
    selected, date = telegramcalendar.process_calendar_selection(
        update, context)
    global _billDate
    _billDate = date.strftime("%Y-%m-%d")
    if selected:
        context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                 text=messages.calendar_response_message % (
                                     date.strftime("%Y-%m-%d")),
                                 reply_markup=ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Send Phone Number", request_contact=True), KeyboardButton(text="Cancle")]], resize_keyboard=True, one_time_keyboard=False, input_field_placeholder='Please Select Option'),)
        return _billDate


def main():
    updater = Updater(
        "5233843479:AAFjubszLgvvhNAlbZljQL6-HymJUbYTJwo", use_context=True)

    dispatcher: Dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("about", sendPhoto))
    dispatcher.add_handler(CommandHandler("getBill", getBill))
    dispatcher.add_handler(CommandHandler("getOffers", getOffers))
    dispatcher.add_handler(CommandHandler("TechUpdates", techUpdates))
    dispatcher.add_handler(MessageHandler(Filters.contact, fetchBill))
    dispatcher.add_handler(CallbackQueryHandler(inline_handler))

    updater.start_polling()


if __name__ == "__main__":
    main()
