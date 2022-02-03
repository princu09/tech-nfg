from django.contrib import admin
from django.urls import path, include
from t_updates import urls

admin.site.site_header = "Tech NFG By NFG"
admin.site.index_title = "Welcome to Tech NFG"

urlpatterns = [
    path('siteAdminApproveByNFG/', admin.site.urls),
    path('', include('t_updates.urls')),
]