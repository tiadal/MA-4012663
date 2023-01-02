from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from user import views as user_views

#for media in dev mode
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # admin
    path('admin/', admin.site.urls),
    # setup section
    path('register/', user_views.register, name="register"),
    path('profile/', user_views.profile, name="profile"),
    path('accounts/profile/', user_views.profile_redirect, name="profile_redirect"),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html', redirect_authenticated_user=True), name="login"), 
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name="logout"),
    # other sections
    path('imprint/', user_views.imprint, name="imprint"),
    # study section
    path('', include(('app.urls', 'app'),namespace='app')),
] 

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'user.views.error_404'
handler500 = 'user.views.error_500'