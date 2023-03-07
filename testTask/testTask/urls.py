from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users_logic.urls')),
    path('data/', include('data.urls'))
]
