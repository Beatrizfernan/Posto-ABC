from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.core import serializers
from .models import Gerente, Abastecimento
import re
from decimal import Decimal
import json
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
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
        valores_unitarios = request.POST.getlist('valor_unitario')

        gerente = Gerente.objects.filter(cpf=cpf).first()
        
        if gerente:
            # Gerente já existe, atualizar informações se necessário
            gerente.nome = nome
            gerente.email = email
            gerente.save()
        else:
            # Criar um novo gerente
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
            Abast = Abastecimento(
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
    gerente = get_object_or_404(Gerente, id=id_gerente)  # Obtém um único objeto Gerente
    abastecimentos = Abastecimento.objects.filter(gerente=gerente)  # Filtra os abastecimentos relacionados ao gerente
    
    # Serializa o objeto Gerente
    gerente_json = json.loads(serializers.serialize('json', [gerente]))[0]['fields']
    gerente_id = json.loads(serializers.serialize('json', [gerente]))[0]['pk']
    
    # Serializa os objetos Abastecimento
    abastecimentos_json = json.loads(serializers.serialize('json', abastecimentos))
    abastecimentos_json = [{'fields': i['fields'], 'id': i['pk']} for i in abastecimentos_json]
    
    # Prepara os dados para resposta
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
    if request.method == 'POST':
        abastecimento_nome = request.POST.get('abastecimento')
        tanque = request.POST.get('tanque')
        bomba = request.POST.get('bomba')
        valor_unitario = request.POST.get('valor_unitario')
        quantidade = request.POST.get('quantidade')

        # Obter o objeto Abastecimento pelo ID
        abastecimento = get_object_or_404(Abastecimento, id=id)

        # Verificar se já existe outro abastecimento com o mesmo nome
        if Abastecimento.objects.exclude(id=id).filter(abastecimento=abastecimento_nome).exists():
            return HttpResponse('Abastecimento já existente', status=400)

        # Atualizar os campos do objeto abastecimento
        abastecimento.abastecimento = abastecimento_nome
        abastecimento.tanque = tanque
        abastecimento.bomba = bomba
        abastecimento.valor_unitario = Decimal(valor_unitario.replace(',', '.')) if valor_unitario else Decimal('0.00')
        abastecimento.quantidade = Decimal(quantidade.replace(',', '.')) if quantidade else Decimal('0.00')

        # Atualizar o valor total com base no valor unitário e na quantidade
        abastecimento.valor_total = abastecimento.valor_unitario * abastecimento.quantidade
        
        # Salvar as alterações
        abastecimento.save()

        return HttpResponse(f'Abastecimento {id} atualizado com sucesso')

    return HttpResponse('Método não permitido', status=405)


def update_gerente(request, id):
    if request.method == 'POST':
        body = json.loads(request.body)
        nome = body.get('nome')
        email = body.get('email')
        cpf = body.get('cpf')

        gerente = get_object_or_404(Gerente, id=id)
        try:
            gerente.nome = nome
            gerente.email = email
            gerente.cpf = cpf
            gerente.save()
            return JsonResponse({'status': '200', 'nome': nome, 'email': email, 'cpf': cpf})
        except Exception as e:
            return JsonResponse({'status': '500', 'error': str(e)})
    return JsonResponse({'status': '405', 'error': 'Método não permitido'})


def gerar_pdf_abastecimentos(request):
    cpf = request.GET.get('cpf')
    
    if not cpf:
        return HttpResponse("CPF não fornecido", status=400)

    gerente = get_object_or_404(Gerente, cpf=cpf)
    abastecimentos = Abastecimento.objects.filter(gerente=gerente)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="abastecimentos_{cpf}.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=A3, rightMargin=30, leftMargin=30, topMargin=30, bottomMargin=30)
    elements = []
    
    styles = getSampleStyleSheet()
    title = Paragraph(f"Relatório de Abastecimentos - Gerente: {gerente.nome}", styles['Title'])
    elements.append(title)
    
    data = [['Data', 'Abastecimento', 'Tanque', 'Bomba', 'Quantidade', 'Valor Unitário', 'Valor Total', 'Imposto (13%)']]
    
    for abastecimento in abastecimentos:
        data.append([
            abastecimento.data_abastecimento.strftime("%d/%m/%Y %H:%M"),
            abastecimento.abastecimento,
            abastecimento.tanque,
            abastecimento.bomba,
            f"{abastecimento.quantidade:.2f}",
            f"R$ {abastecimento.valor_unitario:.2f}",
            f"R$ {abastecimento.valor_total:.2f}",
            f"R$ {(abastecimento.valor_total * Decimal('0.13')):.2f}"
        ])
    
    # Aumentando um pouco a largura das colunas para aproveitar melhor o espaço A3
    col_widths = [100, 110, 90, 90, 110, 110, 110, 110]
    
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    return response