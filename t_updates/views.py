from datetime import date
from email.message import Message
from traceback import print_tb
from django.contrib import messages
# Forieng key
from django.contrib.auth.models import User
# Json Response For Ajax
from django.http import JsonResponse
# Page Redirect , Request Page , Response Page
from django.shortcuts import render, redirect
# Login account
from django.contrib.auth import authenticate, login, logout
from matplotlib.pyplot import text
import telegram
# import Tables
from .models import Blogpost, Order, Product, Subscribe, Wishlist, Cart
# For Search Query
from django.db.models import Q
# Request For Tech News
import requests
from bs4 import BeautifulSoup

from telegram.ext import Updater, CallbackQueryHandler, CommandHandler, CallbackContext, Dispatcher, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup
from telegram.update import Update
from telegram.bot import Bot
from .bot import telegramcalendar
from .bot import utils
from .bot import messages


# Home Page Function
def index(request):
    prod = Product.objects.all().order_by('?')
    laptop = Product.objects.filter(category="laptop").order_by('?')
    return render(request, 'index.html', context={'prod': prod, 'laptop': laptop})


# Shop Page Function
def shop(request):
    prod = Product.objects.all()
    return render(request, 'shop.html', context={'prod': prod})


# Single Product View Page Function
def single_product(request, id):
    prod = Product.objects.get(id=id)
    releted = Product.objects.filter(Q(category__contains=prod.category))
    return render(request, 'single_product.html', context={'prod': prod, 'releted': releted})


# Product View By Category Function
def product_category(request, category):
    prod = Product.objects.filter(category=category)
    category = category
    return render(request, 'shop.html', context={'prod': prod, 'category': category})


def compare_product(request, prod1, prod2):
    prod1 = Product.objects.get(id=prod1)
    prod2 = Product.objects.get(id=prod2)
    return render(request, 'compare_product.html', context={'prod1': prod1, 'prod2': prod2})


# Offers & Promocode Page Function
def offers_promocode(request):
    url = "https://www.grabon.in/flight-coupons/"

    # Make a GET request to fetch the raw HTML content
    html_content = requests.get(url).text

    # Parse the html content
    soup = BeautifulSoup(html_content, "html")

    allData = soup.findAll(class_='go-cpn-show')

    disData = []
    titleData = []
    descData = []

    for i in allData:
        for a in i.findAll("span", class_=[]):
            disData.append(a.text)
        for b in i.findAll("span", class_=['txt']):
            disData.append(b.text)
        title = i.findAll("p", class_=[])
        for c in i.findAll("span", class_=['per']):
            disData.append(b.text)
        for d in i.findAll("p", class_=[]):
            titleData.append(d.text)
        desc = i.findAll("span", class_=['visible-lg'])
        for e in desc:
            descData.append(e.text)
    data = zip(disData, titleData, descData)
    context = {'data': data}
    return render(request, 'offers_promocode.html', context)


# Tech Updates Page Function
def updates(request):
    # news api
    n = "https://newsapi.org/v2/everything?q=apple&from=2022-01-31&to=2022-01-31&sortBy=popularity&apiKey=26ae9ce94adb461eb4cb147a43eb88c1"

    resp = requests.get(n)
    newsapi = resp.json()
    print(newsapi)

    nData = []
    for i in newsapi['articles']:
        print(i)
        nData.append(i)

    context = {'nData': nData}
    return render(request, 'tech-updates.html', context)


# About Page Function
def about(request):
    return render(request, 'about.html')


# My Account Function
def my_account(request):
    return render(request, 'my_account.html')


# Make Changes in My Account Function
def make_changes(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        bday = request.POST['bday']

        u = User.objects.update(email=email, first_name=fname, last_name=lname)
    return redirect('/my_account')


# My Account Function
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'my_orders.html', context={'orders': orders})


# View Bill
def view_bill(request, id):
    bill = Order.objects.get(id=id)
    item = []
    for i in bill.order_Items:
        item.append(i)
    itemLen = []
    for i in bill.itemLen:
        itemLen.append(i)
    price = []
    for i in bill.price:
        price.append(i)
    data = zip(item, itemLen, price)
    return render(request, 'view_bill.html', context={'bill': bill, 'data': data})


# Add Product in Wishlist
def add_wishlist(request):
    pid = request.GET['product']
    product = Product.objects.get(id=pid)
    data = {}
    checkw = Wishlist.objects.filter(
        product=product, user=request.user).count()
    if checkw > 0:
        data = {
            'bool': False
        }
    else:
        wishlist = Wishlist.objects.create(
            product=product,
            user=request.user
        )
        data = {
            'bool': True
        }
    return JsonResponse(data)


# Remove Product from Wishlist
def removeFromWishlist(request, id):
    i = Wishlist.objects.filter(product=id)
    i.delete()
    return redirect('/cart')


# Wishlist Page
def my_wishlist(request):
    orders = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'wishlist.html', {'orders': orders})


# Add Product in Cart
def add_cart(request):
    pid = request.GET['product']
    item = request.GET['cartItem']
    product = Product.objects.get(id=pid)
    data = {}
    checkw = Cart.objects.filter(
        product=product, user=request.user).count()
    if checkw > 0:
        data = {
            'bool': False
        }
        cart = Cart.objects.filter(product=product, user=request.user)
        item = int(cart[0].itemLen) + int(item)
        cart = Cart.objects.filter(
            product=product, user=request.user).update(itemLen=item)
    else:
        cart = Cart.objects.create(
            product=product,
            user=request.user, itemLen=item
        )
        data = {
            'bool': True
        }
    return JsonResponse(data)


# Remove Product from Wishlist
def removeFromCart(request, id):
    i = Cart.objects.filter(product=id)
    i.delete()
    return redirect('/cart')


# Cart Page
def cart(request):
    orders = Cart.objects.filter(user=request.user).order_by('-id')
    totalPrice = 0
    for i in orders:
        new = i.product.price * i.itemLen
        totalPrice = int(totalPrice) + int(new)
    return render(request, 'cart.html', context={'orders': orders, 'totalPrice': totalPrice})


# Show Cart Total in Header
def check_cart_price(request):
    price = Cart.objects.filter(user=request.user)
    sum = 0
    for i in price:
        sum = sum + int(i.product.price * i.itemLen)
    data = {
        'sum': sum
    }
    return JsonResponse(data)


def checkout(request):
    if request.method == "POST":
        order_Items = Cart.objects.filter(user=request.user)
        items = []
        price = []
        itemLen = []
        for i in order_Items:
            items.append(i.product.title)
            price.append(i.product.price)
            itemLen.append(i.itemLen)
        amount = 0
        for i in order_Items:
            new = i.product.price * i.itemLen
            amount = int(amount) + int(new)
        address1 = request.POST['address1']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']
        Order.objects.create(user=request.user, order_Items=items, price=price, itemLen=itemLen, amount=amount,
                             address1=address1, address2=address2, city=city, state=state, zip=zip)

        a = Cart.objects.filter(user=request.user)
        a.delete()
        return redirect('/')

    prod = Cart.objects.filter(user=request.user)
    totalPrice = 0
    for i in prod:
        new = i.product.price * i.itemLen
        totalPrice = int(totalPrice) + int(new)
    return render(request, 'checkout.html', context={'prod': prod, 'totalPrice': totalPrice})


# Blog Page
def blog(request):
    mypost = Blogpost.objects.all()
    return render(request, 'blog.html', {'mypost': mypost})


# View Blog Post
def blogpost(request, id):
    post = Blogpost.objects.filter(post_id=id)[0]
    return render(request, 'blogpost.html', {'post': post})


# Subscribe Email
def subscribe(request):
    if request.method == "POST":
        subscribe_email = request.POST['subscribe_email']

        a = Subscribe.objects.filter(email=subscribe_email)
        if len(a) == 0:
            Subscribe.objects.create(email=subscribe_email)
            messages.success(
                request, 'Subscribe Email Added successfully saved.')
            return redirect('/')
        else:
            return redirect('/')


def place_order(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        address1 = request.POST['address1']
        address2 = request.POST['address2']
        city = request.POST['city']
        state = request.POST['state']
        zip = request.POST['zip']

        return redirect('/')


# Search Data
def search(request):
    if request.method == "POST":
        q = request.POST['q']
        prod = Product.objects.filter(Q(title__contains=q) | Q(
            desc__contains=q) | Q(shortDesc__contains=q) | Q(category__contains=q))
        return render(request, 'search.html', context={'q': q, 'prod': prod})


# Create Account
def handle_signup(request):
    if request.method == 'POST':
        usrname = request.POST['usrname']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        passwd = request.POST['pass']

        user = User.objects.create_user(
            username=usrname, first_name=fname, last_name=lname, email=email, password=passwd)
        user.save()

        user = authenticate(username=usrname, password=passwd)

        if user is not None:
            login(request, user)
            return redirect('/')

    return redirect('/my_account')


# Login Account
def handle_login(request):
    if request.method == "POST":
        usrname = request.POST['usrname']
        passwd = request.POST['password']

    user = authenticate(username=usrname, password=passwd)

    if user is not None:
        login(request, user)
        return redirect('/')
    return redirect('/my_account')


# Logout Function
def handle_logout(request):
    logout(request)
    return redirect('/')


# Telegram Bot

updater = Updater(
    "5233843479:AAFjubszLgvvhNAlbZljQL6-HymJUbYTJwo", use_context=True)

dispatcher: Dispatcher = updater.dispatcher


reply_keyboard = [
    [KeyboardButton(text="/sendbill"), KeyboardButton(text="/about")]]


def start(update: Update, context: CallbackContext):
    bot: Bot = context.bot
    first_name = update.effective_chat.first_name
    last_name = update.effective_chat.last_name
    bot.send_message(chat_id=update.effective_chat.id,
                     text=f"Hello {first_name} {last_name} !! Welcome To TechNFG", reply_markup=ReplyKeyboardMarkup(keyboard=reply_keyboard, resize_keyboard=True, one_time_keyboard=False, input_field_placeholder='Please Select Option'),)


def sendBill(update: Update, context: CallbackContext):
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


def sendPhoto(update: Update, context: CallbackContext):
    photo = open('./static/img/techNFG.png', 'rb')
    send_caption = '<b>About NFG ℹ️ : \n\nThis is a bot built by Python developer of Northfox Group and this bot is for sending every bill and new information to every customer of TechNFG. \n\n<a href="https://mailto:northfoxgroup@hotmail.com">✉️ Mail Us</a> \n\n☎️ Call Us : +919033717372</b>'

    bot: Bot = context.bot
    bot.send_photo(chat_id=update.effective_chat.id, photo=photo,
                   caption=send_caption, parse_mode='html', reply_markup=ReplyKeyboardMarkup(
                       reply_keyboard, resize_keyboard=True, one_time_keyboard=False, input_field_placeholder='Please Select Option'
                   ),)


dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(CommandHandler("about", sendPhoto))
dispatcher.add_handler(CommandHandler("sendbill", sendBill))
dispatcher.add_handler(MessageHandler(Filters.contact, fetchBill))
dispatcher.add_handler(CallbackQueryHandler(inline_handler))

updater.start_polling()
