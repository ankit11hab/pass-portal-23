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
import os

config = {
  'apiKey': "AIzaSyC8N2qP1oHpViVAV-TADSGvM5tRrawo0F8",
  'authDomain': "passportal-b43c7.firebaseapp.com",
  'databaseURL':"https://passportal-b43c7-default-rtdb.firebaseio.com/",
  'projectId': "passportal-b43c7",
  'storageBucket': "passportal-b43c7.appspot.com",
  'messagingSenderId': "248589796957",
  'appId': "1:248589796957:web:cdeb2232356200ead66fb4",
  'measurementId': "G-X8ZLQS5E75",
  "serviceAccount": "main/serviceAccountKey.json"
}

firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
cred = credentials.Certificate('main/serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# -----------------------------code for qr code----------------------
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

# -----------------end---------------------------------

# -------------------------Code for registration-----------------------------
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

    # ---------------------------end------------------------