
from django.shortcuts import render,redirect,HttpResponse
import qrcode
import tempfile
from django.core.mail import EmailMessage
from django.core.mail import send_mail
import random
from django.conf import settings
import pyrebase
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

config = {
  'apiKey': "AIzaSyCkFXpXE7teeesfREQtEiBN48LKnLYTqp0",
  'authDomain': "pass-portal-c7ebd.firebaseapp.com",
  'databaseURL':"https://pass-portal-c7ebd-default-rtdb.firebaseio.com/",
  'projectId': "pass-portal-c7ebd",
  'storageBucket': "pass-portal-c7ebd.appspot.com",
  'messagingSenderId': "780759810916",  
  'appId': "1:780759810916:web:e59f55cd9b200062a3b071",
  'measurementId': "G-PNVV3374ZZ",
    "serviceAccount": "main/serviceAccountKey.json"
}

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
cred = credentials.Certificate('main/serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def login(request):
    return render(request,'main/login.html')



def generate_qr_code(request):
    email=request.session.get('LeaderEmail')
    count=request.session.get('count')
    img = qrcode.make({'email':email,'count':count})
    from_email = settings.EMAIL_HOST_USER

    with tempfile.TemporaryFile() as fp:
        img.save(fp)
        
      
        fp.seek(0)
        
        
        message = EmailMessage(
            'QR code',
            'Here is the QR code you requested',
            from_email,
            [email],    
        )
        
       
        message.attach('qr_code.png', fp.read(), 'image/png')
        
        
        message.send()
    
    return HttpResponse('QR code email sent!')

def otpPage(request):
    return render(request,'main/otp.html')

def postsignIn(request):
    email=request.POST.get('email')
    pasw=request.POST.get('pass')
    request.session['execEmail']=email
    
    try:
        user=authe.sign_in_with_email_and_password(email,pasw)
    except:
        message="Invalid Credentials!!Please ChecK your Data"
        return render(request,"main/login.html",{"message":message})
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request,"main/otp.html",{"email":email})
  

def logout(request):
    try:
        del request.session['uid']
    except:
        pass
    return render(request,"main/login.html")

# def Register(request):
    
#     return render(request,'main/register.html')

def otp(request):
  try:
    email=request.POST.get('email')
    request.session['LeaderEmail']=email
    subject = 'Your email verification email'
    otp = random.randint(1000, 9999)
    message = 'Your otp is '+ str(otp)
    from_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [email])
  except Exception as e:
            print(e)
  request.session['otp'] = otp
  return redirect('/postsignIn/verify/')

def verify(request):
   return render(request,'main/verify.html')

def verify_otp(request):
        otp1 = request.POST.get('otp1')
        otp = request.session.get('otp')
       
        OTP = int(otp1)
        print(OTP)
        if OTP == otp:
            return redirect('/postsignIn/register/')
        else:
            return redirect('/postsignIn/verify/')

def register(request):
    email=request.session.get('LeaderEmail')
    return render(request,'main/register.html',{'email':email})

def SaveData(request):
    execEmail =request.session['execEmail']
    LeaderName=request.POST.get('LeaderName')
    LeaderContact_no=request.POST.get('LeaderContact_no')
    LeaderEmail=request.POST.get('LeaderEmail')
    LeaderPassType=request.POST.get('LeaderPassType')
    member_names = request.POST.getlist('name')
    member_contacts=request.POST.getlist('contact_no')
    count=1
    for i in member_names:
        count=count+1
    request.session['count']=count
    members = []
    for name, contact in zip(member_names, member_contacts):
        member = {
            "name": name,
            "contact": contact,
        }
        members.append(member)
    
    data = {
        "LName": LeaderName,
        "LContact": LeaderContact_no,
        "LEmail": LeaderEmail,
        "LPassType":LeaderPassType,
        "ExecEmail":execEmail,
        "members": members
    }
    
    doc_ref = db.collection('users').document()
    doc_ref.set(data)

    generate_qr_code(request)
    return redirect('/postsignIn/otppage/')

