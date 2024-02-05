from django.contrib import admin
from django.urls import path, include
from ninja_extra import NinjaExtraAPI, api_controller
from api_ninja.views import router as account_router
from ninja_jwt.controller import NinjaJWTDefaultController
from django.conf import settings
from django.conf.urls.static import static

api = NinjaExtraAPI()
api.add_router('/account/', account_router)

api.register_controllers(NinjaJWTDefaultController)


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
    # path('summernote/', include('django_summernote.urls')),
    #
    # path('', include('home.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
