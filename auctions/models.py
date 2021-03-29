from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class auctionlisting(models.Model):
    listing_name = models.CharField(max_length=100)
    listing_description = models.TextField(null=True)
    listing_image = models.TextField(null=True, blank=True)
    listing_created_date = models.DateTimeField(auto_now_add=True, null=True)
    starting_bid = models.IntegerField()
    listing_category = models.CharField(max_length=20)
    listing_creator = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    listing_active = models.BooleanField(default=True)
    listing_winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name = "winner", null=True, blank=True, default=None)
    highest_bid = models.IntegerField(default = None, null=True, blank=True)

    def get_created_date(self):
        return str(self.listing_created_date)[:19]

    def __str__(self):
        return f"{self.listing_name} created at {str(self.listing_created_date)[:19]} by {self.listing_creator} for {self.starting_bid} in {self.listing_category}"
    

class bid(models.Model):
    amount = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    bidded_on = models.ForeignKey(auctionlisting, on_delete=models.CASCADE, null=True)
    bidded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} bidded {self.amount}"

class comment(models.Model):
    text = models.TextField()
    poster = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    listing = models.ForeignKey(auctionlisting, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return f"{self.poster} commented {str(self.created_at)[:19]} sayin {self.text}"

class Watchlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    ownerlist = models.ForeignKey(auctionlisting, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.owner} watched {self.ownerlist}"
    

