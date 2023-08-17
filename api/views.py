from django.shortcuts import render
from django.http import JsonResponse
 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import redirect
from .models import Patient
from .serializers import PatientSerializer
from api.models import Patient, Admin
from django.shortcuts import get_object_or_404
from .serializers import AdminSerializer
from rest_framework.exceptions import AuthenticationFailed
import jwt, datetime
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
    id_Patient = request.data.get('id_Patient')
    print("id_Patient",id_Patient)
    password = request.data.get('password')
    print("password",password)
    
   
    user = Patient.objects.filter(id_Patient=id_Patient).first() 
    print("user",user.password)
   
    if user is None:
        raise AuthenticationFailed('User not found!')
    
    if not user.check_password(password):
        raise AuthenticationFailed('Incorrect password!')
    


    payload = {
        'id_Patient': user.id_Patient,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'your-secret-key', algorithm='HS256') 
    
    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'message': 'Login successful',
        'jwt': token
    }
    return response
 

@api_view(['GET'])
def user(request):
    token = request.COOKIES.get('jwt')
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