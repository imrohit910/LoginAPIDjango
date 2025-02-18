from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.hashers import check_password
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from .models import MyApp
from .serializers import MyAPPSerializer, LoginSerializer

User = get_user_model()  # Use custom user model

@api_view(['POST'])
def create_user(request):
    serializer = MyAPPSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)  # Generate token on signup
        return Response({'message': 'User created successfully', 'token': token.key, 'data': serializer.data}, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            user_obj = User.objects.get(email=email)  # Get custom user model
            if check_password(password, user_obj.password):
                token, _ = Token.objects.get_or_create(user=user_obj)  # Ensure token works for `MyApp`
                return Response({
                    'message': 'Login successful',
                    'token': token.key,
                    'user': {
                        'id': user_obj.id,
                        'name': user_obj.name,
                        'email': user_obj.email,
                        'mobile': user_obj.mobile,
                    }
                }, status=200)
            else:
                return Response({'error': 'Invalid credentials'}, status=400)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)

    return Response(serializer.errors, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])  
def account(request):
    user = request.user
    user_data = {
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'mobile': user.mobile,
    }
    return Response(user_data, status=200)
