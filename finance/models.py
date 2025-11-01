from django.db import models

class MutasiZahir(models.Model):
    tanggal = models.DateField()
    ref_code = models.CharField(max_length=10)
    ref_number = models.CharField(max_length=25)
    description = models.CharField(max_length=150)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    kredit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mutasi_zahir'
        verbose_name = 'Mutasi Zahir'
        verbose_name_plural = 'Mutasi Zahir'

    def __str__(self):
        return f"{self.ref_number} - {self.tanggal}"


class MutasiBank(models.Model):
    tanggal = models.DateField()
    description = models.CharField(max_length=150)
    debit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    kredit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mutasi_bank'
        verbose_name = 'Mutasi Bank'
        verbose_name_plural = 'Mutasi Bank'

    def __str__(self):
        return f"{self.tanggal} - {self.description}"
