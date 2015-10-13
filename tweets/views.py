from django.views.generic import View
from django.shortcuts import render
from user_profile.models import User
from models import User, Tweet, HashTag
from tweets.forms import TweetForm, SearchForm
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.template import Context
from django.http import HttpResponse
import json



# Create your views here.
class Index(View):
    def get(self, request):
        params = {}
        params["name"] = "Django"
        return render(request, 'base.html', params)
    def post(self, request):
        return HttpResponse('I am called from a POST request')


class Profile(View):
    def get(self, request, username):  #User profile page reachable from /user/<username> URL
        params = dict()
        user = User.objects.get(username=username)
        tweets = Tweet.objects.filter(user=user)
        params["tweets"] = tweets
        params["user"] = user

        return render(request, 'profile.html', params)

#
class PostTweet(View):
    def post(self, request, username):
        form = TweetForm(self.request.POST)
        if form.is_valid():
            user = User.objects.get(username=username)
            tweet = Tweet(text=form.cleaned_data['text'], user=user, country=form.cleaned_data['country'])
            tweet.save()
            words = form.cleaned_data['text'].split(" ")
            for word in words:
                if word[0] == "#": #Separamos todas las letras del tweet y si empieza con #, se va a crear un hashtag de esa palabra
                    hashtag, created = HashTag.objects.get_or_create(name=word[1:])
                    hashtag.tweet.add(tweet)
        return HttpResponseRedirect('/user/' +username)

class HashTagCloud(View):
    #HashTag page, se llega desde /hashtag/<hashtag> URL
    def get(self, request, hashtag):
        params = dict()
        hashtag = HashTag.objects.get(name=hashtag)
        params["tweets"] = hashtag.tweet

        return render(request, 'hashtag.html', params)

class Search(View):
    #Search all tweets with query /search/?query=<query> URL
    def get(self, request): #Prepara el search form y dsps lo rendea
        form = SearchForm()
        params = dict()
        params['search'] = form
        return render(request, 'search.html', params)

    def post(self, request): #Esto hace la busqueda
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            tweets = Tweet.objects.filter(text_icontains=query)
            context = Context({"query": query, "tweets": tweets})
            return_str = render_to_string('partials/_tweet_search.html', context)
            return HttpResponse(json.dumps(return_str), content_type="application/json")
        else:
            HttpResponseRedirect("/search")