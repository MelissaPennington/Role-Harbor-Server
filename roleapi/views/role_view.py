from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from roleapi.models import Role, User, Equipment, Organization, OrganizationRole
from roleapi.views.user_view import UserSerializer
# from rolespapi.views.orgaization_role_view import OrganizationRoleSerializer


class RoleView(ViewSet):
    """role view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single role.
        Returns: Response -- JSON serialized role"""

        try:
            role = Role.objects.get(pk=pk)
            serializer = RoleSerializer(role)
            return Response(serializer.data)
        except Role.DoesNotExist:
            return Response({'message': 'role not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        try:
            user_id = request.query_params.get('userId', None)
            roles = ""

            if user_id is not None and user_id != 'undefined':
                user = User.objects.get(id=user_id)
                roles = Role.objects.filter(user_id=user)
            else:
                roles = Role.objects.all()

            serializer = RoleSerializer(roles, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def create(self, request):
        """Handle POST operations
        Returns Response -- JSON serialized role instance"""
        try:
            user = User.objects.get(id=request.data["user"])
            equipment = Equipment.objects.get(id=request.data["equipment"])

            role = Role.objects.create(
                user=user,
                image=request.data["image"],
                name=request.data["name"],
                description=request.data["description"],
                boss=request.data["boss"],
                equipment=equipment,
            )

            if request.data['organizationRoles']:
                for organization_id in request.data['organizationRoles']:
                    new_organization = Organization.objects.get(
                        id=organization_id)
                    OrganizationRole.objects.create(
                        role=role, organization=new_organization)

            serializer = RoleSerializer(role)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def update(self, request, pk):
        """Handle PUT requests for a role
        Returns: Response -- Empty body with 204 status code"""

        equipment = Equipment.objects.get(id=request.data["equipment"])

        try:
            role = Role.objects.get(pk=pk)
            role.name = request.data["name"]
            role.image = request.data["image"]
            role.description = request.data["description"]
            role.boss = request.data["boss"]
            role.equipment = equipment

            if request.data['organizationRoles']:
                existing_organization_roles = OrganizationRole.objects.all().filter(role=role)
                for organization_role in existing_organization_roles:
                    organization_role.delete()
                for organization_id in request.data['organizationRoles']:
                    new_organization = Organization.objects.get(id=organization_id)
                    OrganizationRole.objects.create(role=role, organization=new_organization)

            role.save()

            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except role.DoesNotExist:
            return Response({'message': 'role not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def destroy(self, request, pk):
        """Handle DELETE requests for an role
        Returns: Response -- Empty body with 204 status code"""

        try:
            role = Role.objects.get(pk=pk)
            role.delete()
            return Response(None, status=status.HTTP_204_NO_CONTENT)
        except role.DoesNotExist:
            return Response({'message': 'role not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Add & Remove role organization

    @action(methods=['post'], detail=True)
    def add_organization_role(self, request, pk, organization_id=None):
        """Post request for a user to add an organization to an role"""
        try:
            # item = Item.objects.get(pk=request.data["item"])
            organization = Organization.objects.get(pk=organization_id)
            role = Role.objects.get(pk=pk)
            existing_organization_roles = OrganizationRole.objects.all().filter(
                organization=organization, role=role)
            if len(existing_organization_roles) > 0:
                return Response({'message': 'Organization already added to role'}, status=status.HTTP_200_OK)
            else:
                OrganizationRole.objects.create(
                    organization=organization, role=role)
                return Response({'message': 'Organization added to role'}, status=status.HTTP_201_CREATED)
        except Organization.DoesNotExist:
            return Response({'error': 'Organization not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Role.DoesNotExist:
            return Response({'error': 'Role not found.'}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=['put'], detail=True)
    def remove_organization_role(self, request, pk):
        """Delete request for a user to remove an organization from a role"""
        try:
            # organizationRole = roleItem.objects.get(pk=request.data.get("role_item"), role__pk=pk)
            role = Role.objects.get(pk=pk)

            organization_id = request.query_params.get('organizationId', None)

            if organization_id is not None:
                organization = Organization.objects.get(id=organization_id)
                organization_role = OrganizationRole.objects.get(
                    organization=organization, role=role)
                organization_role.delete()
                serializer = RoleSerializer(role)
                return Response(serializer.data, status=status.HTTP_200_OK)

        except OrganizationRole.DoesNotExist:
            return Response({'error': 'Role with this organization not found.'}, status=status.HTTP_404_NOT_FOUND)


class OrganizationSerializer(serializers.ModelSerializer):
    """JSON serializer for organizations"""
    class Meta:
        model = Organization
        fields = ('id', 'name')
        depth = 1


class RoleSerializer(serializers.ModelSerializer):
    """JSON serializer for roles"""
    organizations = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ('id', 'organizations', 'user', 'name', 'image', 'description', 'equipment', 'boss')
        depth = 1

    def get_organizations(self, obj):
        organization_roles = OrganizationRole.objects.all().filter(role=obj)
        organization_list = [organization_roles.organization for organization_roles in organization_roles]
        serializer = OrganizationSerializer(organization_list, many=True)

        if len(organization_list) > 0:
            return serializer.data
        else:
            return []
