from django.shortcuts import render
from django.http import JsonResponse
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from .models import Patient
from .models import Analyse
from .serializers import PatientSerializer
from .serializers import AnalyseSerializer
from api.models import Patient, Admin
from django.shortcuts import get_object_or_404
from .serializers import AdminSerializer
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime

from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def gettest(request):
    return JsonResponse('Api is working',safe=False)

@api_view(['POST'])
def RegisterAdmin(request):
    serializer = AdminSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)

@api_view(['POST'])
def RegisterUser(request):
    admin_id = request.data.get('id_admin')  # Get the admin id from the request data
    admin = get_object_or_404(Admin, id_Admin=admin_id)  # Retrieve the admin object
    
    serializer = PatientSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    serializer.validated_data['id_admin'] = admin  # Assign the admin object to id_admin field
    serializer.save()
    
    return Response(serializer.data)



@api_view(['POST'])
def loginUser(request):
    print('--------------------------------------------RECIVE DATA--------------------------------------------')
    print("request",request.data)
    id_Patient = int(request.data.get('id_Patient'))
    print("id_Patient",id_Patient)
    password = request.data.get('password')
    print("password",password)
    
  

    user = Patient.objects.filter(id_Patient=id_Patient).first() 
    print("user",user)
    print("user",user.password)
   
    if user is None:
        print("user is None")
    
    if not user.check_password(password):
        print("not user.check_password(password)")


    payload = {
        'id_Patient': user.id_Patient,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }

    # # Generate a random secret key
  
    token = jwt.encode(payload, 'secret', algorithm='HS256') 
    
    response = Response()
    response.set_cookie('jwt', token, httponly=True, samesite='Strict')
    print('--------------------------------///------------SEND DATA--------------------------------------------')
    response.data = {
        'message': 'Login successful',
        'jwt': token
    }
    return response

 
 

@api_view(['GET'])
def user(request):
    token = request.COOKIES.get('jwt')
    print("token   get--------------------------",token)
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user = Patient.objects.filter(id_Patient=payload['id_Patient']).first()
    serializer = PatientSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
def logoutUser(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'success'
    }
    return response





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getAnalyses(request):
    token = request.COOKIES.get('jwt')

    print("token   get--------------------------",token)
    
    if not token:
        raise AuthenticationFailed('Unauthenticated!')
    
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    
    try:
        user = Patient.objects.get(id_Patient=payload['id_Patient'])
        print("user--------------------------------->>>>>>>>>>>>>", user)
    except Patient.DoesNotExist:
        raise AuthenticationFailed('User not found!')
    
    print("user id:", user.id_Patient)
    analyses = Analyse.objects.filter(patient_id=user.id_Patient)  # Use the correct field name
    serializerAnalyse = AnalyseSerializer(analyses, many=True)
    print("analyses------------------->>>>>>>>>>>>>", serializerAnalyse.data)
    
    return Response(serializerAnalyse.data)






# @api_view(['POST'])
# def getAnalyses(request):
#     token = request.COOKIES.get('jwt')
#     print("token   get--------------------------",token)
#     if not token:
#         raise AuthenticationFailed('Unauthenticated!')
#     try:
#         payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#     except jwt.ExpiredSignatureError:
#         raise AuthenticationFailed('Unauthenticated!')

#     user = Patient.objects.filter(id_Patient=payload['id_Patient']).first()
#     serializer = PatientSerializer(user)
#     print("id Patient !!", (serializer.data['id_Patient']))
    
#     try:
#         analyses = Analyse.objects.filter(id_Patient=serializer.data['id_Patient'])
#         serializerAnalyse = AnalyseSerializer(analyses, many=True)
#         print("serializerAnalyse.data::::::::::::::::::::::::::",serializerAnalyse.data)
#     except:
#         print('eeeeeeeeeeeeeerrrrrrrrrrrrrrrrrrrrrrrrrrrrrroooooooooooooooooooooorrrrrrrrrrr')
#     return Response(serializerAnalyse.data)