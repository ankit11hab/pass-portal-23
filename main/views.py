
from django.shortcuts import render, redirect, HttpResponse
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


def generate_qr_code(request, members, leader):
    email = request.session.get('LeaderEmail')
    count = request.session.get('count')
    from_email = settings.EMAIL_HOST_USER
    message = EmailMessage(
        'QR code',
        'Here is the QR code you requested',
        from_email,
        [email],
    )
    img = qrcode.make(
        {'name': leader['LName'], 'pass_type': leader['LPassType']})
    with tempfile.TemporaryFile() as fp:
        img.save(fp)
        fp.seek(0)
        message.attach('qr_code.png', fp.read(), 'image/png')

    for member in members:
        img = qrcode.make(
            {'name': member['name'], 'pass_type': member['pass_type']})
        with tempfile.TemporaryFile() as fp:
            img.save(fp)
            fp.seek(0)
            message.attach('qr_code.png', fp.read(), 'image/png')

    message.send()

    return HttpResponse('QR code email sent!')


def otp(request):
    return render(request, "main/otp.html")


def send_otp(request):
    try:
        email = request.POST.get('email')
        request.session['LeaderEmail'] = email
        subject = 'Your email verification email'
        otp = random.randint(1000, 9999)
        message = 'Your otp is ' + str(otp)
        from_email = settings.EMAIL_HOST_USER
        send_mail(subject, message, from_email, [email])
    except Exception as e:
        print(e)
    request.session['otp'] = otp
    return redirect('verify')


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


def SaveData(request):
    if request.method == 'POST':
        key = "Jkdh9rs6x1mSKH2lDFZ6z6057x4p8CL7"
        iv = "adjfytryd5g87hgh"
        id = ''.join(random.choices(string.ascii_uppercase +
                                    string.digits, k=11))
        amount = 1
        fee_id = "M1006"
        print(id)
        data = id+"|"+fee_id+"|"+str(amount)
        encryptedData = encrypt(key, data, iv)
        print(encryptedData)
        # print(encryptedData)
        LeaderName = request.POST.get('LeaderName')
        LeaderContact_no = request.POST.get('LeaderContact_no')
        LeaderEmail = request.POST.get('LeaderEmail')
        LeaderPassType = request.POST.get('LeaderPassType')
        member_names = request.POST.getlist('name')
        member_contacts = request.POST.getlist('contact_no')
        member_passtype = request.POST.getlist('pass_type')

        count = 1
        for i in member_names:
            count = count+1
        request.session['count'] = count
        members = []
        for name, contact, pass_type in zip(member_names, member_contacts, member_passtype):
            member = {
                "name": name,
                "contact": contact,
                "pass_type": pass_type,
            }
            members.append(member)
        data = {
            "LName": LeaderName,
            "LContact": LeaderContact_no,
            "LEmail": LeaderEmail,
            "LPassType": LeaderPassType,
            "members": members
        }

        doc_ref = db.collection('users').document(id)
        doc_ref.set(data)

        generate_qr_code(request, members, data)
        messages.info(request, {"encryptedData": encryptedData, "id": id})

    return redirect('confirm')


def confirm(request):
    return render(request, 'main/confirm.html')
