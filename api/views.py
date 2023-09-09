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
def loginUser(request):
    print('--------------------------------------------RECIVE DATA--------------------------------------------')
    print("request",request.data)
    id_Patient = int(request.data.get('id_Patient'))
    print("id_Patient",id_Patient)
    password = request.data.get('password')
    print("password",password)
    
  
    try:
        user = Patient.objects.filter(id_Patient=id_Patient).first()
        if not user.check_password(password):
            return Response({'error': 'password  is wrong'}, status='400')

    except:
        return Response({'error': 'password or id_Patient is wrong!'}, status='400')
        

    payload = {
        'id_Patient': user.id_Patient,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }

    # # Generate a random secret key
  
    token = jwt.encode(payload, 'secret', algorithm='HS256') 
    
    response = Response()
    # response.set_cookie('jwt', token, httponly=True, samesite='Strict')
    print('--------------------------------///------------SEND DATA--------------------------------------------')
    response.data = {
        'message': 'Login successful',
        'jwt': token
    }
    return response

 
 
 
@api_view(['GET'])
def user(request):
    auth_header = request.headers.get('Authorization')  # Retrieve the 'Authorization' header
    if not auth_header:
        raise AuthenticationFailed('Unauthenticated!')
    
    try:
        token = auth_header.split(' ')[1]  # Extract the token part from the header (Bearer token)
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
def getAnalyses(request):
    auth_header = request.headers.get('Authorization')  # Retrieve the 'Authorization' header
    if not auth_header:
        raise AuthenticationFailed('Unauthenticated!')
    
    try:
        token = auth_header.split(' ')[1]  # Extract the token part from the header (Bearer token)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user = Patient.objects.filter(id_Patient=payload['id_Patient']).first()
    serializer = PatientSerializer(user)

    analyses = Analyse.objects.filter(patient_id=user.id_Patient)
    serializerAnalyse = AnalyseSerializer(analyses, many=True)
    print("analyses------------------->>>>>>>>>>>>>", serializerAnalyse.data)
    
    return Response(serializerAnalyse.data)


# --------------------------------------------ADMIN--------------------------------------------
@api_view(['POST'])
def RegisterAdmin(request):
    serializer = AdminSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)
 
@api_view(['POST'])
def loginAdmin(request):
    print('--------------------------------------------RECIVE DATA--------------------------------------------')
    print("request",request.data)
    id_Admin =  (request.data.get('id_Admin'))
    password = request.data.get('password')  
    try:
        user = Admin.objects.filter(id_Admin=id_Admin).first()
     
        if not user.check_password(password):
            print("password is wrong")
            return Response({'error': 'password  is wrong'}, status='400')

    except:
        return Response({'error': 'password or id_Patient is wrong!'}, status='400')
        

    payload = {
        'id_Admin': user.id_Admin,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }

    # # Generate a random secret key
  
    token = jwt.encode(payload, 'secret', algorithm='HS256') 
    
    response = Response()
    # response.set_cookie('jwt', token, httponly=True, samesite='Strict')
    print('--------------------------------///------------SEND DATA--------------------------------------------')
    response.data = {
        'message': 'Login successful',
        'jwt': token
    }
    return response

 
 
 
@api_view(['GET'])
def getAdmin(request):
    print('--------------------------------------------RECIVE DATA--------------------------------------------')
    auth_header = request.headers.get('Authorization')  # Retrieve the 'Authorization' header
    print("auth_header",auth_header)
    if not auth_header:
        raise AuthenticationFailed('Unauthenticated!')
    
    try:
        token = auth_header.split(' ')[1]  # Extract the token part from the header (Bearer token)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        print("payload",payload)
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user = Admin.objects.filter(id_Admin=payload['id_Admin']).first()
    serializer = AdminSerializer(user)
    print('serializer.data',serializer.data)
    return Response(serializer.data)



@api_view(['POST'])
def RegisterUser(request):
    auth_header = request.headers.get('Authorization')  # Retrieve the 'Authorization' header
    print("auth_header",auth_header)
    if not auth_header:
        raise AuthenticationFailed('Unauthenticated!')
    
    try:
        token = auth_header.split(' ')[1]  # Extract the token part from the header (Bearer token)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        print("payload",payload)
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    
    print('id_admin',payload['id_Admin'])
    admin = get_object_or_404(Admin, id_Admin=payload['id_Admin'])  # Retrieve the admin object
    
    serializer = PatientSerializer(data=request.data)
  
    serializer.is_valid(raise_exception=True)

    serializer.validated_data['id_admin'] = admin  # Assign the admin object to id_admin field
    print('error',serializer.errors)
    serializer.save()
    
    return Response(serializer.data)


@api_view(['GET'])
def getAnalysesForAdmin(request):
    auth_header = request.headers.get('Authorization')  # Retrieve the 'Authorization' header
    if not auth_header:
        raise AuthenticationFailed('Unauthenticated!')
    
    try:
        token = auth_header.split(' ')[1]  # Extract the token part from the header (Bearer token)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')


    analyses = Analyse.objects.all()
    serializerAnalyse = AnalyseSerializer(analyses, many=True)
    print("analyses------------------->>>>>>>>>>>>>", serializerAnalyse.data)
    
    return Response(serializerAnalyse.data)


@api_view(['GET'])
def getPatients(request):
    print('request', request)
    auth_header = request.headers.get('Authorization')  # Retrieve the 'Authorization' header
    print("auth_header", auth_header)
    if not auth_header:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        token = auth_header.split(' ')[1]  # Extract the token part from the header (Bearer token)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    patients = Patient.objects.all()
    print("patients------------------->>>>>>>>>>>>>", patients)
    patientSerializer = PatientSerializer(patients, many=True)
    serialized_data = patientSerializer.data  # Get the serialized data
    print("patients------------------->>>>>>>>>>>>>", serialized_data)

    return Response(serialized_data)  # Return the serialized data as a JSON response

@api_view(['GET'])
def getAdmins(request):
    print('request', request)
    auth_header = request.headers.get('Authorization')  # Retrieve the 'Authorization' header
    print("auth_header", auth_header)
    if not auth_header:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        token = auth_header.split(' ')[1]  # Extract the token part from the header (Bearer token)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    admin = Admin.objects.all()
    print("patients------------------->>>>>>>>>>>>>", admin)
    adminSerializer = AdminSerializer(admin, many=True)
    serialized_data = adminSerializer.data  # Get the serialized data
    print("patients------------------->>>>>>>>>>>>>", serialized_data)

    return Response(serialized_data)  # Return the serialized data as a JSON response
