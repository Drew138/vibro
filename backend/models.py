from django.contrib.auth.models import AbstractUser
from django.contrib import admin
from django.db import models


class City(models.Model):

    class Meta:
        unique_together = ["name", "state"]

    name = models.CharField(max_length=30, unique=True)
    state = models.CharField(max_length=30, blank=True, null=True)


class Company(models.Model):

    name = models.CharField(max_length=50, unique=True)
    nit = models.CharField(max_length=15, unique=True)
    address = models.CharField(max_length=50, blank=True)
    rut_address = models.CharField(max_length=50, blank=True)
    pbx = models.IntegerField(blank=True)
    city = models.ForeignKey(
        City,
        related_name='company',
        to_field="name",
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    rut_city = models.ForeignKey(
        City,
        related_name='ruts',
        to_field="name",
        on_delete=models.SET_NULL,
        blank=True,
        null=True)


class VibroUser(AbstractUser):

    ADMIN = 'admin'
    ENGINEER = 'engineer'
    CLIENT = 'client'
    SUPPORT = 'support'

    USER_CHOICES = [
        (ADMIN, 'Admin'),
        (ENGINEER, 'Engineer'),
        (CLIENT, 'Client'),
        (SUPPORT, 'Support')
    ]

    email = models.EmailField(unique=True)
    phone = models.IntegerField(blank=True, null=True)
    ext = models.IntegerField(blank=True, null=True)
    celphone_one = models.IntegerField(blank=True, null=True)
    celphone_two = models.IntegerField(blank=True, null=True)
    company = models.ForeignKey(
        Company,
        related_name="user",
        to_field="name",
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    user_type = models.CharField(
        max_length=8,
        choices=USER_CHOICES,
        default=CLIENT)


class Profile(models.Model):

    certifications = models.CharField(max_length=50, default='undefined')
    # TODO create a default.jpg
    picture = models.ImageField(upload_to="profile", default='default.jpg')
    user = models.OneToOneField(
        VibroUser,
        related_name='profile',
        on_delete=models.CASCADE)


class Machine(models.Model):

    class Meta:
        unique_together = ["name", "machine_type", "company"]

    identifier = models.IntegerField(blank=True, null=True)
    name = models.CharField(max_length=50)
    machine_type = models.CharField(max_length=50)
    code = models.TextField(blank=True, null=True)
    transmission = models.TextField(blank=True, null=True)
    brand = models.TextField(blank=True, null=True)
    power = models.TextField(blank=True, null=True)
    rpm = models.IntegerField(blank=True, null=True)
    company = models.ForeignKey(
        Company,
        related_name="machines",
        to_field="name",
        on_delete=models.CASCADE)


class Image(models.Model):

    image = models.ImageField(upload_to="machines/images")
    diagram = models.ImageField(upload_to="machines/diagrams")
    machine = models.OneToOneField(
        Machine,
        related_name="images",
        on_delete=models.CASCADE)


class Date(models.Model):

    class Meta:
        unique_together = ['company', 'date']

    date = models.DateTimeField()
    company = models.ForeignKey(
        Company,
        related_name="date",
        on_delete=models.SET_NULL,
        blank=True,
        null=True)


class Measurement(models.Model):

    class Meta:
        unique_together = ['measurement_type', 'date', 'machine']

    # severity
    RED = "red"
    GREEN = 'green'
    YELLOW = 'yellow'
    BLACK = 'black'
    # measurement type
    PRED = 'pred'
    ESP = 'esp'
    TER = 'ter'
    ULT = 'ult'
    AIR = 'air'
    SEVERITY_CHOICES = [
        (RED, 'Red'),
        (GREEN, 'Green'),
        (YELLOW, 'Yellow'),
        (BLACK, 'Black')
    ]
    MEASUREMENT_CHOICES = [
        (PRED, 'Predictivo'),
        (ESP, 'Especial'),
        (TER, 'Termografía'),
        (ULT, 'Ultrasonido'),
        (AIR, 'Aire y Cauldal')
    ]
    severity = models.CharField(
        max_length=6, choices=SEVERITY_CHOICES, default=BLACK)
    date = models.ForeignKey(
        Date,
        related_name="measurements",
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    analysis = models.TextField()
    recomendation = models.TextField()
    revised = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)
    measurement_type = models.CharField(
        max_length=10,
        choices=MEASUREMENT_CHOICES,
        default=PRED)
    machine = models.ForeignKey(
        Machine,
        related_name="measurements",
        on_delete=models.CASCADE)
    engineer_one = models.ForeignKey(
        VibroUser,
        related_name="measurements",
        on_delete=models.SET_NULL,
        blank=True,
        null=True)
    engineer_two = models.ForeignKey(
        VibroUser,
        related_name="measurements_two",
        on_delete=models.SET_NULL,
        blank=True,
        null=True)


class TermoImage(models.Model):

    NORMAL = 'normal'
    TERMAL = 'termal'
    IMAGE_CHOICES = [
        (NORMAL, 'Normal'),
        (TERMAL, 'Termal')
    ]
    measurement = models.ForeignKey(
        Measurement, related_name='termal_image', on_delete=models.CASCADE)
    image_type = models.CharField(
        max_length=15, choices=IMAGE_CHOICES, default='undefined')
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="termals")


class Point(models.Model):

    # position
    VER = 'V'
    HOR = 'H'
    AX = 'A'
    # type
    ACC = 'A'
    VEL = 'V'
    DEZ = 'D'  # Desplazamiento
    ENV = 'E'  # Envolvente
    HFD = 'H'  # HFD

    POSITION_CHOICES = [(VER, 'Vertical'), (HOR, 'Horizontal'), (AX, 'Axial')]
    TYPE_CHOICES = [
        (VEL, 'Velocity'),
        (ACC, 'Acceleration'),
        (DEZ, 'Displacement'),
        (ENV, 'Envol'),
        (HFD, 'HFD')
    ]

    number = models.IntegerField()
    position = models.CharField(
        max_length=1, choices=POSITION_CHOICES, default='undefined')
    point_type = models.CharField(
        max_length=1, choices=TYPE_CHOICES, default='undefined')
    measurement = models.ForeignKey(
        Measurement,
        related_name="point",
        on_delete=models.CASCADE)


class Tendency(models.Model):

    point = models.OneToOneField(
        Point, on_delete=models.CASCADE, primary_key=True)
    value = models.DecimalField(decimal_places=2, max_digits=4)


class Espectra(models.Model):

    identifier = models.IntegerField()
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=2, max_digits=4)


class TimeSignal(models.Model):

    identifier = models.IntegerField()
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    value = models.DecimalField(decimal_places=2, max_digits=4)
