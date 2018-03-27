from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^quotes$', views.quotes),
	url(r'^logout$', views.logout),
	url(r'^add_quote$', views.add_quote),
	url(r'^quotes/(?P<quote_id>\d+)/add_to_favorites$', views.add_quote_to_favorites),
	url(r'^quotes/(?P<favorited_quote_id>\d+)/remove_from_favorites$', views.remove_quote_from_favorites),
	url(r'^quotes/(?P<user_id>\d+)/profile$', views.show_profile),
]

