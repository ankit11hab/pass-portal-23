from django.shortcuts import render, redirect, HttpResponse
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
from django.core.mail import EmailMultiAlternatives

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
    return render(request, 'main/comingsoon.html')


def home(request):
    return render(request, 'main/home.html')


def otp(request):
    context = {
        'message': "Please Enter E-mail First",
    }
    return render(request, "main/otp.html", context)


@csrf_exempt
def encrypt_data(data, key):
    """Encrypt the data using XOR encryption and a given key"""
    encrypted_data = bytearray(len(data))
    key_len = len(key)
    for i in range(len(data)):
        encrypted_data[i] = data[i] ^ key[i % key_len]
    return bytes(encrypted_data)


@csrf_exempt
def send_otp(request):
    try:
        email = json.loads(request.body)['email']
        request.session['LeaderEmail'] = email
        subject = 'Your email verification email'
        otp = random.randint(1000, 9999)
        # print(otp)
        message = 'Your otp is ' + str(otp)
        from_email = settings.EMAIL_HOST_USER
        # send_mail(subject, message, from_email, [email])

        html_content = f'''<div>Dear User,<br/><br/>
            The OTP for email verification is: <b>{otp}</b><br/><br/>
            With best wishes,<br/>
            Team Alcheringa
        </div>'''
        msg = EmailMultiAlternatives(
            subject, html_content, from_email, [email])
        msg.content_subtype = "html"
        msg.send()
        # request.session['otp'] = otp

        doc_ref = db.collection('all_otps').document()

        doc_ref.set({
            'id': doc_ref.id,
            'email': email,
            'otp': otp,
        })
        request.session['OtpId'] = doc_ref.id
        print(doc_ref)

    except Exception as e:
        print(e)
    return JsonResponse({"otp": "otp"})
    # return redirect('verify')


def verify(request):
    return render(request, 'main/verify.html')


def verify_otp(request):
    otp1 = request.POST.get('otp1')
    # otp = request.session.get('otp')
    otpID = request.session.get('OtpId')
    snapshots = db.collection('all_otps').where('id', '==', otpID).stream()
    users = []
    otp = 0
    for user in snapshots:
        formattedData = user.to_dict()
        print(formattedData)
        otp = formattedData['otp']
        users.append(user.reference)

    # otp=int(user['otp'])

    OTP = int(otp1)
    print(OTP, otp)
    if OTP == otp:
        return redirect('register')

    context = {
        'message': "Incorrect OTP",
    }
    return render(request, 'main/otp.html', context)


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
                                    string.digits, k=5))
        amount = 1
        fee_id = "M1006"
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
        LeaderEmail = request.session['LeaderEmail']
        print(LeaderEmail)
        LeaderPassType = "exclusive"
        # LeaderPassType = request.POST.get('LeaderPassType')
        LeaderIDType = request.POST.get('LeaderIDtype')
        LeaderIDNumber = request.POST.get('LeaderIDnumber')
        LeaderAge = request.POST.get('LeaderAge')
        LeaderGender = request.POST.get('LeaderGender')
        referralId = request.POST.get('ref_id')
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
        Ldata = {
            "LName": LeaderFirstName+' ' + LeaderLastName,
            "LContact": LeaderContact_no,
            "LEmail": LeaderEmail,
            "LPassType": LeaderPassType,
            "LIDType": LeaderIDType,
            "LIDNumber": LeaderIDNumber,
            "LAge": LeaderAge,
            "LGender": LeaderGender,
            # "members": members
        }

        doc_ref = db.collection('users').document(id)
        doc_ref.set(Ldata)
        count = 1
        for i in member_first_names:
            count = count+1
        request.session['count'] = count
        members = []

        # is_ref = False
        # referral_Id = {'ReferralID': referralId}
        # referral = db.collection('referral_ids').where(
        #     'ID', '==', referralId).get()
        # for ref in referral:
        #     if ref.exists:
        #         doc_ref.update(referral_Id)
        #         is_ref = True
        #     else:
        #         print('The Entered Referral ID was Incorrect')

        for fname, lname, contact, pass_type, idtype, idnumber, gender, age, email, in zip(member_first_names, member_last_names, member_contacts, member_passtype, member_idtype, member_idnumber, member_gender, member_age, member_email):
            member = {
                "name": fname+' ' + lname,
                "contact": contact,
                "pass_type": "exclusive",
                "id_type": idtype,
                "id_number": idnumber,
                "age": age,
                "gender": gender,
                'email': email,
            }
            doc_ref.collection('members').document().set(member)
            members.append(member)
            if (pass_type == 'general'):
                paases_type['general'] = paases_type['general']+1
            elif (pass_type == 'premium'):
                paases_type['premium'] = paases_type['premium']+1
            elif (pass_type == 'exclusive'):
                paases_type['exclusive'] = paases_type['exclusive']+1

        # amount = paases_type['general']*500 + \
        #     (paases_type['exclusive']+paases_type['premium'])*750
        amount=paases_type['exclusive']

        if paases_type['general']+paases_type['premium']+paases_type['exclusive'] != len(members)+1:
            messages.warning(request, 'Some Error Occured.Please Try Again')
            return redirect('register')
        # amount=paases_type['exclusive']
        # amount = 750
        if not amount:
            amount = 750
        # amount=1

# -----------------------code for referral id-----------------------------
        referrals = ["nkGLH6MYJr", "ITBCLeZ2mH", "ZnZNspvU39"]
        if (referralId in referrals):
            if (paases_type['general']+paases_type['exclusive']+paases_type['premium'] <= 10):
                amount -= 750
            elif (paases_type['general']+paases_type['exclusive']+paases_type['premium'] <= 5):
                amount -= 250

        paases_type['amount'] = amount
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


def send_verify_otp(email, id):
    try:
        subject = 'Your email verification email'
        otp = random.randint(1000, 9999)
        message = 'Your otp is ' + str(otp)
        from_email = settings.EMAIL_HOST_USER
        # send_mail(subject, message, from_email, [email])
        html_content = f'''<div>Dear User,<br/><br/>
            The OTP for email verification is: <b>{otp}</b><br/><br/>
            With best wishes,<br/>
            Team Alcheringa
        </div>'''
        msg = EmailMultiAlternatives(
            subject, html_content, from_email, [email])
        msg.content_subtype = "html"
        msg.send()
        doc_ref_otp = db.collection('manage_booking_otps').document(id)
        doc_ref_otp.set({'id': id, 'email': email, 'otp': otp})
    except Exception as e:
        print(e)
    return JsonResponse({"otp": "otp"})


key = b'mysecretkey'


@csrf_exempt
def verifiy_otp_manage_booking(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        email = request.POST['email']
        id = request.POST['passid']
        print(otp)
        otp__db = db.collection(
            'manage_booking_otps').document(id).get().to_dict()
        otp_from_db = otp__db['otp']
        print(otp_from_db)
        if (str(otp) == str(otp_from_db)):
            context = []
            doc__ref = db.collection('users').where('verID', '==', id).stream()
            for doc in doc__ref:
                data_ref = doc.to_dict()
                LAge = data_ref['LAge']
                LEmail = data_ref['LEmail']
                LGender = data_ref['LGender']
                LIDType = data_ref['LIDType']
                LPassType = data_ref['LPassType']
                LName = data_ref['LName']
                LIDNumber = data_ref['LIDNumber']
                curr_data = f"{doc.id}"
                curr_encrypted_data = encrypt_data(
                    str.encode(curr_data), key).decode()
                context.append(
                    {"id": doc.id,
                     'age': LAge,
                     'email': LEmail,
                     'gender': LGender,
                     'id_type': LIDType,
                     'pass_type': LPassType,
                     'name': LName,
                     'id_number': LIDNumber, 'encrypted_id': curr_encrypted_data})

                for mem in doc.reference.collection('members').stream():
                    dict = mem.to_dict()
                    dict["id"] = mem.id
                    curr_data = f"{dict['verID']}"
                    curr_encrypted_data = encrypt_data(
                        str.encode(curr_data), key).decode()
                    dict['encrypted_id'] = curr_encrypted_data
                    context.append(dict)
            print(context)
            return render(request, 'payment/success_.html', {'context': context, "cardid": id})
        return render(request, 'main/verify_otp_manage_booking.html')


@csrf_exempt
def manangebooking(request):
    data = json.loads(request.body)
    id = data['id']
    email = data['email']
    print(id+' '+email)
    doc_ref = db.collection('verified_users').document(id).get().to_dict()
    print(doc_ref)
    if (doc_ref['email'] == email):
        send_verify_otp(email, id)
        print('mail sent')
        return HttpResponse('otp sent!')
    return HttpResponse('mail not found')


def manage_booking_page(request):
    return render(request, 'main/manage.html')



def backupData_users(request):
    doc_ref=db.collection('users').stream()
    data_backup=[]
    for doc in doc_ref:
        memb_dict = []
        for mem in doc.reference.collection('members').stream():
            memb_dict.append({f'{mem.id}=>{mem.to_dict()}'})
        data_backup.append(
            f'{doc.id} => {doc.to_dict()},{"members"}=>{memb_dict}')
    print(data_backup)


def backupData_verified_users(request):
    doc_ref=db.collection('verified_users').stream()
    data_backup=[]
    for doc in doc_ref:
        data_backup.append(f'{doc.id} => {doc.to_dict()}')
    print(data_backup)
    return HttpResponse('ho gaya')


def backupData_transactions(request):
    doc_ref=db.collection('transactions').stream()
    data_backup=[]
    for doc in doc_ref:
        data_backup.append(f'{doc.id} => {doc.to_dict()}')
    print(data_backup)
    return HttpResponse('ho gaya')

def delete_kardega(request):
    doc_ref=db.collection('verified_users').where("email","==","digvijaysihag123@gmail.com").stream()
    for doc in doc_ref:
        doc.reference.delete()
    return HttpResponse('ho gaya delte kuch ab')
    
    
def all_verified_users(request):
    #     doc_ref=db.collection('verified_users').stream()
    #     data = []
    #     # for doc in doc_ref:
    #     #     data.append(f'{doc.id} => {doc.to_dict()}')
    return render(request, 'main/all_paid_users.html')
