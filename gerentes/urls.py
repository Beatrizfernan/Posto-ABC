from django.urls import path 
from . import views

urlpatterns = [
    path('', views.gerentes, name='gerentes'),
    path('atualiza_gerente/', views.att_gerente, name="atualiza_gerente"),
    path('excluir_abastecimento/<int:id>', views.excluir_abastecimento, name="excluir_abastecimento"),
    path('update_abastecimento/<int:id>', views.update_abastecimento, name="update_abastecimento"),
    path('update_gerente/<int:id>', views.update_gerente, name="update_gerente"),
]


