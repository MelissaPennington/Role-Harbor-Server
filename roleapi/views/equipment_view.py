from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roleapi.models import Equipment


class EquipmentView(ViewSet):
    """equipment view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single piece of equipment.
        Returns: Response -- JSON serialized equipment"""

        try:
            equipment = Equipment.objects.get(pk=pk)
            serializer = EquipmentSerializer(equipment)
            return Response(serializer.data)
        except Equipment.DoesNotExist:
            return Response({'message': 'Equipment not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to get all items.
        Returns: Response -- JSON serialized list of items"""

        try:
            equipments = Equipment.objects.all()
            serializer = EquipmentSerializer(equipments, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EquipmentSerializer(serializers.ModelSerializer):
    """JSON serializer for equipments"""
    class Meta:
        model = Equipment
        fields = ('id', 'name')
        depth = 1
