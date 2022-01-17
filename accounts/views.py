from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.models import User
from accounts.serializers import UserSerializer, RegisterUserSerializer, CustomTokenObtainPairSerializer


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRFToken(APIView):
    @staticmethod
    def get(request):
        return JsonResponse({'success': 'CSRF cookie set'})


class LoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterUserSerializer


class LogoutView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({'message': f'{e!r}'}, status=400)


class CheckLoggedIn(APIView):
    @staticmethod
    def get(request):
        req_user = request.user.username
        if not req_user:
            return JsonResponse({"message": "No logged in user found"}, status=500)
        user = User.objects.get(username=req_user)
        user_serializer = UserSerializer(user)
        trainee_id = user.trainee.id
        return JsonResponse({"user": user_serializer.data, "trainee_id": trainee_id})
