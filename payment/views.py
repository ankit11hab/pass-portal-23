from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.http import JsonResponse
from main.views import db


# Create your views here.
# @api_view(['POST'])
def payment_error(request):
    error = request.GET.get('id')
    print(error)
    return render("error.html", {'error':error})


# def payment_status(request):
#     return render(request, 'payment/payment_status.html', {'currstatus':'Payment is under process'})


# def get_status_ajax(request):
#     if request.method == 'GET':
#         doc_ref = db.collection('users').document('123456').get().to_dict()
#         if 'verified' in doc_ref and doc_ref.verified:
#             return JsonResponse({"currstatus": "verified"})
#         elif 'error' in doc_ref:
#             return JsonResponse({"currstatus":"error", "error":doc_ref['error']})
#         else:
#             return JsonResponse({"currstatus":"Payment is under process"})
#     else:
#         return HttpResponse("Request method is not a GET")


def payment_response(request):
    if request.method=='post':
        data=request.POST['data']
        data=decrypt(secretkey,data)
        split_data=data.split('|')
        status=split_data[4]
        errDesc=split_data[5]
        tid=split_data[3]
        id=split_data[0]
        if status==1:
            context={"message":"","success":1,"tid":tid}
        else:
            cotext={"message":errDesc,"success":0,}
        

    leader_id = '123456'
    doc_ref = db.collection('users').document(leader_id).get().to_dict()

    leader_data = {
        "name": doc_ref.LName,
        "contact": doc_ref.LContact,
        "email": doc_ref.LEmail,
        "pass_type": doc_ref.LeaderPassType
    }

    doc_ref2 = db.collection('verified_users').document()
    doc_ref2.set(leader_data)

    for member in doc_ref.members:
        member_data = {
            "name": member.name,
            "contact": member.contact,
            "pass_type": member.pass_type
        }
        doc_ref2 = db.collection('verified_users').document()
        doc_ref2.set(member_data)

    return render("response.html")