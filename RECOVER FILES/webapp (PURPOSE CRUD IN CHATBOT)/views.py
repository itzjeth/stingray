from django.http import HttpResponse
from django.contrib import admin
from django.shortcuts import render,redirect, get_object_or_404
from django.db import connection, transaction
from webapp.forms import UserForm,ReviewForm,AdminForm #ChatPairForm
from webapp.models import  Users,Review,Admin #ChatPair
from chatterbot import ChatBot
from django.utils.safestring import mark_safe
from chatterbot.trainers import ListTrainer
from django.templatetags.static import static
from django.contrib import messages
"""{% load static %}"""
import datetime
cursor = connection.cursor()

# You should NOT reinitialize your ChatBot inside the view.
# Instead, initialize it once at the top level of your module (global scope)
def getResponse(request):
    user_message = request.GET.get('userMessage')
    
    if not user_message:
        return HttpResponse("No message received.", status=400)

    try:
        response = bot.get_response(user_message)
        return HttpResponse(mark_safe(str(response).replace('\n', '<br>')))
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

#from django.core.mail import send_mail
#from django.conf import settings



#def train_from_db():
    #chat_data = ChatPair.objects.all()
    #trainer = ListTrainer(bot)
    #for pair in chat_data:
        #trainer.train([pair.question, pair.answer])
     
def home_page(request,):
    
    #if request.method == 'POST':
        #name = request.POST['name']
        #email = request.POST['email']
       # message = request.POST['message']
       
       # send_mail(
           # name,#title
          #  message,#message
          #  'settings.EMAIL_HOST_USER', #sender if not available
          #  [email], #receiver email
          #  fail_silently=False)
    return render(request, 'pages/home.html')


def chatbot_page(request):
    
    return render(request, 'pages/chatbot.html')

def blog_page(request):
    return render(request, 'pages/blog.html')

def dashboard_page(request):
    return render(request, 'pages/dashboard.html')

def faq_page(request):
    return render(request, 'pages/FAQ.html')

def contact_page(request):
    return render(request, 'pages/contact.html')

def rizz(request):
    return render(request, 'pages/rizz.html')

def explorePage(request):
    return render(request, 'pages/explore.html')

def signupPage(request):
    return render(request, 'pages/signup.html')

def loginPage(request):
    return render(request, 'pages/login.html')

def chatbot_front(request):
    return render(request, 'pages/chatbot_front.html')




def chatbot_list(request):
    chatpairs = ChatPair.objects.all()
    return render(request, 'pages/chatbot_list.html', {'chatpairs': chatpairs})

# Add new
def chatbot_add(request):
    if request.method == 'POST':
        form = ChatPairForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Chat entry added.")
            return redirect('chatbot_list')
    else:
        form = ChatPairForm()
    return render(request, 'pages/chatbot_form.html', {'form': form})

# Edit
def chatbot_edit(request, pk):
    chatpair = get_object_or_404(ChatPair, pk=pk)
    if request.method == 'POST':
        form = ChatPairForm(request.POST, instance=chatpair)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Chat entry updated.")
            return redirect('chatbot_list')
    else:
        form = ChatPairForm(instance=chatpair)
    return render(request, 'pages/chatbot_form.html', {'form': form})

# Delete
def chatbot_delete(request, pk):
    chatpair = get_object_or_404(ChatPair, pk=pk)
    if request.method == 'POST':
        chatpair.delete()
        messages.success(request, "🗑️ Entry deleted.")
        return redirect('chatbot_list')
    return render(request, 'pages/chatbot_confirm_delete.html', {'chatpair': chatpair})

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
    reviews = Review.objects.all()
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

# views.py
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

















bot = ChatBot('chatbot', read_only=False,
            logic_adapters=[
                {

                    'import_path':'chatterbot.logic.BestMatch',
                    'maximun_similarity_threshold':0.95

                }
                ])
    
list_to_train = [

     " ",
     "Hello",
#What is CVSU
     #"What is CVSU",
     #"Cavite State University",

     #"what is CVSU",
     #"Cavite State University",

     "what is cvsu",
     """Cavite State University 
     """,

     #"What is cvsu",
     #"Cavite State University",
    
#How to enroll
    #"How to enroll",
    #"Old or New student",

    "how to enroll",
    "Old or New student",

    "enroll",
    "Old or New student",


    "how to enroll as old student",
    """ Certainly, If you are old student, first of all you need to get a CoG or (Certificate of Grades) at the registrar, after that the University will announce where/when the Enrollment will happen. <br><br>" 
    Step 1: Society Fee. It should be announce at your Department. <br><br>
    Step 2: Fill-out Curriculum Checklist. Curriculum checklist are available at your society. Must be placed at long brown folder. It should be labeled properly by their name, course and student number. <br><br>
    Step 3: Evaluation of grades & Advising of Subjects to enroll. Wait for an  Announcement at your department where it will be held. <br><br>
    Step 4: Issuance of Queuing Number (per program) <br><br>"
    Step 5: Encoding of Subjects. Your department will announce where it will be held. """,

    "how to enroll as new student",
     " Absolutely, If you are a New student you should follow these easy steps:<br><br>" 
    """  * First, you need Admission Form then Fill-out and Download the application Form. 
         <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Application Form</a>
         <br><br>
         * Secondly: Printing of Admission form: Download and print the accomplished the online application form and attached the 1x1 photo in the printed application with affixed signature.<br><br>
         * After you attached it, place it all at a short white folder with all the required requirements.<br><br>
         * Next, Bring 2 white short folder and 2 photocopies of all your original requirements.<br><br>
         * After that you should submit the requirements at the Guidance office of CvSU-Bacoor city.<br><br>
         * Lastly wait for further information for Examination Date: you will be given a permit and a schedule for the date of the Examination.""",

      "how to enroll as transferee",
      """ Ofcourse, Transferee (Those who started college level from other University/School) <br><br>"
    "  * Accomplished Application form for Admission  <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Click Here</a><br><br>
    "  * Photocopy of transcript of records/certificate of Grades <br><br>
    "Other requirements after Evaluation: <br><br>
    "  * Honorable Dismissal <br><br>
    "  * Certificate of Good Moral Character <br><br>
    "  * NBI or Police Clearance""",

#Old
    "Old",
    "If you are old student, first of all you need to get a CoG or (Certificate of Grades) at the registrar, after that the University will announce where/when the Enrollment will happen. <br><br>" 
    "Step 1: Society Fee. It should be announce at your Department. <br><br>"
    "Step 2: Fill-out Curriculum Checklist. Curriculum checklist are available at your society. Must be placed at long brown folder. It should be labeled properly by their name, course and student number. <br><br>"
    "Step 3: Evaluation of grades & Advising of Subjects to enroll. Wait for an  Announcement at your department where it will be held. <br><br>"
    "Step 4: Issuance of Queuing Number (per program) <br><br>"
    "Step 5: Encoding of Subjects. Your department will announce where it will be held. ",


    "OLD",
    "If you are old student, first of all you need to get a CoG or (Certificate of Grades) at the registrar, after that the University will announce where/when the Enrollment will happen. <br><br>" 
    "Step 1: Society Fee. It should be announce at your Department. <br><br>"
    "Step 2: Fill-out Curriculum Checklist. Curriculum checklist are available at your society. Must be placed at long brown folder. It should be labeled properly by their name, course and student number. <br><br>"
    "Step 3: Evaluation of grades & Advising of Subjects to enroll. Wait for an  Announcement at your department where it will be held. <br><br>"
    "Step 4: Issuance of Queuing Number (per program) <br><br>"
    "Step 5: Encoding of Subjects. Your department will announce where it will be held. ",

    "old",
    "If you are old student, first of all you need to get a CoG or (Certificate of Grades) at the registrar, after that the University will announce where/when the Enrollment will happen. <br><br>" 
    "Step 1: Society Fee. It should be announce at your Department. <br><br>"
    "Step 2: Fill-out Curriculum Checklist. Curriculum checklist are available at your society. Must be placed at long brown folder. It should be labeled properly by their name, course and student number. <br><br>"
    "Step 3: Evaluation of grades & Advising of Subjects to enroll. Wait for an  Announcement at your department where it will be held. <br><br>"
    "Step 4: Issuance of Queuing Number (per program) <br><br>"
    "Step 5: Encoding of Subjects. Your department will announce where it will be held. ",



#New 
    "New Student",
    "If you are a New student you should follow these easy steps:<br><br>" 
    """  * First, you need Admission Form then Fill-out and Download the application Form. 
         <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Admission Form</a>
         <br><br>
         * Secondly: Printing of Admission form: Download and print the accomplished the online application form and attached the 1x1 photo in the printed application with affixed signature.<br><br>
         * After you attached it, place it all at a short white folder with all the required requirements.<br><br>
         * Next, Bring 2 white short folder and 2 photocopies of all your original requirements.<br><br>
         * After that you should submit the requirements at the Guidance office of CvSU-Bacoor city.<br><br>
         * Lastly wait for further information for Examination Date: you will be given a permit and a schedule for the date of the Examination.""",

    "new",
     """  * First, you need Admission Form then Fill-out and Download the application Form. 
         <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Admission Form</a>
         <br><br>
         * Secondly: Printing of Admission form: Download and print the accomplished the online application form and attached the 1x1 photo in the printed application with affixed signature.<br><br>
         * After you attached it, place it all at a short white folder with all the required requirements.<br><br>
         * Next, Bring 2 white short folder and 2 photocopies of all your original requirements.<br><br>
         * After that you should submit the requirements at the Guidance office of CvSU-Bacoor city.<br><br>
         * Lastly wait for further information for Examination Date: you will be given a permit and a schedule for the date of the Examination.""",

    "NEW",
     """  * First, you need Admission Form then Fill-out and Download the application Form. 
         <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Admission Form</a>
         <br><br>
         * Secondly: Printing of Admission form: Download and print the accomplished the online application form and attached the 1x1 photo in the printed application with affixed signature.<br><br>
         * After you attached it, place it all at a short white folder with all the required requirements.<br><br>
         * Next, Bring 2 white short folder and 2 photocopies of all your original requirements.<br><br>
         * After that you should submit the requirements at the Guidance office of CvSU-Bacoor city.<br><br>
         * Lastly wait for further information for Examination Date: you will be given a permit and a schedule for the date of the Examination.""",


#New Student
    "What are the requirements for New students",
    "First year Applicants (Grade 12 Students) <br><br>"
    """  * Accomplished Application form for Admission <br><br>  <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Admission Form</a>""" 
    "  * Photocopy of Grade 11 card <br><br>"
    "  * Certificate from the principal or adviser indicating that the applicant is currently enrolled as grade 12 student with strand indicated <br><br>"
    "  ✓ The certificate must be originally signed. E-signature is NOT allowed",

    "requirements for New students",
     """  * Accomplished Application form for Admission <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Admission Form</a> <br><br>  """ 
    "  * Photocopy of Grade 11 card <br><br>"
    "  * Certificate from the principal or adviser indicating that the applicant is currently enrolled as grade 12 student with strand indicated <br><br>"
    "  ✓ The certificate must be originally signed. E-signature is NOT allowed",

    "requirements for new students",
     """  * Accomplished Application form for Admission <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Admission Form</a> <br><br>  """ 
    "  * Photocopy of Grade 11 card <br><br>"
    "  * Certificate from the principal or adviser indicating that the applicant is currently enrolled as grade 12 student with strand indicated <br><br>"
    "  ✓ The certificate must be originally signed. E-signature is NOT allowed",
    "requirements for new student",
     """  * Accomplished Application form for Admission <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Admission Form</a> <br><br>  """ 
    "  * Photocopy of Grade 11 card <br><br>"
    "  * Certificate from the principal or adviser indicating that the applicant is currently enrolled as grade 12 student with strand indicated <br><br>"
    "  ✓ The certificate must be originally signed. E-signature is NOT allowed",
    "requirement for new student",
     """  * Accomplished Application form for Admission <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Admission Form</a> <br><br>  """ 
    "  * Photocopy of Grade 11 card <br><br>"
    "  * Certificate from the principal or adviser indicating that the applicant is currently enrolled as grade 12 student with strand indicated <br><br>"
    "  ✓ The certificate must be originally signed. E-signature is NOT allowed",

    "for new student",
   """  * Accomplished Application form for Admission <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Admission Form</a> <br><br>  """ 
    "  * Photocopy of Grade 11 card <br><br>"
    "  * Certificate from the principal or adviser indicating that the applicant is currently enrolled as grade 12 student with strand indicated <br><br>"
    "  ✓ The certificate must be originally signed. E-signature is NOT allowed",



#SHS Graduate
    "What are the requirements for SHS Graduate",
    "First year Applicants (for SHS Graduate) <br><br>"
    """  * Accomplished Application form for Admission    <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Application Form</a><br><br>"""
    "  * Photocopy of completed grade 12 report card <br><br>"
    "  * Certificate of non-issuance of Form 137 for college admission",

    "requirements for SHS Graduate",
     "First year Applicants (for SHS Graduate) <br><br>"
    """  * Accomplished Application form for Admission    <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Application Form</a><br><br>"""
    "  * Photocopy of completed grade 12 report card <br><br>"
    "  * Certificate of non-issuance of Form 137 for college admission",

    "for SHS Graduate",
      "First year Applicants (for SHS Graduate) <br><br>"
    """  * Accomplished Application form for Admission    <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Application Form</a><br><br>"""
    "  * Photocopy of completed grade 12 report card <br><br>"
    "  * Certificate of non-issuance of Form 137 for college admission",

    "for shs graduate",
    "First year Applicants (for SHS Graduate) <br><br>"
    """  * Accomplished Application form for Admission    <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Application Form</a><br><br>"""
    "  * Photocopy of completed grade 12 report card <br><br>"
    "  * Certificate of non-issuance of Form 137 for college admission",

    "for senior highscholl graduate",
      "First year Applicants (for SHS Graduate) <br><br>"
    """  * Accomplished Application form for Admission    <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Application Form</a><br><br>"""
    "  * Photocopy of completed grade 12 report card <br><br>"
    "  * Certificate of non-issuance of Form 137 for college admission",

    "highschool graduate",
      "First year Applicants (for SHS Graduate) <br><br>"
    """  * Accomplished Application form for Admission    <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Application Form</a><br><br>"""
    "  * Photocopy of completed grade 12 report card <br><br>"
    "  * Certificate of non-issuance of Form 137 for college admission",

    "for highschool graduate",
      "First year Applicants (for SHS Graduate) <br><br>"
    """  * Accomplished Application form for Admission    <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Application Form</a><br><br>"""
    "  * Photocopy of completed grade 12 report card <br><br>"
    "  * Certificate of non-issuance of Form 137 for college admission",

    "highschool graduate",
      "First year Applicants (for SHS Graduate) <br><br>"
    """  * Accomplished Application form for Admission    <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Application Form</a><br><br>"""
    "  * Photocopy of completed grade 12 report card <br><br>"
    "  * Certificate of non-issuance of Form 137 for college admission",



#ALS Passer
    "What are the requirements for ALS Passer",
    "First year Applicants (ALS Passer) <br><br>"
    """  * Accomplished Application form for Admission    <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Application Form</a> <br><br>""" 
    "  * Photocopy of Certificate of Rating(COR) with eligibility to enroll in College",

    "requirements for ALS Passer",
    """  * Accomplished Application form for Admission    <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Application Form</a> <br><br>""" 
    "  * Photocopy of Certificate of Rating(COR) with eligibility to enroll in College",

    "requirements for als passer",
    "First year Applicants (ALS Passer) <br><br>"
    "  * Accomplished Application form for Admission <br><br>" 
    "  * Photocopy of Certificate of Rating(COR) with eligibility to enroll in College",

    "for als passer",
    "First year Applicants (ALS Passer) <br><br>"
    "  * Accomplished Application form for Admission <br><br>" 
    "  * Photocopy of Certificate of Rating(COR) with eligibility to enroll in College",

    "als passer",
    "First year Applicants (ALS Passer) <br><br>"
    "  * Accomplished Application form for Admission <br><br>" 
    "  * Photocopy of Certificate of Rating(COR) with eligibility to enroll in College",



#Transferee
    "What are the requirements for Transferee",
    "Transferee (Those who started college level from other University/School) <br><br>"
    "  * Accomplished Application form for Admission <br><br>"
    "  * Photocopy of transcript of records/certificate of Grades <br><br>"
    "Other requirements after Evaluation: <br><br>"
    "  * Honorable Dismissal <br><br>"
    "  * Certificate of Good Moral Character <br><br>"
    "  * NBI or Police Clearance",

    "requirements for Transferee",
    "Transferee (Those who started college level from other University/School) <br><br>"
    "  * Accomplished Application form for Admission <br><br>"
    "  * Photocopy of transcript of records/certificate of Grades <br><br>"
    "Other requirements after Evaluation: <br><br>"
    "  * Honorable Dismissal <br><br>"
    "  * Certificate of Good Moral Character <br><br>"
    "  * NBI or Police Clearance",

    "requirements for transferee",
    "Transferee (Those who started college level from other University/School) <br><br>"
    "  * Accomplished Application form for Admission <br><br>"
    "  * Photocopy of transcript of records/certificate of Grades <br><br>"
    "Other requirements after Evaluation: <br><br>"
    "  * Honorable Dismissal <br><br>"
    "  * Certificate of Good Moral Character <br><br>"
    "  * NBI or Police Clearance",

    "for transferee",
    "Transferee (Those who started college level from other University/School) <br><br>"
    "  * Accomplished Application form for Admission <br><br>"
    "  * Photocopy of transcript of records/certificate of Grades <br><br>"
    "Other requirements after Evaluation: <br><br>"
    "  * Honorable Dismissal <br><br>"
    "  * Certificate of Good Moral Character <br><br>"
    "  * NBI or Police Clearance",

    "transferee",
    "Transferee (Those who started college level from other University/School) <br><br>"
    "  * Accomplished Application form for Admission <br><br>"
    "  * Photocopy of transcript of records/certificate of Grades <br><br>"
    "Other requirements after Evaluation: <br><br>"
    "  * Honorable Dismissal <br><br>"
    "  * Certificate of Good Moral Character <br><br>"
    "  * NBI or Police Clearance",



#Second course applicants
    "What are the requirements for Second course Applicants",
    "Second course Applicants(Those who finished a two-year program or four-year degree program) <br><br>"
    "  * Accomplished Application form for Admission <br><br>"
    "  * Photocopy of transcript of records with graduation date <br><br>" 
    "    Other requirements from evaluation <br><br>"
    "  * Honorable Dismissal <br><br>"
    "  * Certificate of Good Moral Character  <br><br>"
    "  * NBI or Police Clearance",

    "requirements for Second course Applicants",
    "Second course Applicants(Those who finished a two-year program or four-year degree program) <br><br>"
    """  * Accomplished Application form for Admission    <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Application Form</a><br><br>"""
    "  * Photocopy of transcript of records with graduation date <br><br>" 
    "    Other requirements from evaluation <br><br>"
    "  * Honorable Dismissal <br><br>"
    "  * Certificate of Good Moral Character  <br><br>"
    "  * NBI or Police Clearance",

    "requirements for second course applicants",
   """  * Accomplished Application form for Admission    <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Application Form</a><br><br>"""
    "  * Photocopy of transcript of records with graduation date <br><br>" 
    "    Other requirements from evaluation <br><br>"
    "  * Honorable Dismissal <br><br>"
    "  * Certificate of Good Moral Character  <br><br>"
    "  * NBI or Police Clearance",

    "for Second course Applicants",
    "Second course Applicants(Those who finished a two-year program or four-year degree program) <br><br>"
    """  * Accomplished Application form for Admission    <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Application Form</a><br><br>"""
    "  * Photocopy of transcript of records with graduation date <br><br>" 
    "    Other requirements from evaluation <br><br>"
    "  * Honorable Dismissal <br><br>"
    "  * Certificate of Good Moral Character  <br><br>"
    "  * NBI or Police Clearance",

    "for second course Applicants",
    """  * Accomplished Application form for Admission    <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Application Form</a><br><br>"""
    "  * Photocopy of transcript of records with graduation date <br><br>" 
    "    Other requirements from evaluation <br><br>"
    "  * Honorable Dismissal <br><br>"
    "  * Certificate of Good Moral Character  <br><br>"
    "  * NBI or Police Clearance",

    "second course Applicants",
    """  * Accomplished Application form for Admission    <a href="https://drive.google.com/file/d/1zoG0QutodBOX_iegsrPdtaXlgBs8Gn0a/view?fbclid=IwAR0cxxbPFag9mCOKcdWDrqd4Og8ytmJL_WFJYA5M4l_guRogSN7Ds-GBgoo" alt="admission.pdf" style="cursor: pointer;">Application Form</a><br><br>"""
    "  * Photocopy of transcript of records with graduation date <br><br>" 
    "    Other requirements from evaluation <br><br>"
    "  * Honorable Dismissal <br><br>"
    "  * Certificate of Good Moral Character  <br><br>"
    "  * NBI or Police Clearance",
    


#Foreign Students
    "What are the requirements for foreign student",
    """If you are foreign student you should follow these steps:<br><br>
    
    * Submit an approved permit to study from concerned embassy<br><br>
    
    * Pay a non-refundable foreign student fee of $36 dollars(may be changed without prior notice)<br><br>
    
    * Submit a Certificate of English Profiency from the Department of Language and Humanities<br><br>
    
    * Police Clearance from country of origin"""



#Recommend me a course    
    "Can you recommend me a Course",
    "It depends, Please input your Senior hish school strand",

    "can you recommend me a Course",
    "It depends, Please input your Senior hish school strand",

     "recommend me a Course",
    "It depends, Please input your Senior hish school strand",

    "recommend me a course",
    "It depends, Please input your Senior hish school strand",

    "recommend me a course",
    "It depends, Please input your Senior hish school strand",
    


#TVL    
    "TVL (Technical Vocational Livelihood Strand)",
    "I recommend you choosing Bachelor Science in Information Technology or Computer Science",

    "tvl",
    "I recommend you choosing Bachelor Science in Information Technology or Computer Science",

    "Technical Vocational Livelihood Strand",
    "I recommend you choosing Bachelor Science in Information Technology or Computer Science",

    "technical vocational livelihood strand",
    "I recommend you choosing Bachelor Science in Information Technology or Computer Science",

    "techvoc",
    "I recommend you choosing Bachelor Science in Information Technology or Computer Science",

    "tech",
    "I recommend you choosing Bachelor Science in Information Technology or Computer Science",

    "Information technology",
    "I recommend you choosing Bachelor Science in Information Technology or Computer Science",

    "Computer science",
    "I recommend you choosing Bachelor Science in Information Technology or Computer Science",

    "ICT",
    "I recommend you choosing Bachelor Science in Information Technology or Computer Science",

#GAS    
    "GAS (General Academic Strand)",
    "Well GAS is pretty general course so almost all course suits to you, so if you are undecided i think you should focus in what field do you seee in the future",

    "GAS",
    "Well GAS is pretty general course so almost all course suits to you, so if you are undecided i think you should focus in what field do you seee in the future",

    "gas",
    "Well GAS is pretty general course so almost all course suits to you, so if you are undecided i think you should focus in what field do you seee in the future",

    "General Academic Strand",
    "Well GAS is pretty general course so almost all course suits to you, so if you are undecided i think you should focus in what field do you seee in the future",

    "general academic strand",
    "Well GAS is pretty general course so almost all course suits to you, so if you are undecided i think you should focus in what field do you seee in the future",
    

#HUMMS    
    "HUMMS (Humanities and Social Science)",
    "I recommend you choosing Bachelor Science in Secondary Education / Criminilogy / and Pyschology.",

    "humms",
    "I recommend you choosing Bachelor Science in Secondary Education / Criminilogy / and Pyschology.",

    "Humanities and Social Science",
    "I recommend you choosing Bachelor Science in Secondary Education / Criminilogy / and Pyschology.",

    "humanities and social science",
    "I recommend you choosing Bachelor Science in Secondary Education / Criminilogy / and Pyschology.",

    "hums",
    "I recommend you choosing Bachelor Science in Secondary Education / Criminilogy / and Pyschology.",




#CVSU Mission
    "What is cvsu mission",
    "Cavite State University shall provide excellent, equitable and relevant educational opportunities in the arts, sciences and technology through quality instruction and responsive research and development activities. It shall produce professional, skilled and morally upright individuals for global competitiveness.",
    
    "what is cvsu mission",
    "Cavite State University shall provide excellent, equitable and relevant educational opportunities in the arts, sciences and technology through quality instruction and responsive research and development activities. It shall produce professional, skilled and morally upright individuals for global competitiveness.",

    "what is CvSu mission",
    "Cavite State University shall provide excellent, equitable and relevant educational opportunities in the arts, sciences and technology through quality instruction and responsive research and development activities. It shall produce professional, skilled and morally upright individuals for global competitiveness.",

    "cvsu mission",
    "Cavite State University shall provide excellent, equitable and relevant educational opportunities in the arts, sciences and technology through quality instruction and responsive research and development activities. It shall produce professional, skilled and morally upright individuals for global competitiveness.",

    "Cvsu mission",
    "Cavite State University shall provide excellent, equitable and relevant educational opportunities in the arts, sciences and technology through quality instruction and responsive research and development activities. It shall produce professional, skilled and morally upright individuals for global competitiveness.",

    "Cvsu Mission",
    "Cavite State University shall provide excellent, equitable and relevant educational opportunities in the arts, sciences and technology through quality instruction and responsive research and development activities. It shall produce professional, skilled and morally upright individuals for global competitiveness.",




#CVSU Vision
    "What is cvsu vision",
    "The premier University in historic Cavite recognized for excellence in the development of globally competitive and morally upright individuals.",

    "what is cvsu vision",
    "The premier University in historic Cavite recognized for excellence in the development of globally competitive and morally upright individuals.",

    "cvsu vision",
    "The premier University in historic Cavite recognized for excellence in the development of globally competitive and morally upright individuals.",

    "Cvsu vision",
    "The premier University in historic Cavite recognized for excellence in the development of globally competitive and morally upright individuals.",

    "cvsu Vision",
    "The premier University in historic Cavite recognized for excellence in the development of globally competitive and morally upright individuals.",

    "Cvsu Vision",
    "The premier University in historic Cavite recognized for excellence in the development of globally competitive and morally upright individuals.",

    
#CVSU Mission and Vision

    "What is cvsu mission and vision",
    "Cavite State University shall provide excellent, equitable and relevant educational opportunities in the arts, sciences and technology through quality instruction and responsive research and development activities. It shall produce professional, skilled and morally upright individuals for global competitiveness.<br><br>"
    "The premier University in historic Cavite recognized for excellence in the development of globally competitive and morally upright individuals.",

    "what is cvsu mission and vision",
    "Cavite State University shall provide excellent, equitable and relevant educational opportunities in the arts, sciences and technology through quality instruction and responsive research and development activities. It shall produce professional, skilled and morally upright individuals for global competitiveness.<br><br>"
    "The premier University in historic Cavite recognized for excellence in the development of globally competitive and morally upright individuals.",

    "What is cvsu vision and mission",
    "Cavite State University shall provide excellent, equitable and relevant educational opportunities in the arts, sciences and technology through quality instruction and responsive research and development activities. It shall produce professional, skilled and morally upright individuals for global competitiveness.<br><br>"
    "The premier University in historic Cavite recognized for excellence in the development of globally competitive and morally upright individuals.",

    "what is cvsu vision and mission",
    "Cavite State University shall provide excellent, equitable and relevant educational opportunities in the arts, sciences and technology through quality instruction and responsive research and development activities. It shall produce professional, skilled and morally upright individuals for global competitiveness.<br><br>"
    "The premier University in historic Cavite recognized for excellence in the development of globally competitive and morally upright individuals.",

    "mission and vision",
    "Cavite State University shall provide excellent, equitable and relevant educational opportunities in the arts, sciences and technology through quality instruction and responsive research and development activities. It shall produce professional, skilled and morally upright individuals for global competitiveness.<br><br>"
    "The premier University in historic Cavite recognized for excellence in the development of globally competitive and morally upright individuals.",

    "vision and mission",
    "Cavite State University shall provide excellent, equitable and relevant educational opportunities in the arts, sciences and technology through quality instruction and responsive research and development activities. It shall produce professional, skilled and morally upright individuals for global competitiveness.<br><br>"
    "The premier University in historic Cavite recognized for excellence in the development of globally competitive and morally upright individuals.",




#CVSU Bacoor quality policy
    "what is cvsu bacoor quality policy",
    "We Commit to the highest standards of education, value our stakeholders, Strive for continual improvement of our products and services, and Uphold the University’s tenets of Truth, Excellence, and Service to produce globally competitive and morally upright individuals.",

    "cvsu bacoor quality policy",
    "We Commit to the highest standards of education, value our stakeholders, Strive for continual improvement of our products and services, and Uphold the University’s tenets of Truth, Excellence, and Service to produce globally competitive and morally upright individuals.",

    "bacoor quality policy",
    "We Commit to the highest standards of education, value our stakeholders, Strive for continual improvement of our products and services, and Uphold the University’s tenets of Truth, Excellence, and Service to produce globally competitive and morally upright individuals.",

    "what is cvsu quality policy",
    "We Commit to the highest standards of education, value our stakeholders, Strive for continual improvement of our products and services, and Uphold the University’s tenets of Truth, Excellence, and Service to produce globally competitive and morally upright individuals.",

    "quality policy",
    "We Commit to the highest standards of education, value our stakeholders, Strive for continual improvement of our products and services, and Uphold the University’s tenets of Truth, Excellence, and Service to produce globally competitive and morally upright individuals.",

    "What is cvsu bacoor quality policy",
    "We Commit to the highest standards of education, value our stakeholders, Strive for continual improvement of our products and services, and Uphold the University’s tenets of Truth, Excellence, and Service to produce globally competitive and morally upright individuals.",

    "Bacoor quality policy",
    "We Commit to the highest standards of education, value our stakeholders, Strive for continual improvement of our products and services, and Uphold the University’s tenets of Truth, Excellence, and Service to produce globally competitive and morally upright individuals.",




#Who is the current president
    #"Who is the current president of cvsu",
    #"Dr. Hernando D. Robles is the current president of Cavite State University (CvSU). <br>He became the university president in October 2016, after serving as the Campus Administrator of CvSU Naic",

    "who is the current president of cvsu",
    "Dr. Hernando D. Robles is the current president of Cavite State University (CvSU). <br>He became the university president in October 2016, after serving as the Campus Administrator of CvSU Naic",

    "who is the president of cvsu",
    "Dr. Hernando D. Robles is the current president of Cavite State University (CvSU). <br>He became the university president in October 2016, after serving as the Campus Administrator of CvSU Naic",

    "current president of cvsu",
    "Dr. Hernando D. Robles is the current president of Cavite State University (CvSU). <br>He became the university president in October 2016, after serving as the Campus Administrator of CvSU Naic",

    "president of cvsu",
    "Dr. Hernando D. Robles is the current president of Cavite State University (CvSU). <br>He became the university president in October 2016, after serving as the Campus Administrator of CvSU Naic",



 #CvSU - Bacoor Information
    "Who is the currently Campus Administrator",
    "As of February 2024. The current Campus Administrator is Prof. Menvyluz S. Macalalad",

    "who is the currently Campus Administrator",
    "As of February 2024. The current Campus Administrator is Prof. Menvyluz S. Macalalad",

    "who is the currently campus administrator",
    "As of February 2024. The current Campus Administrator is Prof. Menvyluz S. Macalalad",

    "Who is the currently campus administrator",
    "As of February 2024. The current Campus Administrator is Prof. Menvyluz S. Macalalad",

    "Who is the currently campus administrator",
    "As of February 2024. The current Campus Administrator is Prof. Menvyluz S. Macalalad",

    "currently campus administrator",
    "As of February 2024. The current Campus Administrator is Prof. Menvyluz S. Macalalad",

    "current campus administrator",
    "As of February 2024. The current Campus Administrator is Prof. Menvyluz S. Macalalad",

    "campus administrator",
    "As of February 2024. The current Campus Administrator is Prof. Menvyluz S. Macalalad",
    

    

#major bacoor offer
    "What majors does CvSU Bacoor offer",
    "CvSU Bacoor offers various majors including Computer Science, Information Technology, Business Administration, Education, Pychology, and Criminology",

    "what majors does cvsu bacoor offer",
    "CvSU Bacoor offers various majors including Computer Science, Information Technology, Business Administration, Education, Pychology, and Criminology",

    "cvsu Bacoor offer",
    "CvSU Bacoor offers various majors including Computer Science, Information Technology, Business Administration, Education, Pychology, and Criminology",

    "CVSU Bacoor offer",
    "CvSU Bacoor offers various majors including Computer Science, Information Technology, Business Administration, Education, Pychology, and Criminology",
    

#Who has authority to suspends classes
    "Who have authority to suspends classes",
    """The University President who has final authority to suspend classes throughout the University including all units or branches. 
    or he may suspend classes in specific units or campuses for specified periods of units.
    Suspension of classes does not mean that faculty and employee will not report for duty <br><br>
    
    With respect to typhoons, classes will be suspended upon advice of Philippine Atmospheric Geophysical and Astronomici Services Authority (PAG-ASA) whenever the typhoon is sufficient intensity to make it advisable to suspend classes the elementary grade and moreover when the approach of the University because of typhoon becomes more definitely pronounced as to required suspension of classes in the high school and collegiate level as well. Aside from such official announcements to be made classes may be considered automatically suspended in the elementary grades when reports throughout the mass medi confirm the raising of typhoon Signal No.2, the suspension apply furthermore to all high school and collegiate levels if typhos signal is raised to Typhoon Signal No. 3""",



















#What is program accreditation
    "What is program accreditation",
    "The university shall as much as possible, submit all programs for accreditation particularly by Accrediting Agency of Chartered Colleges and Universities in the Philippines (AACCUP) or any accrediting agency prescribed by CHED and the Philippine Association of State Universities and Colleges",



















#Shifting to Other Programs
    "shifting to other programs",
    """ Student who intend to shift to another University program must be accomplish a prescribed form for the purpose to be approved by the Dean of the College where they want to shift to, not later than ten (10) working days before the start of the regular registration period. A copy of the approved application for shifting should be forwarded by the Dean concerned to the University Registrar's Office 
      <a href="https://drive.google.com/file/d/1D8yZCXl3Xc7kCTGz61EjVRse_incTN96/" alt="admission.pdf" style="cursor: pointer;">Shfting Form</a> """


















#Cross Registration
    "what is cross registration"
    "Cross-registrants from other educational institution should have a written permission from their school registrar to be presented to the CvSU registrar. The permit shall state the subject(s) and the total number of units the student is allowed to cross-register and that the University shall be the venue for the course to be registered.",

















#Late registration
    "what happen in late registration",
    """The period for the late registration shall be seven school days after the regular registration schedule. No late registrar will be entertained after this period"""
















#Academic load
    "Academic load",
    "No student shall be alowed to take more than the maximum credit units per semester. A graduating student may be allowed to enroll more than the maximum allowable may be allowed to enroll more than the maximum allowable credit units not to exceed 26 units during the last two semesters of his course provided that he has a GPA of 2.50 or better in the previous two semesters as certified by the University Registrar. A graduating student petitioning for registrating up to maximum allowable academic load must secure a certification from the University Registrar that he is a graduating student.",
    













#Class Attendance

    "Is attendance required to pass",
    "Pupils/Students are required to attend their classes promptly and regularly. <br>"
    "If a university student is absent without excusable reason is 20 percent or more of the number of hours he shall be dropped from the roll."
    """If his performance is poor he shall be given a grade of "5.0" """,

    "attendance required to pass",
    "Pupils/Students are required to attend their classes promptly and regularly. <br>"
    "If a university student is absent without excusable reason is 20 percent or more of the number of hours he shall be dropped from the roll."
    """If his performance is poor he shall be given a grade of "5.0" """,

    "Attendance required to pass",
    "Pupils/Students are required to attend their classes promptly and regularly. <br>"
    "If a university student is absent without excusable reason is 20 percent or more of the number of hours he shall be dropped from the roll."

    "attendance required",
    "Pupils/Students are required to attend their classes promptly and regularly. <br>"
    "If a university student is absent without excusable reason is 20 percent or more of the number of hours he shall be dropped from the roll."
    """If his performance is poor he shall be given a grade of "5.0" """,
    













#What is the passing grade of CVSU   
    "What is the passing grade of cvsu bacoor",
    "The passing grade of 3.00 while 5.00 is the failing grade",

    "Passing grade of cvsu bacoor",
    "The passing grade of 3.00 while 5.00 is the failing grade",

    "Passing grade of cvsu bacoor",
    "The passing grade of 3.00 while 5.00 is the failing grade",

    "passing grade",
    "The passing grade of 3.00 while 5.00 is the failing grade",
  












#Too many absent
    "i have too many absent",
    """If a student has been absent in 20 percent of the time schedule devoted to the class without justifiable reasons, he/she are not excused and the student's performance is poor, he/she will receive a grade of "5.00". """,












#Changing
    "Changing of course",
    """ If you are changing course. Transfer to other sections mush be amid for valid reason only such as conflict in schedule. It shall be done for valid reason only, with the consent of the professor(s) recommended by the Adviser, and approved by the Dean of the GS-OSL
     <a href="https://drive.google.com/file/d/1kgzyZJcWFHykDv07CQg7-K7lJj0t7jgn" alt="admission.pdf" style="cursor: pointer;">Form</a>
    """,

#Adding
    "Adding of course",
    """ If you are adding course is only for those who finished a two-year program or four-year degree program, may add subject by filling a prescribed form for the purpose.  It shall be done for valid reason only, with the consent of the professor(s) recommended by the Adviser, and approved by the Dean of the GS-OSL
     <a href="https://drive.google.com/file/d/1kgzyZJcWFHykDv07CQg7-K7lJj0t7jgn" alt="admission.pdf" style="cursor: pointer;">Form</a>
    """,
    
#Dropping
    "Dropping of course",
    """ Dropping of course/subjects shall only be made for the valid reasons, only in such cases as the course is not needed, ill-advised, conflict in schedule, registered higher course without passing the prerequisite courses(s) and registered major course without passing the prerequisite course(s) and registered major course without passing all the required basic courses except in cases where the basic courses are offered in a semester consurrent with the major course <br><br>
     <a href="https://drive.google.com/file/d/1kgzyZJcWFHykDv07CQg7-K7lJj0t7jgn" alt="admission.pdf" style="cursor: pointer;">Form</a>
    Dropping of course(s) shall be made official by filling a prescribed form at the Office of the College Registrar
    """,











#Re-enrollment of subjects
    "what happen in re-enrollment of subjects",
    """ No student shall be allowed to repeat or re-enroll a subject for more than three (3)  times. <br><br>
    
    A student who fails a subject for the third time hsall be permanently disqualified from further registration in the University""",










#Prerequisite Subjects
    "what is prerequisite subjects",
    """ A student shall not be allowed to register an advanced subject without passing/satisfying the requirements of the prerequisite subject(s) specified in the curriculum. <br>
    Passing grades obtained in the advanced course without first satisfying the prerequisites shall be considered null and void by the University Registrar""",
    








#Leave of absence
    "What is leave of absence",
    """ A student who is granted leave of absence (LOA) within "75%" of the time devoted to a semester/term shall be given a corresponding grade by the instructor concerned for record purposes only but this will not be reflected in his Permanent Record.""",
       







#Honorable Dismissal
    "What is honorable dismissal",
    """ Horable dismissal shall be issued by the University Registrar to a student who stopped schooling in the University provided that he was not found guilty of misdemeanor defined under the University Students' Norm of Conduct. If a student left the University for reasons of misdemeanor and/or academic delinquency, no certification of honorable dismissal shall be issued.""",
      











#Grades and Grading System
"""What is grading system of cvsu bacoor""",
 """The University shall adopt the numerical grading system of "1.00" to "5.00" where "1.00" is the highest grade and "5.00" is a failing grade.
 The system of grading is as follows:<br><br>
 
 <table class="grade-table" style="width: 100%; border: 1px solid white; padding: 30px; color: ">
    <tr >
       <td style="padding: 15px;"> 1.00 </td>
       <td style="border-bottom: 1px solid var(--text-color);"> Excellent (Highest Grade) </td>
    </tr>
    <tr>
        <td>1.25</td>
    </tr>
    <tr>
       <td> 1.50 </td>
       <td style="border-bottom: 1px solid var(--text-color);"> Very Good </td>
    </tr>
    <tr>
        <td>1.75</td>
    </tr>
     <tr>
       <td> 2.00 </td>
       <td style="border-bottom: 1px solid var(--text-color);"> Good </td>
    </tr>
    <tr>
        <td>2.25</td>
    </tr>
     <tr>
       <td> 2.50 </td>
       <td style="border-bottom: 1px solid var(--text-color);"> Satisfactory </td>
    </tr>
        <td>2.75</td>
    </tr>
     <tr>
       <td> 3.00 </td>
       <td style="border-bottom: 1px solid var(--text-color);"> Passing Grade </td>
    </tr>
   <tr></tr>
   <tr></tr>
   <tr></tr>
   <tr></tr>
   <tr></tr>
   <tr></tr>
   <tr></tr>
   <tr></tr>
     <tr>
       <td> 4.00 </td>
       <td style="border-bottom: 1px solid var(--text-color);"> Conditional Grade has to be removed by taking a removal examination either to obtain a grade of "3.00" or slide to 5.00" </td>
    </tr>
    <tr></tr>
    <tr></tr>
    <tr></tr>
    <tr></tr>
    <tr></tr>
    <tr></tr>
    <tr></tr>
    <tr></tr>
     <tr>
       <td> INC </td>
       <td style="border-bottom: 1px solid var(--text-color);"> Grade of incomplete. The student is passing but has not completed other requirement of the course </td>
    </tr>
    <tr></tr>
    <tr></tr>
    <tr></tr>
    <tr></tr>
    <tr></tr>
    <tr></tr>
    <tr></tr>
    <tr></tr>
    <tr>
        <td> 5.00 </td>
        <td style="border-bottom: 1px solid var(--text-color);"> The student failed the course. The numberical grade of "5.00" must be written in red ink by the teacher </td>
     </tr>
    
    
    
    
    </table><br><br>
    
    Each College shall endeavor to formulate and adopt a uniform method or system of assigning grades to scores and the assignment of weights to different types of test, requirements, laboratory exercises, and the like. This should be forwarded to the Vice President for Academic Affairs for his review and corrections before final adoption of the College concerned.""",
      








    

 #Grade Requirements and Retention   
    "grade requirements and retention",
    """ In order to qualify for the general comprehensive examination, a student must obtain a GPA of 2.00 or better for all the courses taken. Courses listed under "others" shall be excluded from the computation but grades in these subjects must be passing.<br><br>

Failure to pass a subject twice shall disqualify the student from the graduate program.<br><br>

Similarly, a graduate student must maintain a GPA of 2.00 or better every term in order to qualify to continue with his program """,
   








    
#Course Number System
    "What is course number system",
    "In addition to the CHED the numbers of courses in revised or proposed program shout requirement conform to the course number system being adopted by the University",









#Process of Phase Out Program
    "process phase out program",
    """A phase-out program should be anticipated in the implementation of new or revised programs.<br><br>

        If the new program is designed to replace an existing curriculum, the implementation should start from the incoming freshmen only and the old curriculum should end with the graduation of the current students taking it.<br><br>

In the revised courses, the compulsory requirement for students for the introduced/revised courses should start only in the current year they are supposed to take course. In no case shall the introduced/revised courses be required as back subjects for students.
""",








#Schedule of Revision
    "Schedule of Revision of new course",
    "Unless the revision or introduction of new required course is a mandatory requirement by CHED, no revision on any curriculum of the University shall be made within five (5) years of its implementation.",








#What is Unit Load
    "what is unit load?",
    "A non-working student may enroll a maximum load of 12 credit units if classes are conducted during regular days. However, for Saturday/summer classes, a graduate student may enroll a maximum load of nine (9) units for non-laboratory subjects and six (6) units for subjects with laboratory. CvSU full-time faculty members and staff who are admitted in the GS-OLC shall be allowed to enroll a maximum of six (6) units per semester.",







#Advanced or Transfer Credits
    "Advanced or transfer credits",
    "Advanced or Transfer Credits. A student may apply to the GS-OLC for transfer credits of academic work done in another institution only upon the recommendation of the department where he is planning to specialize, subject to the following conditions.",







#Full time student
    "full-time student",
    "A full-time stident is one who is registered for formal academic credit units and who carries the full load for a given semester under the curriculum in which he is enrolled including graduating students who may carry less than the full load for purpose of completing the requirements of the current semester.",


#Part time student
    "part time student",
    "A part-time student is one who is registered for formal credits but who carries less than the full load for a given semester under the curriculum in which he is enrolled.",



#transfer students What
    "what are transfer student",
    "A transfer student is one who comes from another college/university where he started studying for a course and who is now registered in the University after fulfilling all requirements as transfer student. Transferees during the last semester of the last year of a given curriculum shall be discouraged.",


#Student assistant
    "student assistant",
    "A student assistant is one who is employed on a full- time basis at the University rendering service of at least 100 hours a month. A student assistant is advised to carry reduced load of at most 18 units academic load.",


#Foreign student
    "foreign student", 
    "Foreign student is a University student who is not a citizen of the Philippines. In case there are more than five (5) foreign students, an adviser shall be designated",








#table of grade of conversion
    "table of conversion",
    """ All units earned in other colleges or universities shall be evaluated on the basis of the following "table of conversion" <br><br>
    
    
    <table style="width: 100%; border: 1px solid var(--text-color);; padding: 30px;">
  <tr>
    <td style="padding: 15px; border-bottom: 1px solid var(--text-color);  padding: 5px;">Grade</td>
    <td style="padding: 15px; border-bottom: 1px solid var(--text-color);  padding: 5px;">Grade</td>
    <td style="padding: 15px; border-bottom: 1px solid var(--text-color); padding: 5px;">Equivalent</td>
  </tr>
    <tr >
       <td style="padding: 15px; border-bottom: 1px solid var(--text-color);"> 1.00 </td>
       <td style="border-bottom: 1px solid var(--text-color);"> 95%' </td>
       <td style="border-bottom: 1px solid var(--text-color);"> 1+ or A+' </td>
    </tr>
    <tr >
      <td style="padding: 15px; border-bottom: 1px solid var(--text-color);"> 1.25 </td>
      <td style="border-bottom: 1px solid var(--text-color);"> 93%' </td>
      <td style="border-bottom: 1px solid var(--text-color);"> 1 or A' </td>
   </tr>
   <tr >
    <td style="padding: 15px; border-bottom: 1px solid var(--text-color);"> 1.50 </td>
    <td style="border-bottom: 1px solid var(--text-color);"> 90%' </td>
    <td style="border-bottom: 1px solid var(--text-color);"> 1- or A-' </td>
 </tr>
 <tr >
  <td style="padding: 15px; border-bottom: 1px solid var(--text-color);"> 1.75 </td>
  <td style="border-bottom: 1px solid var(--text-color);"> 89%' </td>
  <td style="border-bottom: 1px solid var(--text-color);"> 2+ or B+' </td>
</tr>
<tr >
  <td style="padding: 15px; border-bottom: 1px solid var(--text-color);"> 2.00 </td>
  <td style="border-bottom: 1px solid var(--text-color);"> 85%' </td>
  <td style="border-bottom: 1px solid var(--text-color);"> 2 or B' </td>
</tr>
<tr >
  <td style="padding: 15px; border-bottom: 1px solid var(--text-color);"> 2.25 </td>
  <td style="border-bottom: 1px solid var(--text-color);"> 83%' </td>
  <td style="border-bottom: 1px solid var(--text-color);"> 2- or B-' </td>
</tr>
<tr >
  <td style="padding: 15px; border-bottom: 1px solid var(--text-color);"> 2.50 </td>
  <td style="border-bottom: 1px solid var(--text-color);"> 80%' </td>
  <td style="border-bottom: 1px solid var(--text-color);"> 3+ or C+' </td>
</tr>
<tr >
  <td style="padding: 15px; border-bottom: 1px solid var(--text-color);"> 2.75 </td>
  <td style="border-bottom: 1px solid var(--text-color);"> 78%' </td>
  <td style="border-bottom: 1px solid var(--text-color);"> 3 or C' </td>
</tr>
<tr >
  <td style="padding: 15px; border-bottom: 1px solid var(--text-color);"> 3.00 </td>
  <td style="border-bottom: 1px solid var(--text-color);"> 75%' </td>
  <td style="border-bottom: 1px solid var(--text-color);"> 3- or C-' </td>
</tr>
   
   
    
    
    
    </table>""",








#Granting of awards and honors
    "Granting of awards and honors",
    """For Non-Graduating Students (First to Third Year) <br><br>

Any member of the non-graduating classes shall be a candidate for honor if he/she meets the following requirements: <br><br>

1.1 Weighted average grade of not lower than "88%" in Science, Mathematics and Research and a GPA of not lower than "85%" during the academic year. <br><br>

1.2 No grade lower than "83%" in any subject in any grading period.<br><br>

2. Deserving students shall be awarded first, second, and third honors.<br><br>

3. Placement of candidates in the honor roll shall be based on the composite academic performance and co-curricular activities (Appendix A). The weight of academic performance and co-curricular activities are "85%" and "15%" respectively; and<br><br>

4. Candidates who qualify for honors shall receive medals and certificate of recognition.<br><br>

For Graduating Students.<br><br>

1. Members of the graduating class can be candidates for honors provided they have:<br><br>

1.1 Completed the curriculum in four years;<br><br>

1.2 A GPA of not lower than "85%" from first to fourth year;""",






#Amount Refundable
    "amount refundable",
"""The amount of refundable fees that can be availed by the students shall correspond to the total amount actually paid in cash during enrollment, limited to specific fees respectively""",










#Reason for refund
    "valid reason for refunds",
    """Reason for Refund<br><br>

    The reasons for which refund of school fees other than deposit are allowed shall include any of the following:<br><br>

    * Withdrawal of registration <br>
    * Dropping of enrolled subject  <br>
    * Scholarship  <br>
    * Overpayment  <br>


    For reason of "overpayment", refund of the excess amount shall be considered only if the total fees for the semester is paid in "cash" or "in full" during registration. If "in installment", the excess amount shall be credited to the students for the next payment period. <br><br>

    Withdrawal/refund of deposit shall be allowed only for reasons of graduation from the University or transfer to another school, as the case maybe. """,












#Period of Refund 
    "what is the period of refund",
    """Period of Refund. The period within which refund of school fees as those enumerated under 9.1.1, except "deposit", shall be on a semestral basis and to be made within three (3) weeks or 15 school days from the start of regular""",










#Partial Scholarship
    "partial scholarship",
    """Partial scholarship GPA of 88% to '88.99%' in all aca subjects at the end of the school year, and GPA of '88%' '10%' in Science, Mathematics and Scientific Research.<br><br>

    A scholar, whether full or partial must:<br><br>

    * Not have a grade lower than '85%' in any of the subjects <br><br>

    * Abide by the provisions of the University Norm of Condu for students. (The scholarship is forfeited if the student involved in any form of misdemeanor); and <br><br>

    * Submit notice or any change of legal guardian and residen while studying in the University SHS""",









#Scholarship Priviliges
    "What is scholarship priviliges?",
    """Scholarship Privileges. The scholar shall receive the privileges listed below. These privileges may be changed at any time as deemed necessary by the Board of Regents: <br><br>



<b>Full scholarship</b>

    * P500.00 monthly stipend <br><br>

    * P500.00 yearly book allowance  <br><br>

<b>Partial scholarship</b>

    * P300.00 monthly stipend <br><br>

    * P500.00 yearly book allowance <br><br>
""",













#Cat Image



    
    
    
  






#
#How much is society fee
#Too many absent
#

#Dress code
    "what is the dress code of cvsu bacoor",
    """All bonafide students of the University are required to wear the prescribed school uniform during scholl days except on designated "washday" or declared field days/special days. Laboratory/PE. uniforms shall be worn only during the prescribed time/period.""",    

    "the dress code of cvsu bacoor",
    """All bonafide students of the University are required to wear the prescribed school uniform during scholl days except on designated "washday" or declared field days/special days. Laboratory/PE. uniforms shall be worn only during the prescribed time/period.""",   

    "dress code of cvsu bacoor",
    """All bonafide students of the University are required to wear the prescribed school uniform during scholl days except on designated "washday" or declared field days/special days. Laboratory/PE. uniforms shall be worn only during the prescribed time/period.""",   

    "Dress code of cvsu bacoor",
    """All bonafide students of the University are required to wear the prescribed school uniform during scholl days except on designated "washday" or declared field days/special days. Laboratory/PE. uniforms shall be worn only during the prescribed time/period.""",   

    "What is the dress code of cvsu bacoor",
    """All bonafide students of the University are required to wear the prescribed school uniform during scholl days except on designated "washday" or declared field days/special days. Laboratory/PE. uniforms shall be worn only during the prescribed time/period.""",   








#When is wash day?
    "When is wash day",
    """The washday is usually on Wednesday and Saturday where you can wear anything other than uniform but due to extreme heat these season. The Office of the Vice President of Academic Affairs has released Office Memorandum No. 12, s.2024 regarding on the Non-Mandatory Wearing of Prescribed Uniform.<br><br>
     
    Whereareas, wearing of prescribed uniform for all levels will be NON-MANDATORY from April 4-30 2024.""",
    






 #when is uniform day?
    "When is uniform day",
    """Uniform day is usually Monday, Tuesday, Thursday, Friday and Sunday but due to extreme heat these season. The Office of the Vice President of Academic Affairs has released Office Memorandum No. 12, s.2024 regarding on the Non-Mandatory Wearing of Prescribed Uniform.<br><br>
     
    Whereareas, wearing of prescribed uniform for all levels will be NON-MANDATORY from April 4-30 2024. """,







#Display of ID

    "What is COR",
    "Certification of Registrations",

    "what is cor",
    "Certification of Registrations",
 






#COG
    "What is COG?",
    "Certificate of Grades",
     







#is COR required
    "Is COR required to bring",
    "Yes, COR is required of every student. The students shall no be allowed to enter and use any facilities without COR",

    "is COR required to bring",
    "Yes, COR is required of every student. The students shall no be allowed to enter and use any facilities without COR",

    "required to bring",
    "Yes, COR is required of every student. The students shall no be allowed to enter and use any facilities without COR",
    
 







#ID in cvsu bacoor
    "Is there an student ID in cvsu bacoor",
    "As of now, majority of the student have no student ID yet, but COR (Certification of Registration) is acceptable",

    "Is there an student ID in cvsu bacoor",
    "As of now, majority of the student have no student ID yet, but COR (Certification of Registration) is acceptable",

    "Is there an student ID in cvsu bacoor",
    "As of now, majority of the student have no student ID yet, but COR (Certification of Registration) is acceptable",

    "Is there an student ID in cvsu bacoor",
    "As of now, majority of the student have no student ID yet, but COR (Certification of Registration) is acceptable",
   
  






  
#Notice of Hearing

    "What is Notice of Hearing",
    "Notice of Hearing shall be served on all the parties. stating the date, time and place where the initial hearing of the case will be held.",

    "notice of hearing",
    "Notice of Hearing shall be served on all the parties. stating the date, time and place where the initial hearing of the case will be held.",
   


#
    
   
   
   
   
   

    
#Does CVSU have free tuition
    #"Does CVSU have free tuition",
    #"Thus, students who are currently enrolled in courses leading to a bachelor's degree are exempted from paying tuition and other school fees. <br>With this opportunity, seize and aspire to be what you want to be, anticipating the challenges and difficulties you will encounter along the way.",

    "Does cvsu have free tuition",
    "Thus, students who are currently enrolled in courses leading to a bachelor's degree are exempted from paying tuition and other school fees. <br>With this opportunity, seize and aspire to be what you want to be, anticipating the challenges and difficulties you will encounter along the way.",

    "does CVSU have free tuition",
    "Thus, students who are currently enrolled in courses leading to a bachelor's degree are exempted from paying tuition and other school fees. <br>With this opportunity, seize and aspire to be what you want to be, anticipating the challenges and difficulties you will encounter along the way.",

    "does cvsu have free tuition",
    "Thus, students who are currently enrolled in courses leading to a bachelor's degree are exempted from paying tuition and other school fees. <br>With this opportunity, seize and aspire to be what you want to be, anticipating the challenges and difficulties you will encounter along the way.",

    "have free tuition",
    "Thus, students who are currently enrolled in courses leading to a bachelor's degree are exempted from paying tuition and other school fees. <br>With this opportunity, seize and aspire to be what you want to be, anticipating the challenges and difficulties you will encounter along the way.",

#What is the meaning of the CvSU logo

    #"What is the meaning of the CvSU logo",
    #"The book and the torch at the center of the seal symbolizes knowledge and wisdom.",

    #"what is the meaning of the CvSU logo",
    #"The book and the torch at the center of the seal symbolizes knowledge and wisdom.",

    "what is the meaning of the cvsu logo",
    "The book and the torch at the center of the seal symbolizes knowledge and wisdom.",

    "meaning of the cvsu logo",
    "The book and the torch at the center of the seal symbolizes knowledge and wisdom.",

    "Meaning of the cvsu logo",
    "The book and the torch at the center of the seal symbolizes knowledge and wisdom.",

#What are the colors of CvSU

    #"What are the colors of CvSU",
    #"Green, gold, and white are the dominant colors of the logo denoting the three tenets of CvSU, namely: truth, excellence, and service.",

    #"what are the colors of CvSU",
    #"Green, gold, and white are the dominant colors of the logo denoting the three tenets of CvSU, namely: truth, excellence, and service.",

    "what are the colors of cvsu",
    "Green, gold, and white are the dominant colors of the logo denoting the three tenets of CvSU, namely: truth, excellence, and service.",

    "colors of cvsu",
    "Green, gold, and white are the dominant colors of the logo denoting the three tenets of CvSU, namely: truth, excellence, and service.",

    
   
   
#Parking advisory of cvsu parking
    "Can i park at the parking area of cvsu bacoor",
    """We strictly advise student NOT to park around the vicinity of CVSU - Bacoor City Campus and along Solidarity Route along Soldiers Hills IV(4) <br><br>

    The BTMO conducts continuous clearing operations to avoid blocking the driveways in the surrounding areas of Cavite State University - Bacoor City 𝗖𝗮𝗺𝗽𝘂𝘀. In connection with this, parking in the vicinity of the 𝗰𝗮𝗺𝗽𝘂𝘀 is strictly prohibited in pursuance of the policy.
    Students are encouraged to park in the right parking areas to avoid receiving parking tickets or violations.""",





#Pre-order a University Shirt
    "Where can i pre order a university tshirt for IT",
    """ Pre ordering for University Tshirt is now reopen for only 250 PESOS
     Payment can be done throught cash or walk-in transactions at the CSG Office<br><br>
    
     Note that you need to secure a copy of your receipt/payment that will serve as a proof during claiming """,


    "Where can i pre order a u-games jacket for IT",
    """ Pre ordering for U-Games jacket is now reopen for only 750 PESOS
     Payment can be done throught cash or walk-in transactions at the CSG Office<br><br>
    
     Note that you need to secure a copy of your receipt/payment that will serve as a proof during claiming. Strictly no payment, no pre-order!""",






#Following activities of DCS Week 2024
    "What are the following activities of DCS week?",
    """ The following are the activities of DCS Week 2024: 
    
       <table style="width: 100%;">
  <div style="padding: 15px; border: 1px solid black;">
            * Booth & Lounge<br>
            * Computer System Servicing<br>
            * Keyboard Master<br>
            * Mobile Legends: Bang Bang<br>
            * Call of Duty Mobile<br>
            * 8 Ball Pool<br>
            * Techno Quiz Bee<br>
            * Digital Arts: Canva Category<br>
            * Same Day Edit Challenge<br>
            * Students' Best Output Exhibit<br><br>

    Techtalks :
       <i> Exploring Drupal: An Open-Source Content Management Framework <br>
       by Mr. Judy Montesa<br><br>

       Pangarap...pangarap paano ba gumawa?<br>
       by Mr. John Verlin Santos<br><br>

       Tech Career Roadmap: Setting goals as IT and CS<br>
       by Ms. Geraldine Gutierrez
       </i>

    
  
  </div>
</table>""",



#OSAS GOALS

    "What is OSAS Goals?",
    " To look after the educational, vocational, as well as the personal development needs of the student; to assist them to maximize their potentials by helping them understand themselves and their environment and to enchance their pyschological growth towards socialized maturity",


#BSCS Class Advisory
    "Show me the BSCS class advisory",
    """Absolutely, Here is the BSCS Class Advisory: <br><br>
    <table style="border: 1px solid var(--text-color); width: 100%; padding: 10px;">
    <td>
      <b>For First Year: <br></b>
        1-1 Rodillar Gole Jr.   <br>
        1-2 Rachel Rodriguez    <br>
        1-3 Mikaela Arciaga     <br>
        1-4 Rufino Dela Cruz    <br>
        1-5 Mariel Castillo     <br><br>
  
        <b>For Second Year: <br></b>
        2-1 Joven Rios      <br>
        2-2 Aida Penson     <br>
        2-3 Ronald Rosete   <br>
        2-4 Clarissa Rostrollo   <br>
        2-5 Jerico Castillo     <br>
        2-6 James Manozo        <br>
        2-7 Eden Belgica    <br><br>
  
        <b>For Third Year: <br></b>
        3-1 Lorenzo Moreno Jr. <br>
        3-2 Nestor Pimentel     <br>
        3-3 Benedick Sarmiento   <br><br>
  
        <b>For Fourth Year: <br></b>
        4-1 Ely Rose Panganiban-Briones <br>
    </td>
  
    </table><br><br>
    Here is the All Class Advisory of BSCS.
    """,    
   



#BSIT Class Advisory
    "Show me the BS IT class advisory",
    """Sure, Here is the BSIT Class Advisory <br><br>

    <table style="border: 1px solid var(--text-color); width: 100%; padding: 10px;">
    <td>
      <b>For First Year: <br></b>
      1-1 Raymart Gianan  <br>
      1-2 Alvina Ramallosa  <br>
      1-3 Alvin Catalo  <br>
      1-4 Clarence Salvador  <br>
      1-5 Jovelyn Ocampo  <br>
      1-6 Salvacion Contante  <br> <br>

      <b>For Second Year: <br></b>
      2-1 Redem Decipulo  <br>
      2-2 Lawrence Jimenez  <br>
      2-3 Eduard Ello  <br>
      2-4 Roi Francisco  <br>
      2-5 Jay-Ar Racadio  <br>
      2-6 Ralph Christian Bolarda  <br>
      2-7 Jayson Nati  <br> <br>

      <b>For Third Year: <br></b>
      3-1 Edmund Martinez  <br>
      3-2 Jen Jerome Dela Pena  <br>
      3-3 Shane Carlo Biscocho  <br>
      3-4 Robina Mutia  <br>
      3-5 Marcon Offindo  <br>
      3-6 Alvin Celino  <br> <br>

      <b>For Fourth Year: <br></b>
      4-1 Ryan Paul Roy  <br>
      4-2 Nino Rodil  <br>
      4-3 Steffanie Bato <br></td>
      
      </table>
      <table>

      </table>
      <br><br>

    Here is the All Class Advisory of BSIT.
    """,

    "what is cvsu know for",
    """CvSU adheres to its commitment to Truth, Excellence and Service as it aims to be the "premier University in historic Cavite recognized for excellence in the development of globally competitive and morally upright individuals" """,

    "what is the main branch of cvsu",
    "Certainly, At present. CvSU has 11 campuses in the province. The main campus, approximately 70 hectares in land area and named as Don Severino delas Alas Campus, is in Indang, Cavite, Philippines",

    "what does cvsu stands for",
    "Certainly, The CVSU stands for Cavite State University or CvSU",

    "Where does "

#Testing Picture
   

    "generate me a tetrix game i can play",
    """<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Typical_Tetris_Game.svg/1200px-Typical_Tetris_Game.svg.png" alt="" width="350"> """,

    #add who is the last campus administrator
    
    #"How can I apply for scholarships at CvSU Bacoor",
    #"To apply for scholarships at CvSU Bacoor, you need to inquire at the Scholarship Office of the university. They usually have specific requirements and application procedures for different scholarship programs.",
    
   

    #"will we still pass an updated CTC",
    #" If it's during admission, it's possible, but when we come out with the list for NOA, the card must be updated (1st to 4th quarter) and good moral indicated that you are a graduate, and the updated Card and Good Moral Certified True Copy (CTC) will be attached.",

   # "not Certified True Copy (CTC), can I forward them",
   # " Upon admission, the requirements may not be CTC first, but when we issue a list for NOA, the CTC requirements must be passed",

    "What does NOA mean and What is NOA for",
    "NOA means Notice of Admission, The NOA is given to qualified students who can enroll.",

    "When is the deadline for submission of requirements",
    " We depend on each course or quota, we will announce in each program when we are close to admission.",

    "Can I take a course that is not aligned with STRAND",
    "The course to be taken from us must be aligned with the strand.",





    #"Can the requirements be incomplete Can i just follow",
    #"The requirements must be complete so that we can evaluate if you are qualified for the course you will take.",

    
]  
#corpus
#ChatterBotCorpusTrainer = ChatterBotCorpusTrainer(bot)
#corpusend
list_trainer = ListTrainer(bot)
list_trainer.train(list_to_train)
#corpus
#ChatterBotCorpusTrainer.train('chatterbot.corpus.english')
#corpusend