from django.db import models
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


def iin_to_birtdate(iin):
    birthdate = datetime.strptime(iin[:6], '%y%m%d').date()
    return birthdate


class Program(models.Model):
    min_sum = models.FloatField()
    max_sum = models.FloatField()
    min_age = models.IntegerField()
    max_age = models.IntegerField()
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name = 'Программа'
        verbose_name_plural = 'Программы'

    def __str__(self):
        return 'id: {}'.format(self.pk)


class Borrower(models.Model):
    iin = models.CharField(max_length=12)
    birthdate = models.DateField(blank=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name = 'Заемщик'
        verbose_name_plural = 'Заемщики'

    def save(self, *args, **kwargs):
        self.birthdate = iin_to_birtdate(self.iin)
        return super().save(*args, **kwargs)

    def __str__(self):
        return 'ИИН: {}'.format(self.iin)

    @property
    def age(self):
        today = date.today()
        age = relativedelta(today, self.birthdate).years
        return age


class Application(models.Model):
    SUCCESS = 'Одобрено'
    FAILURE = 'Отказано'
    STATUSES = (
        (SUCCESS, SUCCESS),
        (FAILURE, FAILURE)
    )
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    sum = models.FloatField()
    status = models.CharField(max_length=8 ,choices=STATUSES)
    reject_reason = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def __str__(self):
        return 'Заявка для {}'.format(self.borrower)


class BlackList(models.Model):
    borrower = models.ForeignKey(Borrower, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(blank=True, null=True, auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name = 'Черный список'
        verbose_name_plural = 'Черный список'
