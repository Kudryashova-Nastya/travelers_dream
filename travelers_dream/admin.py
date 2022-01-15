from django.contrib import admin

from .models import Agreement, City, Client, Contract, Currency, Employee, Hotel, InternationalPassport, Organization, \
    Activity
from .models import Payment, PositionEmployee, Reservation, RoomType, StatusClient, Ticket, TransportType


class AgreementAdmin(admin.ModelAdmin):
    list_display = ('date', 'agent', 'client', 'country')

class ClientAdmin(admin.ModelAdmin):
    list_display = ('fio', 'gender', 'dob')

class ContractAdmin(admin.ModelAdmin):
    list_display = ('date', 'client_id', 'sum', 'organization')

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('fio', 'position', 'dob', 'organization')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'room_type', 'start', 'end', 'amount')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('transport', 'contract', 'transfer')

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'date', 'time', 'day_activity', 'night_activity')


admin.site.register(Agreement, AgreementAdmin)
admin.site.register(City)
admin.site.register(Client, ClientAdmin)
admin.site.register(Contract, ContractAdmin)
admin.site.register(Currency)
admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Hotel)
admin.site.register(InternationalPassport)
admin.site.register(Organization)
admin.site.register(Payment)
admin.site.register(PositionEmployee)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(RoomType)
admin.site.register(StatusClient)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(TransportType)
admin.site.register(Activity)
