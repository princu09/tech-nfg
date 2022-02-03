# Page Redirect , Request Page , Response Page
from unicodedata import category
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
# Login account
from django.contrib.auth import authenticate, login, logout
# import Tables
from .models import Address, Blogpost, Product, Wishlist , Cart
# For Search Query
from django.db.models import Q
# Date Time
import requests
from bs4 import BeautifulSoup

def index(request):
    prod = Product.objects.all().order_by('?')
    laptop = Product.objects.filter(category="laptop").order_by('?')
    return render(request, 'index.html'  , context={'prod' : prod , 'laptop' : laptop})


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


def about(request):
    return render(request, 'about.html')


def shop(request):
    prod = Product.objects.all()
    return render(request, 'shop.html', context={'prod': prod})


def single_product(request, id):
    prod = Product.objects.get(id=id)
    return render(request, 'single_product.html', context={'prod': prod})


def my_account(request):
    return render(request, 'my_account.html')


def make_changes(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        bday = request.POST['bday']

        u = User.objects.update(email=email, first_name=fname, last_name=lname)
    return redirect('/my_account')


def my_address(request):
    current_user = request.user
    a = Address.objects.filter(id=current_user.id)
    return render(request, 'my_address.html', context={'a': a})


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


def handle_login(request):
    if request.method == "POST":
        usrname = request.POST['usrname']
        passwd = request.POST['password']

    user = authenticate(username=usrname, password=passwd)

    if user is not None:
        login(request, user)
        return redirect('/')
    return redirect('/my_account')


def handle_logout(request):
    logout(request)
    return redirect('/')


def blog(request):
    mypost = Blogpost.objects.all()
    return render(request, 'blog.html', {'mypost': mypost})


def blogpost(request, id):
    post = Blogpost.objects.filter(post_id=id)[0]
    return render(request, 'blogpost.html', {'post': post})


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


def removeFromWishlist(request, id):
    i = Wishlist.objects.filter(product=id)
    i.delete()
    return redirect('/my_wishlist')


def my_wishlist(request):
    orders = Wishlist.objects.filter(user=request.user).order_by('-id')
    return render(request, 'wishlist.html', {'orders': orders})


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


def removeFromCart(request, id):
    i = Cart.objects.filter(product=id)
    i.delete()
    return redirect('/cart')


def cart(request):
    orders = Cart.objects.filter(user=request.user).order_by('-id')
    totalPrice = 0
    for i in orders:
        new = i.product.price * i.itemLen
        totalPrice = int(totalPrice) + int(new)
    return render(request, 'cart.html', context={'orders': orders, 'totalPrice': totalPrice})
