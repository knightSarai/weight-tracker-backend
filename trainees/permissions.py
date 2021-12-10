from rest_framework.permissions import BasePermission, SAFE_METHODS


class WeightMeasurementPermission(BasePermission):
    message = 'Editing/Retrieving measurement is restricted to the trainee or its trainer only.'

    def has_object_permission(self, request, view, obj):
        is_user_trainer = obj.trainee.trainer.user == request.user
        is_owner = obj.trainee.user == request.user

        return is_user_trainer or is_owner
