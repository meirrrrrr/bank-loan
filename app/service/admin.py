from django.contrib import admin

from app.service.models import Program, BlackList


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'min_sum', 'max_sum', 'min_age', 'max_age', 'created_at', 'updated_at'
    )
    fields = (
        'min_sum', 'max_sum', 'min_age', 'max_age'
    )
    ordering = ('id', 'min_sum', 'max_sum', 'min_age', 'max_age', 'created_at', 'updated_at')


@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
    list_display = ('id', 'borrower',)
    fields = ('borrower',)
    ordering = ('id',)
