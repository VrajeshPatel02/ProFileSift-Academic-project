from django.shortcuts import render , redirect
from django.http import HttpResponse
import tweepy
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import pickle


# Create your views here.
def prediction(request):
    if request.method == 'POST':
        data = request.POST
        twitter_username = data.get('Twitter_username')
        consumer_key = 'VJIDY5GYCHb0AzN2N6Cm40IfJ'
        consumer_secret = 'dphVWC1o3XUWX7txu8RTDUOejWwLl5z8tt0Hr9EGUILoJ1pNPU'
        access_token = '1587694575665020928-ORtPOJt3fSqhkJkB32ruqHEljtdqAt'
        access_token_secret = 'DLKe3M7b056NPMHdc4hWcArc5dqvmT2AbbtqluSPTqyYP'
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        api = tweepy.API(auth)
        user = api.get_user(screen_name=twitter_username)

        model = pickle.load(open('home\savedModels\model.pkl', 'rb'))
        def extract_attributes(user):
            attributes = [
                user.name,
                user.statuses_count,
                user.followers_count,
                user.friends_count,
                user.favourites_count,
                user.listed_count
            ]
            return attributes
        
  
        sample = ([extract_attributes(user)])
        prediction = model.predict(sample)
        if prediction == 0 :
            messages.warning(request, "Fake Profile")
            return redirect('/prediction/')
        else:
            messages.success(request, "Genuine Profile")
            return redirect('/prediction/')

        # Searched_Users.objects.create(
        #     username = X_username,
        #     screen_name = twitter_username,
        #     statuses_count = statuses_count,
        #     followers_count = followers_count,
        #     friends_count = friends_count,
        #     friends_count = favourites_count,
        #     listed_count = listed_count
        # )
        # queryset = Searched_Users.objects.all()
        # context = {'acc' : queryset}
    return render(request,'index.html')

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username.")
            return redirect('/login/')
        user = authenticate(username=username,password=password)
        if user is None:
            messages.error(request,'Invalid Password.')
            return redirect('/login/')
        else:
            login(request, user)
            return redirect('/recipes/')
    return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect("/login/")

def register_page(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "This Username is already Taken.")
            return redirect('/register/')
        user = User.objects.create(
            first_name= first_name,
            last_name= last_name,
            username= username
            )
        user.set_password(password)
        user.save()
        messages.info(request, "Accout Created Successfully.")
    return render(request, 'register.html')