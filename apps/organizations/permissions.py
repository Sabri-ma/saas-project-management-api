from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import OrganizationMembership


class IsOrganizationMember(BasePermission):
    """
    User must belong to the object's organization.
    """

    def has_object_permission(self, request, view, obj):
        organization = getattr(obj, "organization", None)

        if organization is None and hasattr(obj, "project"):
            organization = obj.project.organization

        if organization is None and hasattr(obj, "task"):
            organization = obj.task.project.organization

        return OrganizationMembership.objects.filter(
            organization=organization,
            user=request.user,
        ).exists()

from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import OrganizationMembership


class IsOrganizationContributor(BasePermission):
    def has_object_permission(self, request, view, obj):
        organization = getattr(obj, "organization", None)

        if organization is None and hasattr(obj, "project"):
            organization = obj.project.organization

        membership = OrganizationMembership.objects.filter(
            organization=organization,
            user=request.user,
        ).first()

        if membership is None:
            return False

        if request.method in SAFE_METHODS:
            return True

        return membership.role in {
            OrganizationMembership.Role.OWNER,
            OrganizationMembership.Role.ADMIN,
            OrganizationMembership.Role.MEMBER,
        }
class IsOrganizationAdminOrOwner(BasePermission):
    """
    Only OWNER or ADMIN can modify.
    Members/viewers can read.
    """

    def has_object_permission(self, request, view, obj):
        organization = getattr(obj, "organization", None)

        if organization is None and hasattr(obj, "project"):
            organization = obj.project.organization

        if organization is None and hasattr(obj, "task"):
            organization = obj.task.project.organization

        membership = OrganizationMembership.objects.filter(
            organization=organization,
            user=request.user,
        ).first()

        if membership is None:
            return False

        if request.method in SAFE_METHODS:
            return True

        return membership.role in {
            OrganizationMembership.Role.OWNER,
            OrganizationMembership.Role.ADMIN,
        }


class IsOrganizationOwner(BasePermission):
    """
    Only organization owner can perform the action.
    """

    def has_object_permission(self, request, view, obj):
        organization = getattr(obj, "organization", obj)

        return OrganizationMembership.objects.filter(
            organization=organization,
            user=request.user,
            role=OrganizationMembership.Role.OWNER,
        ).exists()
    
def user_can_manage_organization(user, organization):
    return OrganizationMembership.objects.filter(
        organization=organization,
        user=user,
        role__in=[
            OrganizationMembership.Role.OWNER,
            OrganizationMembership.Role.ADMIN,
        ],
    ).exists()