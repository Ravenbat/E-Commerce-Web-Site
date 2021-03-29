from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("close/<int:id>", views.closelisting, name="closelisting"),
    path("bid/<int:id>", views.bidonitem, name="placebid"),
    path("comment/<int:id>", views.create_comment, name="newcomment"),
    path("categories", views.categories, name="categories"),
    path("category/<str:categoryname>", views.listings_category, name="listings_category"),
    path("watchlist/<int:id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("watchlist", views.get_watchlist, name="watchlist")
]
