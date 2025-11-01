from django.urls import path
from finance.views import home
from . import views
from django.shortcuts import redirect

def redirect_to_home(request):
    return redirect('home')

urlpatterns = [
    path('', redirect_to_home),
    path('home/', home, name='home'),
    path('mutasi-bank/', views.mutasi_bank, name='mutasi_bank'),
    path('mutasi-zahir/', views.mutasi_zahir, name='mutasi_zahir'),
    path('laporan/', views.laporan, name='laporan'),
    path('import_data/', views.import_data, name='import_data'),
    path('generate_report_different/', views.generate_report_different, name='generate_report_different'),
]