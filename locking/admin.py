from django.contrib import admin
from .models import Transaction, Lock

class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'status', 'start_time', 'end_time')
    list_filter = ('status', 'start_time')
    search_fields = ('transaction_id',)

class LockAdmin(admin.ModelAdmin):
    list_display = ('seat', 'lock_type', 'transaction_id', 'acquired_at')
    list_filter = ('lock_type', 'transaction_id')
    search_fields = ('resource',)

admin.site.register(Lock, LockAdmin)
admin.site.register(Transaction, TransactionAdmin)
