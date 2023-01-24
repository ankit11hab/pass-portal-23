from django.shortcuts import render, redirect,HttpResponse
from django.http import JsonResponse
import qrcode
import string
import random
import tempfile
from django.core.mail import EmailMessage
from django.core.mail import send_mail
import random
from .encrypt_decrypt import encrypt, decrypt
from django.conf import settings
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import base64
import json


config = {
    'apiKey': os.environ.get('API_KEY'),
    'authDomain': "pass-portal-a05c7.firebaseapp.com",
    'databaseURL': "https://pass-portal-a05c7-default-rtdb.firebaseio.com/",
    'projectId': "pass-portal-a05c7",
    'storageBucket': "pass-portal-a05c7.appspot.com",
    'messagingSenderId': "160016579583",
    'appId': "1:160016579583:web:e04e2383bfd944f4aa05ca",
}


# firebase=pyrebase.initialize_app(config)
# authe = firebase.auth()
cred = credentials.Certificate('main/serviceAccountKey.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# add this section to payment success and send qr for leader and members

def comingsoon(request):
    return render(request,'main/comingsoon.html')

def home(request):
    return render(request, 'main/home.html')


def otp(request):
    return render(request, "main/otp.html")


@csrf_exempt
def send_otp(request):
    try:
        email = json.loads(request.body)['email']
        request.session['LeaderEmail'] = email
        subject = 'Your email verification email'
        otp = random.randint(1000, 9999)
        message = 'Your otp is ' + str(otp)
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [email])
        request.session['otp'] = otp
    except Exception as e:
        print(e)
    return JsonResponse({"otp": "otp"})
    # return redirect('verify')


def verify(request):
    return render(request, 'main/verify.html')


def verify_otp(request):
    otp1 = request.POST.get('otp1')
    otp = request.session.get('otp')

    OTP = int(otp1)
    print(OTP)
    if OTP == otp:
        return redirect('register')
    return render(request, 'main/verify.html')


def register(request):
    email = request.session.get('LeaderEmail')
    return render(request, 'main/register.html', {'email': email})


def register2(request):
    email = request.session.get('LeaderEmail')
    return render(request, 'main/register2.html', {'email': email})


def SaveData(request):
    if request.method == 'POST':
        key = "Jkdh9rs6x1mSKH2lDFZ6z6057x4p8CL7"
        iv = "adjfytryd5g87hgh"
        id = ''.join(random.choices(string.ascii_uppercase +
                                    string.digits, k=8))
        amount = 1
        fee_id = "M1006"
        print(id)
        paases_type = {
            'general': 0,
            'premium': 0,
            'exclusive': 0,
            'id': id,
            'amount': 0,
        }
        LeaderFirstName = request.POST.get('LeaderFirstName')
        LeaderLastName = request.POST.get('LeaderLastName')
        LeaderContact_no = request.POST.get('LeaderContact_no')
        # LeaderEmail = request.POST.get('LeaderEmail')
        LeaderEmail =         request.session['LeaderEmail']
        print(LeaderEmail)
        LeaderPassType = request.POST.get('LeaderPassType')
        LeaderIDType = request.POST.get('LeaderIDtype')
        LeaderIDNumber = request.POST.get('LeaderIDnumber')
        LeaderAge = request.POST.get('LeaderAge')
        LeaderGender = request.POST.get('LeaderGender')
        member_first_names = request.POST.getlist('first_name')
        member_last_names = request.POST.getlist('last_name')
        member_contacts = request.POST.getlist('contact_no')
        member_passtype = request.POST.getlist('pass_type')
        member_idtype = request.POST.getlist('IDtype')
        member_idnumber = request.POST.getlist('IDnumber')
        member_age = request.POST.getlist('age')
        member_gender = request.POST.getlist('gender')
        member_email = request.POST.getlist('email')

        if (LeaderPassType == 'general'):
            paases_type['general'] = paases_type['general']+1
        elif (LeaderPassType == 'premium'):
            paases_type['premium'] = paases_type['premium']+1
        elif (LeaderPassType == 'exclusive'):
            paases_type['exclusive'] = paases_type['exclusive']+1

        count = 1
        for i in member_first_names:
            count = count+1
        request.session['count'] = count
        members = []

        for fname, lname, contact, pass_type, idtype, idnumber, gender, age, email, in zip(member_first_names, member_last_names, member_contacts, member_passtype, member_idtype, member_idnumber, member_gender, member_age, member_email):
            member = {
                "name": fname+' ' + lname,
                "contact": contact,
                "pass_type": pass_type,
                "id_type": idtype,
                "id_number": idnumber,
                "age": age,
                "gender": gender,
                'email': email,
            }
            members.append(member)
            if (pass_type == 'general'):
                paases_type['general'] = paases_type['general']+1
            elif (pass_type == 'premium'):
                paases_type['premium'] = paases_type['premium']+1
            elif (pass_type == 'exclusive'):
                paases_type['exclusive'] = paases_type['exclusive']+1
        Ldata = {
            "LName": LeaderFirstName+' ' + LeaderLastName,
            "LContact": LeaderContact_no,
            "LEmail": LeaderEmail,
            "LPassType": LeaderPassType,
            "LIDType": LeaderIDType,
            "LIDNumber": LeaderIDNumber,
            "LAge": LeaderAge,
            "LGender": LeaderGender,
            "members": members
        }

        doc_ref = db.collection('users').document(id)
        doc_ref.set(Ldata)
        amount = paases_type['general']*500 + \
            (paases_type['premium']+paases_type['premium'])*750
        amount = 1
        print(amount)
        paases_type['amount'] = amount
        amount=1
        data = id+"|"+fee_id+"|"+str(amount)
        encryptedData = encrypt(key, data, iv)
        fstring = f'{id}|{paases_type["general"]}|{paases_type["exclusive"]}|{paases_type["premium"]}|{paases_type["amount"]}'
        print(fstring)
        messages.info(request,  encryptedData)
        messages.error(request, fstring)
        print(paases_type)

    return redirect('confirm')


def confirm(request):
    return render(request, 'main/confirm_payment.html')

def send_verify_otp(email,id):
    try:
        subject = 'Your email verification email'
        otp = random.randint(1000, 9999)
        message = 'Your otp is ' + str(otp)
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [email])
        doc_ref_otp=db.collection('manage_booking_otps').document(id)
        doc_ref_otp.set({'id':id,'email':email,'otp':otp})
    except Exception as e:
        print(e)
    return JsonResponse({"otp": "otp"})


@csrf_exempt
def verifiy_otp(request):
    if request.method=='POST':
        otp = request.POST['otp']
        email = request.POST['email']
        id = request.POST['id']
        print(otp)
        otp__db=db.collection('manage_booking_otps').document(id).get().to_dict()
        otp_from_db=otp__db['otp']
        print(otp_from_db)
        if(str(otp)==str(otp_from_db)):
            doc__ref=db.collection('users').where('verID','==',id).stream()
            print(doc__ref)
            context=[]
            for doc in doc__ref:
                data_ref=doc.to_dict()            
                LAge=data_ref['LAge']
                print(LAge)
                LEmail=data_ref['LEmail']
                LGender=data_ref['LGender']
                LIDType=data_ref['LIDType']
                LPassType=data_ref['LPassType']
                LName=data_ref['LName']
                LIDNumber=data_ref['LIDNumber']
            # LEmail,LGender,LIDNumber,LIDType,LName,LPassType,members
                context.append({'LAge':LAge,
                'LEmail':LEmail,
                'LGender':LGender,
                'LIDType':LIDType,
                'LPassType':LPassType,
                'LName':LName,
                'LIDNumber':LIDNumber})
                print(context[0])
                # members=doc.collection('members').document().get()
                members=doc.getData('members')
                print(members) 
                for memb in members:
                    memb_dict=memb.to_dict()
                    age=memb_dict['age']
                    email=memb_dict['email']
                    contact=memb_dict['contact']
                    gender=memb_dict['gender']
                    idtype=memb_dict['id_type']
                    pass_type=memb_dict['pass_type']
                    name=memb_dict['name']
                    idnumber=memb_dict['id_number']

                    context+={
                    "name": name,
                    "contact": contact,
                    "pass_type": pass_type,
                    "id_type": idtype,
                    "id_number": idnumber,
                    "age": age,
                    "gender": gender,
                    'email': email,
                }
            return render(request,'main/managebooking.html',context)
        return render(request,'main/verify_otp_manage_booking.html')

# @csrf_exempt 
def manangebooking(request):
    send_verify_otp('akshat.akshat@iitg.ac.in','4VY5M')
    print('sent')
    # data=json.loads(request.body);
    # data=request.POST
    # id=data['id']
    # email=data['email']
    # print(id+' '+email)
    # doc_ref=db.collection('verified_users').document(id).get().to_dict()
    # print(doc_ref)
    # if(doc_ref['email']==email):
        # send_verify_otp(email,id)
        # return HttpResponse('otp sent!')
    return HttpResponse('mail not found')
