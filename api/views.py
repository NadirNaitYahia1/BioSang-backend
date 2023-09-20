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
    id_Patient = int(request.data.get('id_Patient'))
    password = request.data.get('password')
    
  
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

    try :
        user = Patient.objects.filter(id_Patient=payload['id_Patient']).first()
    except :
        return Response({'error': 'id_Patient is wrong!'}, status='400')
    serializer = PatientSerializer(user)

    analyses = Analyse.objects.filter(patient_id=user.id_Patient)
    serializerAnalyse = AnalyseSerializer(analyses, many=True)
    
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
    id_Admin =  (request.data.get('id_Admin'))
    password = request.data.get('password')  
    try:
        user = Admin.objects.filter(id_Admin=id_Admin).first()
     
        if not user.check_password(password):
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
    response.data = {
        'message': 'Login successful',
        'jwt': token
    }
    return response

 
 
 
@api_view(['GET'])
def getAdmin(request):
    auth_header = request.headers.get('Authorization')  # Retrieve the 'Authorization' header
    if not auth_header:
        raise AuthenticationFailed('Unauthenticated!')
    
    try:
        token = auth_header.split(' ')[1]  # Extract the token part from the header (Bearer token)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    try :
        user = Admin.objects.filter(id_Admin=payload['id_Admin']).first()
    except :
        return Response({'error': 'id_Admin is wrong!'}, status='400')
    serializer = AdminSerializer(user)
    return Response(serializer.data)



@api_view(['POST'])
def RegisterUser(request):
    auth_header = request.headers.get('Authorization')  # Retrieve the 'Authorization' header
    if not auth_header:
        raise AuthenticationFailed('Unauthenticated!')
    
    try:
        token = auth_header.split(' ')[1]  # Extract the token part from the header (Bearer token)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')
    
    admin = get_object_or_404(Admin, id_Admin=payload['id_Admin'])  # Retrieve the admin object
    
    print('request.data',request.data)
    name = request.data.get('name')
    prenom = request.data.get('prenom')
    date = request.data.get('date_naissance')
    try :
        user = Patient.objects.filter(name=name,prenom=prenom,date_naissance=date).first()
        if user:
            patient_id = user.id_Patient
            print('(((((((((((((((((USER EXIST)))))))))))))))))))))')
        else :
            serializer = PatientSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['id_admin'] = admin  # Assign the admin object to id_admin field
            serializer.save()
            patient_id = serializer.data['id_Patient']  

    

    except :
        print('heeeeeelooooo wooorld')
        pass
  
    # ajouter analyse :
 
    

    date = '2021-05-05'
    file = 'file'

# Get the uploaded file from request.FILES


 
    admin =  get_object_or_404(Admin, id_Admin=payload['id_Admin'])
    admin_id = admin.id_Admin
    data = {
        'date': date,
         
        'admin_id': admin_id, 
        'patient_id': patient_id,   
    }


    Analyse_serializer = AnalyseSerializer (data=data)
    print("data",data)
        
    if Analyse_serializer.is_valid():
        Analyse_serializer.save() 
        return Response(Analyse_serializer.data,status=200)
    else:
        return Response(Analyse_serializer.errors, status=400)
        
 




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
    try :
        user = Admin.objects.filter(id_Admin=payload['id_Admin']).first()
    except :
        return Response({'error': 'id_Admin is wrong!'}, status='400')

    analyses = Analyse.objects.all()
    serializerAnalyse = AnalyseSerializer(analyses, many=True)
    
    return Response(serializerAnalyse.data)


@api_view(['GET'])
def getPatients(request):
    auth_header = request.headers.get('Authorization')  # Retrieve the 'Authorization' header
    if not auth_header:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        token = auth_header.split(' ')[1]  # Extract the token part from the header (Bearer token)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    patients = Patient.objects.all()
    patientSerializer = PatientSerializer(patients, many=True)
    serialized_data = patientSerializer.data  # Get the serialized data

    return Response(serialized_data)  # Return the serialized data as a JSON response

@api_view(['GET'])
def getAdmins(request):
    auth_header = request.headers.get('Authorization')  # Retrieve the 'Authorization' header
    if not auth_header:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        token = auth_header.split(' ')[1]  # Extract the token part from the header (Bearer token)
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    admin = Admin.objects.all()
    adminSerializer = AdminSerializer(admin, many=True)
    serialized_data = adminSerializer.data  # Get the serialized data

    return Response(serialized_data)  # Return the serialized data as a JSON response

@api_view(['POST'])
def uploadFile(request):
    if request.method == 'POST':

        auth_header = request.headers.get('Authorization')  # Retrieve the 'Authorization' header
        if not auth_header:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            token = auth_header.split(' ')[1]  # Extract the token part from the header (Bearer token)
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')


       
        
      
        # Get additional data from request.data
        patient_id = request.data.get('patient_id')
        print('patient_id',patient_id)
        date = request.data.get('date')

        # Get the uploaded file from request.FILES
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            print("error no file")
            return Response({'error': 'No file uploaded.'}, status=400)

 
        admin =  get_object_or_404(Admin, id_Admin=payload['id_Admin'])
        admin_id = admin.id_Admin
        patient = get_object_or_404(Patient, id_Patient= patient_id)

        data = {
            'date': date,
            'fichier': uploaded_file,
            'admin_id': admin_id, 
            'patient_id': patient_id,   
        }

        serializer = AnalyseSerializer(data=data)


        
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'success'}, status=200)
        else:
            return Response(serializer.errors, status=400)
        
    return Response({'error': 'Invalid request method.'}, status=405)