from rest_framework import serializers
from rpg_data_provider_app.models import RpgEvents

class RpgEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RpgEvents
        fields = '__all__'

class RequestCreateRpgEventsSerializer(serializers.Serializer):
    hotel_id = serializers.IntegerField(required=True)
    timestamp = serializers.DateTimeField(required=True)
    rpg_status = serializers.IntegerField(required=True)
    room_id = serializers.IntegerField(required=True)
    night_of_stay = serializers.DateField(required=True)

class RequestGetListRpgEventsSerializer(serializers.Serializer):
    hotel_id = serializers.IntegerField(required=False)
    updated__gte = serializers.DateField(required=False)
    updated__lte = serializers.DateField(required=False)
    rpg_status = serializers.IntegerField(required=False)
    room_id = serializers.IntegerField(required=False)
    night_of_stay__gte = serializers.DateField(required=False)
    night_of_stay__lte = serializers.DateField(required=False)
