from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.core import serializers
from .models import Gerente, Abastecimento
import re
from decimal import Decimal
import json
from django.views.decorators.csrf import csrf_exempt

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

        gerente = Gerente.objects.filter(cpf=cpf)
        
        if gerente.exists():
            return render(request, 'gerentes.html', {'error': 'Gerente já existe', 'nome': nome, 'email': email, 'cpf': cpf, 'abastecimentos': zip(abastecimentos, tanques, bombas, valores_unitarios, quantidades)})

        if not re.fullmatch(re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+'), email):
            return render(request, 'gerentes.html', {'error': 'Email inválido', 'nome': nome, 'email': email, 'cpf': cpf, 'abastecimentos': zip(abastecimentos, tanques, bombas, valores_unitarios, quantidades)})

        gerente = Gerente(
            nome=nome,
            email=email,
            cpf=cpf
        )

        gerente.save()

        for abastecimento, tanque, bomba, quantidade, valor_unitario in zip(abastecimentos, tanques, bombas, quantidades, valores_unitarios):
            quantidade_decimal = Decimal(quantidade.replace(',', '.'))
            valor_unitario_decimal = Decimal(valor_unitario.replace(',', '.'))
            Abast= Abastecimento(
                abastecimento=abastecimento,
                tanque=tanque,
                bomba=bomba,
                valor_unitario=valor_unitario_decimal,
                quantidade=quantidade_decimal,
                gerente=gerente
            )
            Abast.save()

        return HttpResponse('Dados salvos com sucesso!')

def att_gerente(request):
   
        id_gerente = request.POST.get('id_gerente')
        gerente = Gerente.objects.filter(id=id_gerente)
        abastecimentos = Abastecimento.objects.filter(gerente=gerente[0])
        gerente_json = json.loads(serializers.serialize('json', [gerente]))[0]['fields']
        gerente_id = json.loads(serializers.serialize('json', [gerente]))[0]['pk']
        abastecimentos_json = json.loads(serializers.serialize('json', abastecimentos))
        abastecimentos_json = [{'fields': i['fields'], 'id': i['pk']} for i in abastecimentos_json]
        data = {'gerente': gerente_json, 'abastecimentos': abastecimentos_json, 'gerente_id': gerente_id}
        return JsonResponse(data)

def excluir_abastecimento(request, id):
    try:
        abastecimento = Abastecimento.objects.get(id=id)
        
        abastecimento.delete()
        return redirect(reverse('gerentes') + f'?aba=att_gerente&id_gerente={id}')
    except :
        return redirect(reverse('gerentes') + f'?aba=att_gerente&id_gerente={id}')

@csrf_exempt
def update_abastecimento(request, id):
    
        abastecimento = request.POST.get('abastecimento')
        tanque = request.POST.get('tanque')
        bomba = request.POST.get('bomba')
        valor = request.POST.get('valor')
        quantidade = request.POST.get('quantidade')

        abastecimento = Abastecimento.objects.get(id=id)
        list_abastecimentos = Abastecimento.objects.exclude(id=id).filter(abastecimento=abastecimento)
        if list_abastecimentos.exists():
             return HttpResponse('placa já existente')
        
        abastecimento.abastecimento = abastecimento
        abastecimento.tanque = tanque
        abastecimento.bomba = bomba
        abastecimento.valor_unitario = Decimal(valor.replace(',', '.'))
        abastecimento.quantidade = Decimal(quantidade.replace(',', '.'))
        abastecimento.save()

        return HttpResponse(id)

def update_gerente(request, id):
    
        body = json.loads(request.body)

        nome = body['nome']
        email = body['email']
        cpf = body['cpf']

        gerente = get_object_or_404(Gerente, id=id)
        try:
            gerente.nome = nome
            gerente.email = email
            gerente.cpf = cpf
            gerente.save()
            return JsonResponse({'status': '200', 'nome': nome, 'email': email, 'cpf': cpf})
        except Exception as e:
            return JsonResponse({'status': '500'})
