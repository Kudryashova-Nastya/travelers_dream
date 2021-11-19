from django.contrib.auth.models import User
from django.db import models


class Agreement(models.Model):
    date = models.DateField()
    organization = models.ForeignKey('Organization', models.DO_NOTHING, db_column='organization')
    country = models.CharField(max_length=64)
    agent = models.ForeignKey('Employee', models.DO_NOTHING, blank=True, null=True)
    client = models.ForeignKey('Client', models.DO_NOTHING)
    number_participants = models.IntegerField()
    date_start = models.DateField()
    date_end = models.DateField()
    cities = models.TextField(db_collation='utf8mb4_bin')

    class Meta:
        managed = False
        db_table = 'agreement'

    def __str__(self):
        return self.id


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField(default=0)
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField(default=1)
    is_active = models.IntegerField(default=1)
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class City(models.Model):
    country = models.CharField(max_length=128)
    city = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'city'

    def __str__(self):
        return self.city


class Client(models.Model):
    fio = models.CharField(max_length=256)
    gender = models.CharField(max_length=1)
    dob = models.DateField()
    place = models.CharField(max_length=256)
    passport_series = models.IntegerField(blank=True, null=True)
    passport_number = models.IntegerField(blank=True, null=True)
    date_issue = models.DateField(blank=True, null=True)
    date_end = models.DateField(blank=True, null=True)
    issued_by = models.CharField(max_length=256, blank=True, null=True)
    international_passport = models.ForeignKey('InternationalPassport', models.DO_NOTHING, blank=True, null=True)
    status = models.ForeignKey('StatusClient', models.DO_NOTHING, db_column='status')
    doc_type = models.CharField(max_length=24, default='Паспорт')
    birth_certificate = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'client'

    def __str__(self):
        return self.fio


class Contract(models.Model):
    date = models.DateField()
    organization = models.ForeignKey('Organization', models.DO_NOTHING, db_column='organization')
    agreement_id = models.IntegerField()
    agent_id = models.IntegerField()
    client_id = models.IntegerField()
    date_start = models.DateField()
    date_end = models.DateField()
    participants = models.TextField(db_collation='utf8mb4_bin')
    sum = models.IntegerField()
    currency = models.ForeignKey('Currency', models.DO_NOTHING, db_column='currency')

    class Meta:
        managed = False
        db_table = 'contract'

    def __str__(self):
        return self.id


class Currency(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=64)
    rate = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'currency'

    def __str__(self):
        return self.name


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Employee(models.Model):
    organization = models.ForeignKey('Organization', models.DO_NOTHING, db_column='organization')
    initials = models.CharField(max_length=64)
    fio = models.CharField(max_length=256)
    dob = models.DateField(blank=True, null=True)
    position = models.ForeignKey('PositionEmployee', models.DO_NOTHING, db_column='position')
    photo = models.CharField(max_length=256, blank=True, null=True)
    user = models.OneToOneField(AuthUser, models.CASCADE, db_column='user', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'employee'

    def __str__(self):
        return self.fio


class Hotel(models.Model):
    city = models.ForeignKey(City, models.DO_NOTHING, db_column='city')
    name = models.CharField(max_length=256)
    stars = models.CharField(max_length=32)
    address = models.CharField(max_length=512)

    class Meta:
        managed = False
        db_table = 'hotel'

    def __str__(self):
        return self.name


class InternationalPassport(models.Model):
    fio = models.CharField(max_length=256)
    gender = models.CharField(max_length=1)
    dob = models.DateField()
    place = models.CharField(max_length=256)
    number = models.IntegerField()
    date_issue = models.DateField()
    date_end = models.DateField()
    issued_by = models.CharField(max_length=256)
    citizenship = models.CharField(max_length=64)
    code = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'international_passport'

    def __str__(self):
        return self.fio


class Organization(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'organization'

    def __str__(self):
        return self.name


class Payment(models.Model):
    date = models.DateField()
    organization = models.IntegerField()
    contract = models.ForeignKey(Contract, models.DO_NOTHING)
    amount_rub = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'payment'

    def __str__(self):
        return self.id


class PositionEmployee(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'position_employee'

    def __str__(self):
        return self.name


class Reservation(models.Model):
    hotel = models.ForeignKey(Hotel, models.DO_NOTHING)
    room_type = models.ForeignKey('RoomType', models.DO_NOTHING, db_column='room_type')
    start = models.DateTimeField()
    end = models.DateTimeField()
    amount = models.IntegerField()
    contract = models.ForeignKey(Contract, models.DO_NOTHING)
    currency = models.IntegerField()
    food = models.CharField(max_length=3)

    class Meta:
        managed = False
        db_table = 'reservation'

    def __str__(self):
        return self.hotel


class RoomType(models.Model):
    type = models.CharField(max_length=32)
    balcony = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'room_type'

    def __str__(self):
        return self.type


class StatusClient(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'status_client'

    def __str__(self):
        return self.name


class Ticket(models.Model):
    contract = models.ForeignKey(Contract, models.DO_NOTHING)
    transport = models.ForeignKey('TransportType', models.DO_NOTHING, db_column='transport')
    travel_card = models.IntegerField()
    transfer = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ticket'

    def __str__(self):
        return self.id


class TransportType(models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'transport_type'

    def __str__(self):
        return self.name
