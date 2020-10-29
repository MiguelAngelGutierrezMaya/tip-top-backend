"""tip_top_backend URL Configuration"""

# Django
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, re_path


admin.site.site_header = 'API Tip-Top Systems'
admin.site.site_title = 'Administration'
admin.site.index_title = 'API Tip-Top Systems Administration'
admin.autodiscover()

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path('', include(('tip_top_backend.users.urls', 'users'), namespace='users')),
    path('', include(('tip_top_backend.levels.urls', 'levels'), namespace='levels')),
    path('', include(('tip_top_backend.units.urls', 'units'), namespace='units')),
    path('', include(('tip_top_backend.materials.urls', 'materials'), namespace='materials')),
    path('', include(('tip_top_backend.lessons.urls', 'lessons'), namespace='lessons')),
    path('', include(('tip_top_backend.roles.urls', 'roles'), namespace='roles')),
    path('', include(('tip_top_backend.documents.urls', 'documents'), namespace='documents')),
    path('', include(('tip_top_backend.cities.urls', 'cities'), namespace='cities')),
    path('', include(('tip_top_backend.classes.urls', 'classes'), namespace='classes')),
    path('', include(('tip_top_backend.students.urls', 'students'), namespace='students')),
    path('', include(('tip_top_backend.student_classes.urls', 'student_classes'), namespace='student_classes')),
    path('', include(('tip_top_backend.memos.urls', 'memos'), namespace='memos')),
    path('', include(('tip_top_backend.notifications.urls', 'notifications'), namespace='notifications')),
    # re_path(r'^\.well-known/', include('letsencrypt.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
