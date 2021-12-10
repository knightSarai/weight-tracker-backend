from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from trainers.models import Trainer
from .models import WeightMeasurement, Trainee


class MeasurementsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        test_user = User.objects.create(
            username='test_user',
            password='123456789'
        )
        test_user_trainer = User.objects.create(
            username='test_user_trainer',
            password='123456789'
        )

        test_user_2 = User.objects.create(
            username='test_user_2',
            password='123456789'
        )
        trainer = Trainer.objects.create(user=test_user_trainer)
        trainee = Trainee.objects.create(user=test_user, trainer=trainer)
        Trainee.objects.create(user=test_user_2, trainer=trainer)
        WeightMeasurement.objects.create(trainee=trainee, value='80')

    def test_anonymous_user_view_measurements_fail(self):
        """Test that the measurements view fails if the user is not logged in"""
        url = reverse('trainees:allmusermeasurements')
        response = self.client.get(url)
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_measurement_succeed(self):
        """Test that the measurements view succeeds if the user is logged in and is the owner of the measurement"""
        test_user = User.objects.get(username='test_user')

        self.client.force_login(test_user)
        url = reverse('trainees:allmusermeasurements')
        response = self.client.get(url)

        measurements = response.json()
        first_measurement, *_ = measurements

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(first_measurement.get('trainee'), test_user.id)

    def test_owner_view_measurement_detail(self):
        """Test that the measurements detail view succeed if the user is the owner of the measurement"""
        test_user = User.objects.get(username='test_user')

        self.client.force_login(test_user)
        url = reverse('trainees:measurementdetail', kwargs={'pk': 1})
        response = self.client.get(url)

        measurement = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(measurement.get('trainee'), test_user.id)

    def test_not_owner_view_measurement_detail(self):
        """Test that the measurements detail view will return a 403 if the user is not the owner of the measurement"""
        test_user = User.objects.get(username='test_user_2')

        self.client.force_login(test_user)
        url = reverse('trainees:measurementdetail', kwargs={'pk': 1})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_owner_update_measurement_detail(self):
        """Test that the measurements detail update view will return a 200,
         if the user is the owner of the measurement"""

        test_user = User.objects.get(username='test_user')
        test_measurement = WeightMeasurement.objects.get(pk=1)

        self.client.force_login(test_user)
        url = reverse('trainees:measurementdetail', kwargs={'pk': test_measurement.pk})
        response = self.client.put(url, {'trainee': test_user.trainee.pk, 'value': '90'})
        json_response = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response.get('value'), '90')
