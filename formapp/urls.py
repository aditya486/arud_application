from django.urls import path, include
from . import views
# from django.contrib.auth.urls import views as auth_views

app_name = 'formapp'

urlpatterns = [
    path('', views.Information, name='info'),
    path('login/', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path('delete/(int:<id>)', views.delete, name='employee_delete'),
    path('update/<int:id>/', views.UpdateView, name='update'),
    path('password/<int:id>',
         views.password_change_view, name='change_password'),
    path('html_to_pdf_view/<int:id>',
         views.html_to_pdf_view, name="html_to_pdf_view"),
    path('csv_view/(<int:id>)', views.csv_view, name='csv_view'),
    path('show', views.show, name="show"),
    # path('edit/(<int:id>)', views.edit, name='employee_edit'),
    path('view_profile/(<int:id>)',
         views.view_profile, name="view_profile"),




    # path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
