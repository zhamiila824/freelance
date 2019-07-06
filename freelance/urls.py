from django.contrib import admin
from django.urls import path, include


v1 = ([
    path('', include(('user.urls', 'user'), namespace='user')),
    path('', include(('task.urls', 'task'), namespace='task')),
])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(v1)),
]
