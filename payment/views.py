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
import random
import string
from pypdf import PdfWriter, PdfReader
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io


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
        # status = split_data[4]
        status = '1'
        errDesc = split_data[5]
        tid = split_data[3]
        # id = split_data[0]
        id = "LNDKR6O0"
        leader_id = id
        doc_ref = db.collection('users').document(
            leader_id)
        if status == "1":
            print("inside 1")
            context = {"message": "", "success": 1, "tid": tid}
            doc_ref.update({"currStatus": "verified",'transID':tid})
            leader_data = {
                "name": doc_ref.get().to_dict()['LName'],
                "contact": doc_ref.get().to_dict()['LContact'],
                "email": doc_ref.get().to_dict()['LEmail'],
                "pass_type": doc_ref.get().to_dict()['LPassType'],
                "age": doc_ref.get().to_dict()['LAge'],
                "gender": doc_ref.get().to_dict()['LGender'],
                "transID": tid,
            }
            doc_ref2 = ''
            while True:
                memID = ''.join(random.choices(string.ascii_uppercase +
                                               string.digits, k=8))
                doc_ref2 = db.collection('verified_users').document(memID)
                if not doc_ref2.get().exists:
                    doc_ref2.set(leader_data)
                    break

            docref3 = db.collection('verified_users').document(doc_ref2.id)
            leader_array = {
                'name': docref3.get().to_dict()['name'],
                'pass_type': docref3.get().to_dict()['pass_type'],
                'id': docref3.id,
            }
            # print(leader_array)
            i = 0
            member_array = []
            for member in doc_ref.get().to_dict()['members']:
                member_data = {
                    "name": member['name'],
                    "contact": member['contact'],
                    "pass_type": member['pass_type'],
                    "email":member['email'],
                    "age":member['age'],
                    "gender":member['gender'],
                    "transID": tid
                }
                doc_ref2 = ''
                while True:
                    memID = ''.join(random.choices(string.ascii_uppercase +
                                                   string.digits, k=8))
                    doc_ref2 = db.collection('verified_users').document(memID)
                    if not doc_ref2.get().exists:
                        doc_ref2.set(member_data)
                        break
                # doc_ref2 = db.collection('verified_users').document()
                # doc_ref2.set(member_data)
                member_array.append(
                    {'name': member_data['name'], 'pass_type': member_data['pass_type'], 'id': doc_ref2.id})
                # doc_ref = db.collection('users').document(
                #     leader_id)
                # members = doc_ref.get().to_dict()["members"]
                # print(doc_ref2.id)
                # member.update({"id": doc_ref2.id})
                # doc_ref.update(
                #     {"members[i]['id']": doc_ref2.id})
                # i += 1
                # member.set({"id": doc_ref2.get().to_dict()['id']})
                # print(context)
            # print(member_array)
                # generate_qr_code(request,leader_array,member_array)
            return redirect('get_verified_details')
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
    return render(request,'under_process.html')

def generate_qr_code(request,leader,members):
    # email="akshat.akshat@iitg.ac.in"
    email = request.session.get('LeaderEmail')
    count = request.session.get('count')
    from_email = settings.EMAIL_HOST_USER
    message = EmailMessage(
        'QR code',
        'Here is the QR code you requested',
        from_email,
        [email],
    )
    qr = qrcode.QRCode(version=6,
    box_size=18,
    border=4,)
    qr.add_data(
        {'name': leader['name'], 'pass_type': leader['pass_type'], 'id': leader['id']})
    # qr.add_data(
        # {'name': 'leadeLName', 'pass_type': 'leaderLPassType', 'id': 'leaderid'})
    qr.make()
    img = qr.make_image(fill_color="#fffde9",
                        back_color="black")
    lid = leader['id']
    # lid=2
    img.save(f'assests/QRcode/{lid}.png', format='PNG')
    gen_pdf(lid)
    # with open(f'{lid}.pdf', "rb") as f:
    #     pdfToSend = f.read()
    message.attach_file(f'assests/pdf/{lid}.pdf')
    for member in members:
        qr = qrcode.QRCode()
        qr.add_data(
            {'name': member['name'], 'pass_type': member['pass_type'], 'id': member['id']})
        qr.make()
        img = qr.make_image(fill_color="#fffde9",
                        back_color="black")
        mid = member['id']
        img.save(f'static/QRcode/{mid}.png', format='PNG')
        gen_pdf(mid)
        # with open(f'{mid}.pdf', "rb") as f:
        #     pdfToSend = f.read()
        message.attach(f'assests/pdf/{mid}.pdf')
    message.send()

    return HttpResponse('QR code email sent!')

@csrf_exempt
def get_verified_details(request):
    print('called')
    if request.method=="POST":
        print('entered')
        id1=json.loads(request.body)['id']
        # tid=220075070
        # print(id1)
        doc_ref = db.collection('users').document(id1)
        tid=doc_ref.get().to_dict()['transID']
        # id,name,pass_type
        q=db.collection('verified_users').where('transID','==',tid).stream()
        context=[]
        for doc in q :
            context.append(doc.to_dict())
        print(context)
        return render(request,'payment/success_.html',{'context':context})
    return render(request,'payment/success_.html')


def gen_pdf(pdfID):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=(2000, 2000))
    can.drawImage(f"{pdfID}.png", 1100, 800)
    can.save()
    packet.seek(0)
    new_pdf = PdfReader(packet)
    existing_pdf = PdfReader(open("assets/exclusive_alcheringa.pdf", "rb"))
    output = PdfWriter()
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    output.add_page(existing_pdf.pages[1])
    outputStream = open(f"assests/pdf/{pdfID}.pdf", "wb")
    output.write(outputStream)
    outputStream.close()