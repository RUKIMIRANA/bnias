from django.contrib import admin
from .models import (
    Citizen,
    Colline,
    Commune,
    LostIdCardReport,
    Province,
    Publication,
    RegisteredIdCard,
    RegisteredIdCardApplication,
    Service,
)

# Register your models here.
admin.site.register(Citizen)
admin.site.register(Colline)
admin.site.register(Commune)
admin.site.register(LostIdCardReport)
admin.site.register(Province)
admin.site.register(Publication)
admin.site.register(RegisteredIdCard)
admin.site.register(RegisteredIdCardApplication)
admin.site.register(Service)
