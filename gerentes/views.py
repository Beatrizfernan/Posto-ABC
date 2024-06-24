from django.shortcuts import render
from django.http import HttpResponse
from .models import Gerente, Abastecimento
import re
from decimal import Decimal

def gerentes(request):
    if request.method == "GET":
        gerentes_list = Gerente.objects.all()
        return render(request, 'gerentes.html', {'gerentes': gerentes_list})
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        cpf = request.POST.get('cpf')
        abastecimentos = request.POST.getlist('abastecimento')
        tanques = request.POST.getlist('tanque')
        bombas = request.POST.getlist('bomba')
        quantidades = request.POST.getlist('quantidade')
        valores_unitarios = request.POST.getlist('valor')

       
        
        gerente = Gerente.objects.create(
            nome=nome,
            email=email,
            cpf=cpf
        )

        for abastecimento, tanque, bomba, quantidade, valor_unitario in zip(abastecimentos, tanques, bombas, quantidades, valores_unitarios):
    
            quantidade_decimal = Decimal(quantidade.replace(',', '.'))
            valor_unitario_decimal = Decimal(valor_unitario.replace(',', '.'))
            Abastecimento.objects.create(
                abastecimento=abastecimento,
                tanque=tanque,
                bomba=bomba,
                valor_unitario=valor_unitario_decimal,
                quantidade=quantidade_decimal,
                gerente=gerente
            )

        return HttpResponse('Dados salvos com sucesso!')
