from django.urls import path
from . import views

urlpatterns = [
    path('importar-pdf/', views.importar_pdf, name='importar_pdf'),
    path('import-success/', views.import_success, name='import_success'),
    path('pdf-to-html/', views.pdf_to_html, name='pdf_to_html'),
    path('materiasf/<str:codcarrera>', views.get_materiasf, name='get_materiasf'),
    path('menu', views.menu, name='menu'),
]
