"""
FaST backend URL configuration
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from graphene_file_upload.django import FileUploadGraphQLView
from django.shortcuts import render
from django.http import HttpResponse


# Health probe for kubernetes
def healthz(request):
    return HttpResponse(status=200)


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # TODO: remove csrf_exempt on graphql
    # We leave the graohiql activated even in prod mode for API demo purposes
    url(r'^graphql', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),

    # This health endpoint is used as a liveness probe by kubernetes
    url(r'^healthz', healthz)
]

# Debug setup for the farmer app PWA
# Just needed when debugging the application
if settings.DEBUG:
    def farmer_mobile_app_debug(request):
        return render(request, 'farmer_mobile_app_debug.html')

    def farmer_mobile_app_embedded_debug(request):
        return render(request, 'farmer_mobile_app_embedded_debug.html')

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [url(r'^farmer_mobile_app_debug/', farmer_mobile_app_debug),
                    url(r'^farmer_mobile_app_embedded_debug/', farmer_mobile_app_embedded_debug)]
