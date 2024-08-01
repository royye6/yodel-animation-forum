from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('chat.urls')),
    # path('', include('content.urls')),
    path('', include('core.urls')),
    # path('', include('users.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
]
