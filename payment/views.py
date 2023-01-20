from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse
from main.views import db
from main.encrypt_decrypt import decrypt
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
# @api_view(['POST'])
def payment_error(request):
    error = request.GET.get('id')
    print(error)
    return render("error.html", {'error': error})


# def payment_status(request):
#     return render(request, 'payment/payment_status.html', {'currstatus':'Payment is under process'})


def get_status_ajax(request):
    if request.method == 'GET':
        id = request.GET.get("id")
        # print(request.GET)

        doc_ref = db.collection('users').document(id).get().to_dict()
        print(doc_ref)
        if doc_ref['currStatus'] == "verified":
            return JsonResponse({"currstatus": "verified"})
        elif doc_ref['currStatus'] == "error":
            return JsonResponse({"currstatus": "error", "error": doc_ref['error']})
        else:
            return JsonResponse({"currstatus": "Payment is under process"})
    else:
        return HttpResponse("Request method is not a GET")


@csrf_exempt
def payment_response(request):
    context = {"message": '', "success": 0, "tid": ''}
    if request.method == 'POST':
        secretkey = "Jkdh9rs6x1mSKH2lDFZ6z6057x4p8CL7"
        data = request.POST['data']
        decryptdata = decrypt(secretkey, data)
        split_data = decryptdata.split('|')
        status = split_data[4]
        errDesc = split_data[5]
        tid = split_data[3]
        id = split_data[0]
        # id = "B9UFZ58T8BM"
        leader_id = id
        doc_ref = db.collection('users').document(
            leader_id)
        if status == "1":
            context = {"message": "", "success": 1, "tid": tid}
            doc_ref.update({"currStatus": "verified"})
            leader_data = {
                "name": doc_ref.get().to_dict()['LName'],
                "contact": doc_ref.get().to_dict()['LContact'],
                "email": doc_ref.get().to_dict()['LEmail'],
                "pass_type": doc_ref.get().to_dict()['LPassType'],
                "transID": tid
            }

            doc_ref2 = db.collection('verified_users').document()

            doc_ref2.set(leader_data)
            i = 0
            for member in doc_ref.get().to_dict()['members']:
                member_data = {
                    "name": member['name'],
                    "contact": member['contact'],
                    "pass_type": member['pass_type'],
                    "transID": tid
                }
                doc_ref2 = db.collection('verified_users').document()
                doc_ref2.set(member_data)
                # doc_ref = db.collection('users').document(
                #     leader_id)
                # members = doc_ref.get().to_dict()["members"]
                # print(doc_ref2.id)
                # member.update({"id": doc_ref2.id})
                # doc_ref.update(
                #     {"members[i]['id']": doc_ref2.id})
                # i += 1
                # member.set({"id": doc_ref2.get().to_dict()['id']})
                print(context)
            return redirect('payment_success')
        else:
            doc_ref = db.collection('users').document(
                leader_id)
            doc_ref.update({"currStatus": "error", "error": errDesc})
            context = {"message": errDesc, "success": 0, "tid": tid}
            print(context)

    return render(request, "payment/response.html", context)


@csrf_exempt
def success(request):
    return render(request, 'payment/success.html')
