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
    path("autocomplete_location", views.autocomplete_location, name="autocomplete_location"),
    path("edit_ad/<int:ad_id>", views.edit_ad, name="edit_ad"),
    path("send_message", views.send_message, name="send_message"),
    path("delete_pic/<int:ad_id>/<int:pic_id>", views.delete_pic, name="delete_pic"),
    path("forgot_password", PasswordResetView.as_view(), name="forgot_password"),
    path("password_reset_confirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

