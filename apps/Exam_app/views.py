# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

from .models import *

from django.contrib import messages

#dont forget to import models (and migrate)

# Create your views here.

def index(request):
	return render(request, "Exam_app/index.html")

def register(request):
    
    # pulling response from validator
    response = User.objects.RegisterValidator(request.POST)

    if response['isValid'] == True:
        print "REGISTRATION SUCCESSFUL"
        request.session['user_id'] = response['user'].id
        return redirect ("/quotes")

    else:
        print "REGISTRATION FAILED"
        print response['errors']
        for error in response['errors']:
            messages.error(request,error)
        return redirect("/")

def login(request):

    response = User.objects.LoginValidator(request.POST)

    if response['isValid'] == True:
        print "LOGIN SUCCESSFUL"
        request.session['user_id'] = response['user'].id
        return redirect("/quotes")

    else:
        print "LOGIN FAILED"
        print response['errors']
        for error in response['errors']:
            messages.error(request, error)
        return redirect("/")

def quotes(request):

	context ={}
	context['user'] = User.objects.get(id=request.session['user_id'])
	context['quotes'] = Quote.objects.all()
	# print "HERE", context['quotes']
	context['favorites'] = Favorite.objects.filter(favoritor_id = request.session['user_id'])
	context['unfavorited_quotes'] = []

	for quote in context['quotes']:
		print quote.id
		search =Favorite.objects.filter(favorited_id=quote.id, favoritor_id= context['user'])
		if len(search) ==0:
			context['unfavorited_quotes'].append(quote)

	print context['unfavorited_quotes']

	return render(request, "Exam_app/home.html", context)

def add_quote(request):

	response = Quote.objects.QuoteValidator(request.POST)

	if len(response['errors']) > 0:
		print "Failed"
		for error in response['errors']:
			messages.error(request, error)
		return redirect("/quotes")

	else:

		print "Sucessful"
		new_quote = Quote.objects.create(
			quote = request.POST['quote'],
			source = request.POST['source'],
			uploader_id = request.session['user_id']
			)
		return redirect("/quotes")

def add_quote_to_favorites(request, quote_id):

	favorited_quote = Favorite.objects.create(
		favoritor_id = request.session['user_id'],
		favorited_id = quote_id,
		)
	return redirect("/quotes")

def remove_quote_from_favorites(request, favorited_quote_id):

	favorited_quote = Favorite.objects.get(id = favorited_quote_id)
	favorited_quote.delete()
	return redirect("/quotes")

def show_profile(request, user_id):

	context ={}
	context['user'] = User.objects.get(id=user_id)
	context['quotes'] = Quote.objects.filter(uploader_id = user_id)
	context['count'] = len(context['quotes'])

	print context['count']

	return render(request, "Exam_app/profile.html", context)

def logout(request):

	request.session.clear()

	return redirect("/")

 
