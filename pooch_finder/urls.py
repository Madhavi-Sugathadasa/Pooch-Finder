from django.urls import path
from django.conf import settings
from django.conf.urls.static import static




from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("register", views.register_view, name="register"),
    path("logout", views.logout_view, name="logout"),
    path("post_ad", views.post_ad, name="post_ad"),
    path("<int:ad_id>", views.ad_more_details, name="ad_more_details"),
    path("my_ads", views.view_my_ads, name="my_ads"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

