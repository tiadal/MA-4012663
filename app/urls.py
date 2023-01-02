from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    # index.html
    path('', views.homepage, name="homepage"),
    # public survey
    path('survey/', views.picksurvey, name="test-picksurvey"),
    path('survey/<testid>/start/<int:userid>', views.teststart, name="test-start"),
    path('survey/<testid>/<userid>/<int:caseid>', views.testcase, name="test-case"),
    path('survey/<testid>/<userid>/end/', views.testend, name="test-end"),
    # private survey
    path('survey/<testid>/settings/', views.testsettings, name="test-settings"),
    path('survey/<testid>/results/', views.testresults, name="test-results"),
    path('survey/<testid>/delete/', views.testdelete, name="test-delete"),    
    path('create/', views.testcreate, name="test-create"),
    path('reports/<int:reportid>/', views.testfinalresults, name="test-final-results"),
    # general settings for surveys
    path('create/settings/', views.testcreatesettings, name="test-createsettings"),
    path('create/settings/variable/<variableid>/delete', views.settingsvariabledelete, name="test-settingsvariabledelete"),
    path('create/settings/template/<templateid>', views.testtemplateedit, name="test-templateedit"),
    path('create/preview/template/<templateid>', views.templatepreview, name="preview-template"),
    path('create/settings/template/<templateid>/delete', views.testtemplatedelete, name="test-templatedelete"),
    path('create/settings/form/<formid>', views.formedit, name="test-formedit"),
    path('create/settings/form/<formid>/delete', views.formdelete, name="test-formdelete"),
]
