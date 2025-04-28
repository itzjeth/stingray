from django.http import HttpResponse
from django.contrib import admin
from django.shortcuts import render,redirect, get_object_or_404
from django.db.models import Q
from django.db import connection, transaction
from forms import UserForm,ReviewForm,AdminForm 
from models import  Users,Review,Admin
from django.utils.safestring import mark_safe
from django.templatetags.static import static
from django.contrib import messages
"""{% load static %}"""
import datetime
cursor = connection.cursor()








     
def home_page(request,):
    return render(request, 'pages/home.html')

def chatbot_page(request):
    return render(request, 'pages/chatbot.html')

def dashboard_page(request):
    return render(request, 'pages/dashboard.html')

def chatbot_front(request):
    return render(request, 'pages/chatbot_front.html')

def userHomePage(request):
    return render(request, 'pages/userHome.html')
     
def userReview(request):
    alert = None
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                alert = 'success'
            except Exception as e:
                print("Error saving form:", e)  # ✅ Add this
                alert = 'error'
        else:
            print("Form is invalid:", form.errors)  # ✅ Debug invalid form
            alert = 'error'
    else:
        form = ReviewForm()

    return render(request, "pages/home.html", {'form': form, 'alert': alert})

def review_list(request):
    query = request.GET.get('q')
    reviews = Review.objects.all()
    if query:
        reviews = reviews.filter(
            Q(user__icontains=query) |
            Q(email__icontains=query) |
            Q(message__icontains=query)
        )
    return render(request, 'pages/review_list.html', {'reviews': reviews})

def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = ReviewForm()
    return render(request, 'pages/review_form.html', {'form': form})

def review_update(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = ReviewForm(instance=review)
    return render(request, 'pages/review_form.html', {'form': form})

def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    return render(request, 'pages/review_confirm_delete.html', {'review': review})







def doLogin(request):
	if request.method == "POST":
		uid = request.POST.get('userId', '')
		upass = request.POST.get('userpass', '')
		utype = request.POST.get('type', '')

		if utype == "Admin":
			for a in Admin.objects.raw('SELECT * FROM TB_Admin WHERE AdminId="%s" AND AdminPass="%s"' % (uid, upass)):
				if a.AdminId == uid:
					request.session['AdminId'] = uid
					return render(request, "pages/base.html")
			else:
				messages.error(request, "Incorrect username or password")
				return redirect("home")

		if utype == "User":
			for a in Users.objects.raw('SELECT * FROM TB_Users WHERE userEmail="%s" AND userPass="%s"' % (uid, upass)):
				if a.userEmail == uid:
					request.session['CustId'] = uid
					request.session['user_name'] = a.userName
					request.session['user_image'] = a.userImage.url if a.userImage else '/media/profile_images/default.png'
					return render(request, "pages/chatbot.html")
			else:
				messages.error(request, "Incorrect username or password")
				return redirect("home")

def edit_profile(request):
    user_email = request.session.get('CustId')
    user = Users.objects.get(userEmail=user_email)

    if request.method == 'POST':
        user.userName = request.POST.get('userName')
        if 'userImage' in request.FILES:
            user.userImage = request.FILES['userImage']
        user.save()
        request.session['user_name'] = user.userName
        request.session['user_image'] = user.userImage.url
        return redirect('chatbot')  # Or wherever you'd like to redirect

    return render(request, 'pages/edit_profile.html', {'user': user})

def base(request):

    return render(request, 'pages/base.html')

def user_list(request):
    query = request.GET.get('q')
    if query:
        users = Users.objects.filter(userName__icontains=query)
    else:
        users = Users.objects.all()
    return render(request, 'pages/user_list.html', {'users': users, 'query': query})


def user_add(request):  
    if request.method == "POST":  
        formtwo = UserForm(request.POST, request.FILES)  
        if formtwo.is_valid():  
            try:  
                user = formtwo.save()
                request.session['user_name'] = user.userName
                messages.success(request, '🎉 Account created successfully.')
                return redirect("user_list")  
            except:  
                messages.error(request, "❌ An unexpected error occurred.")
        else:
            messages.error(request, "⚠️ Form data is invalid. Please try again.")
    else:
        formtwo = UserForm()
    return render(request, 'pages/user_form.html', {'form': formtwo})

def user_edit(request, id):
    user = get_object_or_404(Users, pk=id)
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ User updated successfully.")
            return redirect('user_list')
        else:
            messages.error(request, "❌ Failed to update user.")
    else:
        form = UserForm(instance=user)
    return render(request, 'pages/user_form.html', {'form': form})

def user_delete(request, id):
    user = get_object_or_404(Users, pk=id)
    if request.method == "POST":
        user.delete()
        messages.success(request, "🗑️ User deleted successfully.")
        return redirect('pages/user_list')
    return render(request, 'user_confirm_delete.html', {'user': user})














def userAdd(request):  
    if request.method == "POST":  
        formtwo = UserForm(request.POST)  
        if formtwo.is_valid():  
            try:  
                user = formtwo.save()
                
                # ✅ Store username in session
                request.session['user_name'] = user.userName

                messages.success(request, 'Your account is created. Now you can login')
                return redirect("/webapp/dashboard")  
            except:  
                return render(request, "../error.html")
        else:
            formtwo = UserForm()
        messages.success(request, 'Try another username')
        return render(request, 'dashboard.html', {'form': formtwo})
     
def doLogout(request):
	key_session = list(request.session.keys())
	for key in key_session:
		del request.session[key]
	return render(request,'pages/home.html',{'success':'Logged out successfully'})

def showUserInfo(request):
	userX = Users.objects.all()
	return render(request,'pages/chatbot.html',{'chatkot':userX})

def getUser(request,userId):
	userX = Users.objects.get(userId=userId)
	return render(request,'pages/chatbot.html',{'f':userX})


#def updateUser(request,userId):
	#userX = Users.objects.get(userId=userId)
	#formtwo = UserForm(request.POST,request.FILES,instance=userX)
	#if formtwo.is_valid():
		#formtwo.save()
		#return redirect("/allcaffe")
	#return render(request,'updatefood.html',{'f':userX})			
  

#def updatePic(request):
    #user = userInfo.objects.get(userId=userId)
    #form = userForm(request.POST, request.FILES,instance=user)
    #if form.is_valid():
    #    form.save()
    #    return redirect("/webapp/sting")
   # return render(request, 'chatbot.html',{'u':user})

