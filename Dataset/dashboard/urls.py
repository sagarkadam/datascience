from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),
    path('about-us/', views.AboutUsView.as_view(), name='about'),
    path('privacy', views.PrivacyView.as_view(), name='privacy'),
    path('thanks', views.ThanksView.as_view(), name='thanks'),
    path('datasets/', views.DatasetProfileList.as_view(), name='datasets'),

    #DataScience_FAQ
    path('datascience_faq', views.DataScience_FAQ.as_view(), name='datascience_faq'),

    path('datascience_faq/<str:faq_value>/', views.DataScience_FAQ_Url.as_view(), name='datascience_faq_url'),

    path('submit/', views.DatasetCreate.as_view(), name='submit'),

    #dataset_review
    path('dataset_review/<int:pk>/', views.dataset_review.as_view(), name='dataset_review'),

    path('admin_panel/', views.AdminPanelView.as_view(), name='admin_panel'),

    path('admin_panel/<str:url_value>/', views.AdminPanelViewURl.as_view(), name='admin_panel_url'),
    #demo_user_login
    path('dashboard_panel/', views.dashboard_panel.as_view(), name='dashboard_panel'),

    path('datasets_panel/', views.datasets_panel.as_view(), name='datasets_panel'),
    #search
    url('^search/$', views.search.as_view(), name='search'),

    #filter_data
    path('filter_data/', views.filter_data.as_view(), name='filter_data'),

    #sort_data
    path('sort_data/', views.sort_data.as_view(), name='sort_data'),

    url('ds_treasure/$', views.ds_treasure.as_view(), name='ds_treasure'),

    url('ml_5w1h/$', views.ml_5w1h.as_view(), name='ml_5w1h'),

]