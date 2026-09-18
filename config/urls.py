from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "api/v1/auth/",
        include("apps.accounts.urls"),
    ),

    path(
        "api/v1/organizations/",
        include("apps.organizations.urls"),
    ),
    path(
    "api/v1/teams/",
    include("apps.teams.urls"),
    ),
    path(
    "api/v1/projects/",
    include("apps.projects.urls"),
    ),
    path(
    "api/v1/tasks/",
    include("apps.tasks.urls"),
    ),
    path(
    "api/v1/comments/",
    include("apps.comments.urls"),
    ),

    path(
    "api/v1/attachments/",
    include("apps.attachments.urls"),
    ),
]
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )