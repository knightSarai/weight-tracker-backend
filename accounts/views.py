from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework import authentication, permissions
from rest_framework.views import APIView

from accounts.serializers import UserSerializer


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
                return JsonResponse({"error: ": "Username and Password is needed"})

            user = authenticate(username=username, password=password)

            if not user:
                return JsonResponse({"error:": "User does not exist"})

            login(request, user)
            user_serializer = UserSerializer(user)
            return JsonResponse({
                "message": "User logged in successfully",
                "user": user_serializer.data
            })

        except Exception as e:
            return JsonResponse({"message": f"{e!r}"})


@method_decorator(ensure_csrf_cookie, name="dispatch")
class LogoutViw(APIView):
    authentication_class = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    @staticmethod
    def get(request):
        try:
            logout(request)
            return JsonResponse({"success": "User logged out successfully"})
        except Exception as e:
            return JsonResponse({"error": f"User logged out error {e!r}"})
