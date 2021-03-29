from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(comment)
admin.site.register(bid)
admin.site.register(auctionlisting)
admin.site.register(Watchlist)