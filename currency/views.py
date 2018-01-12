from django.shortcuts import redirect
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,authenticate,logout
from .forms import CurrencyForm
from django.http import HttpResponse
import requests
from django.http import JsonResponse
import unicodedata
from django.utils import timezone
from .models import Currency


def frontpage(request):
	return render(request,'currency/frontpage.html')


def formpage(request):
	if request.method=="POST":
		form = CurrencyForm(request.POST)
		from_data=request.POST["fr"]
		to_data=request.POST["to"]
		to_data = str(to_data)
		link="https://api.fixer.io/latest?base="
		s = link+from_data
		result = requests.get(s)
		prices = result.json()
		act_rates = prices['rates']
		act_price =act_rates[to_data]
		date=timezone.now()
		ans=str(from_data) + 'to' + str(to_data) + 'at'+ str(date)
		Currency.objects.create(data=ans)
		return render(request,'currency/outputpage.html',{'result':act_price})
	else:
		link="https://api.fixer.io/latest"
		result = requests.get(link)
		res = result.json()
		codes = res['rates'].keys()
		codess=[]
		for i in codes:
			codess.append(unicodedata.normalize('NFKD', i).encode('ascii','ignore'))
		form = CurrencyForm()
		return render(request,'currency/formpage.html', {'form':form,'codess':codess})



def signup(request):
	if request.method=='POST':
		form=UserCreationForm(request.POST)
		if form.is_valid():
			obj=form.save(commit=False)
			username=form.cleaned_data.get("username")
			password=form.cleaned_data.get("password1")
			obj.save()
			user=authenticate(username=username,password=password)
			login(request,user)
			return redirect('formpage')

	else:
		form=UserCreationForm()
		return render(request,'currency/signup.html',{'form':form})



def signin(request):
	print(request)
	if request.method =='POST':
		form=AuthenticationForm(request.POST)
		print(form)
		username=request.POST['username']
		password=request.POST['password']
		print(form)
		user=authenticate(username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('formpage')
	else:
		form=AuthenticationForm()
		return render(request,'currency/signin.html',{'form':form})


def signout(request):
	logout(request)
	return render(request,'currency/frontpage.html')
