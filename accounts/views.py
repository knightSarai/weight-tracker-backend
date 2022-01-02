from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from rest_framework import authentication, permissions, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from accounts.serializers import UserSerializer, RegisterUserSerializer


@method_decorator(ensure_csrf_cookie, name="dispatch")
class GetCSRFToken(APIView):
    @staticmethod
    def get(request):
        return JsonResponse({'success': 'CSRF cookie set'})


@method_decorator(ensure_csrf_cookie, name="dispatch")
class LoginView(APIView):
    def post(self, request):
        try:
            data = self.request.data
            username = data.get("username")
            password = data.get("password")

            if username is None or password is None:
                return JsonResponse({"message": "Username and Password is needed"}, status=500)

            user = authenticate(username=username, password=password)

            if not user:
                return JsonResponse({"message": "User does not exist"}, status=500)

            login(request, user)
            user_serializer = UserSerializer(user)
            trainee_id = user.trainee.id
            return JsonResponse({
                "message": "User logged in successfully",
                "user": user_serializer.data,
                "trainee_id": trainee_id
            })

        except Exception as e:
            return JsonResponse({"message": f"{e!r}"}, status=500)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class LogoutViw(APIView):
    authentication_class = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            logout(request)
            return JsonResponse({"message": "User logged out successfully"})
        except Exception as e:
            return JsonResponse({"message": f"User logged out error {e!r}"}, status=500)


class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterUserSerializer


class BlacklistTokenView(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def post(request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as e:
            return Response({'message': f'{e!r}'}, status=400)


# @method_decorator(ensure_csrf_cookie, name="dispatch")
# class SignUpView(APIView):
#     def post(self, request):
#         try:
#             data = self.request.data
#             username = data.get("username")
#             email = data.get("email")
#             password = data.get("password")
#             password_confirm = data.get("passwordConfirm")
#
#             if not username or not email or not password or not password_confirm:
#                 return JsonResponse({"message": "All fields are required"}, status=500)
#
#             if password != password_confirm:
#                 return JsonResponse({"message": "Passwords don't match"}, status=500)
#
#             with transaction.atomic():
#                 user = User.objects.create_user(username=username, email=email, password=password)
#                 Trainee.objects.create(user=user)
#
#             return JsonResponse({"message": "User created in successfully"})
#
#         except Exception as e:
#             return JsonResponse({"message": f"{e!r}"}, status=500)


@method_decorator(csrf_protect, name="dispatch")
class CheckLoggedIn(APIView):
    authentication_class = [authentication.SessionAuthentication]
    permission_classes = [permissions.AllowAny]

    @staticmethod
    def get(request):
        req_user = request.user.username
        if not req_user:
            return JsonResponse({"message": "No logged in user found"}, status=500)
        user = User.objects.get(username=req_user)
        user_serializer = UserSerializer(user)
        trainee_id = user.trainee.id
        return JsonResponse({"user": user_serializer.data, "trainee_id": trainee_id})
