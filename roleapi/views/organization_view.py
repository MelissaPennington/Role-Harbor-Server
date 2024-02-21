from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from roleapi.models import Organization

class OrganizationView(ViewSet):
    """organization view"""

    def retrieve(self, request, pk):
        """Handle GET requests for a single organization.
        Returns: Response -- JSON serialized organization"""

        try:
            organization = Organization.objects.get(pk=pk)
            serializer = OrganizationSerializer(organization)
            return Response(serializer.data)
        except Organization.DoesNotExist: 
            return Response({'message': 'Organization not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to get all organizations.
        Returns: Response -- JSON serialized list of organizations"""

        try:
            organizations = Organization.objects.all()
            serializer = OrganizationSerializer(organizations, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrganizationSerializer(serializers.ModelSerializer):
    """JSON serializer for organizations"""
    class Meta:
        model = Organization
        fields = ('id', 'name')
        depth = 1
