from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .serializers import RequestCreateRpgEventsSerializer, RequestGetListRpgEventsSerializer, RpgEventsSerializer
from rpg_data_provider_app.models import RpgEvents
from django.db import transaction
from django.db.models import Q
import sys
import uuid

class RpgEventsViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        request_body=RequestCreateRpgEventsSerializer,
        responses={
            200: 'Successfully Insert',
            400: 'Bad Request',
            500: 'Server Error'
        }
    )
    @action(detail=False, methods=['post'])
    def create_events(self, request):
        payload = RequestCreateRpgEventsSerializer(data=request.data)
        if not payload.is_valid():
            output = {'success': 'FAILED', 'data': None, 'message': payload.error_messages, 'error': payload.errors}
            return Response(output, status=status.HTTP_400_BAD_REQUEST)

        validated_payload = payload.validated_data
        try:
            with transaction.atomic():
                duplicate_rpg_events = RpgEvents.objects.filter(
                    ~Q(rpg_status=2),
                    hotel_id=validated_payload.get('hotel_id'),
                    room_id=validated_payload.get('room_id'),
                    night_of_stay=validated_payload.get('night_of_stay')
                ).first()
                
                if duplicate_rpg_events:
                    output = {'success': 'FAILED', 'data': None, 'message': 'DUPLICATE_BOOKING', 'error': None}
                    return Response(output, status=status.HTTP_400_BAD_REQUEST)

                RpgEvents.objects.create(
                    id = uuid.uuid4(),
                    updated_at=validated_payload.get('timestamp'),
                    hotel_id=validated_payload.get('hotel_id'),
                    room_id=validated_payload.get('room_id'),
                    rpg_status=validated_payload.get('rpg_status'),
                    night_of_stay=validated_payload.get('night_of_stay')
                )
            
            output = {'success': 'SUCCESS', 'data': validated_payload, 'message': 'Successfully Inserted', 'error': None}
            return Response(output, status=status.HTTP_200_OK)
        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            error_message = "{}:{}".format(filename, line_number)

            output = {'success': 'ERROR', 'data': None, 'message': error_message, 'error': str(e)}
            return Response(output, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('hotel_id', openapi.IN_QUERY, description="Hotel ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('room_id', openapi.IN_QUERY, description="Room ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('updated__gte', openapi.IN_QUERY, description="Updated At Greater Than or Equal", type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('updated__lte', openapi.IN_QUERY, description="Updated At Less Than or Equal", type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('rpg_status', openapi.IN_QUERY, description="RPG Status", type=openapi.TYPE_INTEGER),
            openapi.Parameter('night_of_stay__gte', openapi.IN_QUERY, description="Night of Stay Greater Than or Equal", type=openapi.TYPE_STRING, format='date'),
            openapi.Parameter('night_of_stay__lte', openapi.IN_QUERY, description="Night of Stay Less Than or Equal", type=openapi.TYPE_STRING, format='date')
        ],
        responses={
            200: 'Successfully Retrieved',
            400: 'Bad Request',
            500: 'Server Error'
        }
    )
    @action(detail=False, methods=['get'])
    def list_events(self, request):
        payload = RequestGetListRpgEventsSerializer(data=request.query_params)
        if not payload.is_valid():
            output = {'success': 'FAILED', 'data': None, 'message': payload.error_messages, 'error': payload.errors}
            return Response(output, status=status.HTTP_400_BAD_REQUEST)

        validated_payload = payload.validated_data
        try:
            rpg_events = RpgEvents.objects.filter()

            if validated_payload.get('hotel_id'):
                rpg_events = rpg_events.filter(hotel_id=validated_payload.get('hotel_id'))

            if validated_payload.get('updated__gte'):
                rpg_events = rpg_events.filter(updated_at__gte=validated_payload.get('updated__gte'))

            if validated_payload.get('updated__lte'):
                rpg_events = rpg_events.filter(updated_at__lte=validated_payload.get('updated__lte'))

            if validated_payload.get('rpg_status'):
                rpg_events = rpg_events.filter(rpg_status=validated_payload.get('rpg_status'))

            if validated_payload.get('room_id'):
                rpg_events = rpg_events.filter(room_id=validated_payload.get('room_id'))

            if validated_payload.get('night_of_stay__gte'):
                rpg_events = rpg_events.filter(night_of_stay__gte=validated_payload.get('night_of_stay__gte'))

            if validated_payload.get('night_of_stay__lte'):
                rpg_events = rpg_events.filter(night_of_stay__lte=validated_payload.get('night_of_stay__lte'))

            rpg_events = rpg_events.order_by('updated_at')

            data_output = RpgEventsSerializer(rpg_events, many=True).data
        
            output = {'success': 'SUCCESS', 'data': data_output, 'message': 'Successfully Retrieved', 'error': None}
            return Response(output, status=status.HTTP_200_OK)
        except Exception as e:
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            error_message = "{}:{}".format(filename, line_number)

            output = {'success': 'ERROR', 'data': None, 'message': error_message, 'error': str(e)}
            return Response(output, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
