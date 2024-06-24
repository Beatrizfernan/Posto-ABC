from django.db import models
from decimal import Decimal

class Gerente(models.Model):
    nome = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    cpf = models.CharField(max_length=12)

    def __str__(self) -> str:
        return self.nome

class Abastecimento(models.Model):
    abastecimento = models.CharField(max_length=50)
    tanque = models.CharField(max_length=50)
    bomba = models.CharField(max_length=50)
    valor_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    quantidade = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    gerente = models.ForeignKey(Gerente, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.valor_total = self.valor_unitario * self.quantidade
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.abastecimento
