import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from main.views import db
from main.encrypt_decrypt import decrypt
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import EmailMessage
import qrcode
from django.conf import settings
import random
import string
from pypdf import PdfWriter, PdfReader
from django.templatetags.static import static
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
import os
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives


# Create your views here.
# @api_view(['POST'])
def payment_error(request):
    error = request.GET.get('id')
    print(error)
    return render("error.html", {'error': error})


# def payment_status(request):
#     return render(request, 'payment/payment_status.html', {'currStatus':'Payment is under process'})


def get_status_ajax(request):
    if request.method == 'GET':
        id = request.GET.get("id")
        # print(request.GET)

        doc_ref = db.collection('users').document(id).get().to_dict()
        print(doc_ref)
        if 'currStatus' in doc_ref:
            if doc_ref['currStatus'] == "verified":
                return JsonResponse({"currStatus": "verified"})
            elif doc_ref['currStatus'] == "error":
                return JsonResponse({"currStatus": "error", "error": doc_ref['error']})
            else:
                return JsonResponse({"currStatus": "Payment is under process"})
        else:
            return JsonResponse({"currStatus": "Payment is under process"})
    else:
        return HttpResponse("Request method is not a GET")


@csrf_exempt
def payment_response(request):
    context = {"message": '', "success": 0, "tid": ''}
    print(context)
    if request.method == 'POST':
        secretkey = "Jkdh9rs6x1mSKH2lDFZ6z6057x4p8CL7"
        data = request.POST['data']
        decrypt_data = decrypt(secretkey, data)
        print(decrypt_data)
        split_data = decrypt_data.split('|')
        status = split_data[4]
        errDesc = split_data[5]
        tid = split_data[3]
        id = split_data[0]
        # id = "GBTCG"
        doc_ref_trans=db.collection('transactions').document(tid)
        doc_ref_trans.set({"id":split_data[0],"fee_type":split_data[1],"amount":split_data[2],"status":status,"errDesc":split_data[5],"time":split_data[6]})
        leader_id = id
        doc_ref = db.collection('users').document(
            leader_id)
        if status == "1":
            print("inside 1")
            context = {"message": "", "success": 1, "tid": tid}
            doc_ref.update({"currStatus": "verified", 'transID': tid})
            leader_data = {
                "name": doc_ref.get().to_dict()['LName'],
                "contact": doc_ref.get().to_dict()['LContact'],
                "email": doc_ref.get().to_dict()['LEmail'],
                "pass_type": doc_ref.get().to_dict()['LPassType'],
                "age": doc_ref.get().to_dict()['LAge'],
                "gender": doc_ref.get().to_dict()['LGender'],
                "transID": tid,
                "day1": True,
                "day2": True,
                "day3": True
            }
            doc_ref2 = ''
            while True:
                memID = ''.join(random.choices(string.ascii_uppercase +
                                               string.digits, k=5))
                doc_ref2 = db.collection('verified_users').document(memID)
                if not doc_ref2.get().exists:
                    doc_ref2.set(leader_data)
                    break
            doc_ref.update({"verID":doc_ref2.id})       
            docref3 = db.collection('verified_users').document(doc_ref2.id)
            leader_array = {
                'name': docref3.get().to_dict()['name'],
                'pass_type': docref3.get().to_dict()['pass_type'],
                'id': docref3.id,
            }
            print(leader_array)
            i = 0
            member_array = []
            for member_doc in doc_ref.collection('members').stream():
                member=member_doc.to_dict()
                member_data = {
                    "name": member['name'],
                    "contact": member['contact'],
                    "pass_type": member['pass_type'],
                    "email": member['email'],
                    "age": member['age'],
                    "gender": member['gender'],
                    "transID": tid,
                    "day1": True,
                    "day2": True,
                    "day3": True
                }
                doc_ref2 = ''
                while True:
                    memID = ''.join(random.choices(string.ascii_uppercase +
                                                   string.digits, k=5))
                    doc_ref2 = db.collection('verified_users').document(memID)
                    if not doc_ref2.get().exists:
                        doc_ref2.set(member_data)
                        break
                doc_ref.collection('members').document(member_doc.id).update({"verID":doc_ref2.id})
                member_array.append(
                    {'name': member_data['name'], 'pass_type': member_data['pass_type'], 'id': doc_ref2.id})
            print(member_array)
            info = doc_ref.get().to_dict()
            email = info['LEmail']
            name = info['LName']
            passid=info['verID']
            # count = request.session.get('count')
            from_email = settings.EMAIL_HOST_USER
            subject = 'Confirmation Mail'
            otp = random.randint(1000, 9999)
            message = 'Your registeration for Alcheringa 2023 has been sent to us.Hang on to your cape and keep an eye out we will send you a QR code shortly'
            from_email = settings.EMAIL_HOST_USER
            # send_mail(subject, message, from_email, [email])
            html_content = f'''<div>Dear {name},<br/><br/>
                Your registration for Alcheringa 2023 has been sent to us. Kindly take screenshot of the passes with the QR codes that are being shown on the website.<br/><br/>
                Your passID is {passid}.
                With best wishes,<br/>
                Team Alcheringa
            </div>'''
            msg = EmailMultiAlternatives(subject, html_content, from_email, [email])
            msg.content_subtype = "html"
            msg.send()
            # generate_qr_code(request,leader_array,member_array)
            return redirect('get_payment_details')
        else:
            doc_ref = db.collection('users').document(
                leader_id)
            doc_ref.update({"currStatus": "error", "error": errDesc})
            context = {"message": errDesc, "success": 0, "tid": tid}
            print(context)

    return render(request, "payment/response.html", context)


@csrf_exempt
def success(request):
    return render(request, 'payment/success_.html')


@csrf_exempt
def under_process(request):
    return render(request, 'under_process.html')

@csrf_exempt
def encrypt_data(data, key):
    """Encrypt the data using XOR encryption and a given key"""
    encrypted_data = bytearray(len(data))
    key_len = len(key)
    for i in range(len(data)):
        encrypted_data[i] = data[i] ^ key[i % key_len]
    return bytes(encrypted_data)

@csrf_exempt
def get_verified_details(request):
    # print('called')
 if request.method=="POST":
    id=request.POST['uid']
    doc_ref = db.collection('users').document(id)
    tid = doc_ref.get().to_dict()['transID']
    # id,name,pass_type
    q = db.collection('verified_users').where('transID', '==', tid).stream()
    context = []
    
    for doc in q:
        doc_dict = doc.to_dict()
        doc_dict['id'] = doc.id
        context.append(doc_dict)
       
    print(context)
    key = b'mysecretkey'
    print(type(key))
  
    for member in context:
        curr_data = f"{member['id']}"
        curr_encrypted_data = encrypt_data(str.encode(curr_data), key).decode()
        member['encrypted_id'] = curr_encrypted_data
        member['id'] = member['name'].replace(" ","")+member['email'].split('@')[0]+member['id'][:4]
    print(context)
   
    
    return render(request, 'payment/success_.html', {'context': context,"cardid":id})


def get_payment_details(request):
    return render(request, 'payment/transaction_done.html')

# def generate_qr_code(request):
#     # email = request.session.get('LeaderEmail')
#     email = "akshat.aksat@iitg.ac.in"
#     count = request.session.get('count')
#     from_email = settings.EMAIL_HOST_USER
#     message = EmailMessage(
#         'QR code',
#         'Here is the Pass you requested',
#         from_email,
#         [email],
#     )
#     qr = qrcode.QRCode(version=6,
#                        box_size=18,
#                        border=4,)
#     qr.add_data(
#         {'name': 'leader[', 'pass_type': 'leader[', 'id': 'leader['})
#     qr.make()
#     img = qr.make_image(fill_color="#fffde9",
#                         back_color="black")
#     # lid = leader['id']
#     lid = 123456789
#     img.save(static(f'static/QRcode/{lid}.png'), format='PNG')
#     gen_pdf(lid)
#     message.attach_file(static(f'static/pdf/{lid}.pdf'))
#     members = [1, 2, 3, 4]
#     for mid in members:
#         qr = qrcode.QRCode()
#         qr.add_data(
#             {'name': member['name'], 'pass_type': member['pass_type'], 'id': member['id']})
#         qr.make()
#         img = qr.make_image(fill_color="#fffde9",
#                             back_color="black")
#         mid = member['id']
#         img.save(static(f'static/QRcode/{mid}.png'), format='PNG')
#         gen_pdf(mid)
#         message.attach(static(f'static/pdf/{mid}.pdf'))
#     message.send()

#     return HttpResponse('Pass sent!')


# def gen_pdf(pdfID):
#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=(2000, 2000))
#     can.drawImage(static(f"static/QRcode/{pdfID}.png"), 1100, 800)
#     can.save()
#     packet.seek(0)
#     new_pdf = PdfReader(packet)
#     existing_pdf = PdfReader(
#         open(static("static/exclusive_alcheringa.pdf"), "rb"))
#     output = PdfWriter()
#     page = existing_pdf.pages[0]
#     page.merge_page(new_pdf.pages[0])
#     output.add_page(page)
#     output.add_page(existing_pdf.pages[1])
#     outputStream = open(static(f'static/pdf/{pdfID}.pdf'), "wb")
#     output.write(outputStream)
#     outputStream.close()
