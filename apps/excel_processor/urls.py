from django.urls import path
from . import views

app_name = 'excel_processor'

urlpatterns = [
    # Auth and main pages
    path('', views.login_view, name='login'),
    path('index/', views.index, name='index'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('analytics/', views.analytics, name='analytics'),
    path('logout/', views.logout_view, name='logout'),

    # Admin actions
    path('create-user/', views.create_user, name='create_user'),
    path('toggle-user/', views.toggle_user, name='toggle_user'),
    path('upload-excel/', views.upload_excel, name='upload_excel'),
    path('toggle-excel/', views.toggle_excel, name='toggle_excel'),
    path('delete-excel/', views.delete_excel, name='delete_excel'),
    path('configure-sheets/<int:excel_id>/', views.configure_sheets, name='configure_sheets'),

    # AJAX endpoints
    path('api/get-sheets/', views.get_sheets, name='get_sheets'),
    path('api/get-columns/', views.get_columns, name='get_columns'),  
    path('api/fetch-results/', views.fetch_results, name='fetch_results'),
]
