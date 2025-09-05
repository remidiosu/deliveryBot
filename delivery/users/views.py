from django.shortcuts import render
from users.models import Courier, Controller
from users.serials import ControllerSerializer, CourierSerializer
from users.permissions import BotSharedSecretPermission
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class RegisterCourierView(APIView):
    def post(self, request):
        serializer = CourierSerializer(data=request.data)
        if serializer.is_valid():
            courier = serializer.save()
            return Response(CourierSerializer(courier).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RegisterControllerView(APIView):
    def post(self, request):
        serializer = ControllerSerializer(data=request.data)
        if serializer.is_valid():
            controller = serializer.save()
            return Response(ControllerSerializer(controller).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyUserView(APIView):
    def get(self, request):
        telegram_id = request.query_params.get("telegram_id")
        if not telegram_id:
            return Response({"error": "telegram_id required"}, status=400)

        courier = Courier.objects.filter(telegram_id=telegram_id).first()
        if courier:
            return Response({"registered": True, "role": "курьер"})
        
        controller = Controller.objects.filter(telegram_id=telegram_id).first()
        if controller:
            return Response({"registered": True, "role": "админ"})

        return Response({"registered": False})


class FetchUserView(APIView):
    def get(self, request):
        telegram_id = request.data.get('telegram_id')
        if not telegram_id:
            return Response({"error": "telegram_id required"}, status=400)

        courier = Courier.objects.filter(telegram_id=telegram_id).first()
        if courier:
            profile = {
                "role": "курьер", 
                "full_name": courier.full_name, 
                "phone_number": courier.phone_number, 
            }
            return Response(profile)
        
        controller = Controller.objects.filter(telegram_id=telegram_id).first()
        if controller:
            profile = {
                "role": "админ", 
                "full_name": controller.full_name, 
                "phone_number": controller.phone_number, 
            }
            return Response(profile)

        return Response({"registered": False})
    

class UpdateCourierView(APIView):
    def patch(self, request):
        tg_id = request.data.get('telegram_id')
        if not tg_id:
            return Response({"error": "telegram_id required"}, status=status.HTTP_400_BAD_REQUEST)

        courier = Courier.objects.filter(telegram_id=tg_id).first()
        if courier:
            return Response({"error": "Courier not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourierSerializer(courier, data=request.data, partial=True)
        if serializer.is_valid():
            updated = serializer.save()
            return Response(CourierSerializer(updated).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateControllerView(APIView):
    def patch(self, request):
        tg_id = request.data.get('telegram_id')
        if not tg_id:
            return Response({"error": "telegram_id required"}, status=status.HTTP_400_BAD_REQUEST)

        controller = Controller.objects.filter(telegram_id=tg_id).first()
        if controller:
            return Response({"error": "Admin not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ControllerSerializer(controller, data=request.data, partial=True)
        if serializer.is_valid():
            updated = serializer.save()
            return Response(CourierSerializer(updated).data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    