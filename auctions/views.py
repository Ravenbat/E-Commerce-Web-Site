from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from datetime import datetime
from django.db.models import Max
from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": auctionlisting.objects.all()
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    return render(request, "auctions/create.html")

def create_listing(request):
    if request.method  == 'POST':
        al = auctionlisting()
        al.listing_name = request.POST['ltitle']
        al.listing_description = request.POST['ldescription']
        al.listing_image = request.POST['lurl']
        al.listing_category = request.POST['lcategory']
        al.starting_bid = request.POST['lstartbid']
        al.listing_creator = request.user
        al.save()
        return redirect('listing', al.id)

def listing(request, id):
    x = 0
    al = auctionlisting.objects.get(id=id) 
    bids = bid.objects.filter(bidded_on = auctionlisting.objects.get(id=id))
    for i in bids:
        x += 1
    varuser = False
    highestbidder = al.starting_bid
    if x > 0:
        highestbidder = bid.objects.get(amount=al.highest_bid)
        varuser = request.user
        if varuser == highestbidder.bidder:
            varuser = True
    allcomments = comment.objects.filter(listing = al).order_by('-created_at') 
    context={
        'listing': auctionlisting.objects.get(id=id),
        'minbid': int(auctionlisting.objects.get(id=id).starting_bid + 1),
        'user': request.user,
        'bids': x,
        'varuser': varuser,
        'winner' : al.listing_winner,
        'comments': allcomments
    }
    return render(request, 'auctions/listing.html', context)

def closelisting(request, id):
    j = 0
    active = auctionlisting.objects.get(id=id)
    if active.listing_active == True:
        active.listing_active = False
    else:
        active.listing_active = True
    if active.highest_bid != None:
        highestbidder = bid.objects.get(bidded_on = active.id, amount = active.highest_bid)
        active.listing_winner = highestbidder.bidder
    else:
        active.listing_winner = None
    active.save()
    return redirect('index')

def bidonitem(request, id):
    if request.method == "POST":
        number = request.POST.get('bidamount')
        biditem = bid(amount = number, bidder = request.user, bidded_on = auctionlisting.objects.get(id=id))
        biditem.save()
        al = auctionlisting.objects.get(id=id)
        al.highest_bid = number
        al.save()
        return redirect('listing', al.id)

def create_comment(request, id):
    if request.method == 'POST':
        newcomment = comment(text = request.POST.get("comment"), poster = request.user, listing = auctionlisting.objects.get(id=id))
        newcomment.save()
        return redirect('listing', id)

def categories(request):
    a1 = auctionlisting.objects.all()
    print(a1)
    set1 = set()
    for i in a1:
        set1.add(i.listing_category)
    print(set1)
    return render(request, "auctions/categories.html", {
        "al": set1
    })

def listings_category(request, categoryname):
    return render(request, "auctions/listings_in_category.html", {
        "al" : auctionlisting.objects.filter(listing_category = categoryname)
    })

def add_to_watchlist(request, id):
    wl = Watchlist()
    wl.owner = request.user
    wl.ownerlist = auctionlisting.objects.get(id=id)
    wl.save()
    return redirect('listing', id)

def get_watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "wl" : Watchlist.objects.filter(owner = request.user)
    })


    







