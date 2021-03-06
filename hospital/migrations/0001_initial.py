# Generated by Django 3.2.6 on 2022-07-13 02:52

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import hospital.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=20, unique=True, validators=[hospital.models.validarRut])),
                ('first_name', models.CharField(max_length=20, validators=[hospital.models.validarLetras])),
                ('last_name', models.CharField(max_length=20, validators=[hospital.models.validarLetras])),
                ('password', models.CharField(max_length=20, unique=True, validators=[hospital.models.validarContraseña])),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='PatientReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patientId', models.PositiveIntegerField(null=True)),
                ('assignedDoctorId', models.PositiveIntegerField(null=True)),
                ('patientName', models.CharField(max_length=40)),
                ('email', models.CharField(max_length=60)),
                ('Type', models.CharField(max_length=100, null=True)),
                ('reportGenerado', models.CharField(max_length=20, null=True)),
                ('Gmi', models.FloatField()),
                ('GlucosaPromedio', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, upload_to='profile_pic/PatientProfilePic/')),
                ('email', models.CharField(max_length=60, validators=[hospital.models.validarEmail])),
                ('Type', models.CharField(choices=[('Elegir tipo de diabetes', 'Elegir tipo de diabetes'), ('Diabetes tipo 1', 'Diabetes tipo 1'), ('Diabetes tipo 2', 'Diabetes tipo 2'), ('Diabetes gestacional', 'Diabetes gestacional')], default=('Elegir tipo de diabetes', 'Elegir tipo de diabetes'), max_length=100, validators=[hospital.models.validarOpcion])),
                ('assignedDoctorId', models.PositiveIntegerField(null=True)),
                ('status', models.BooleanField(default=False)),
                ('libreview_email', models.CharField(max_length=60)),
                ('libreview_password', models.CharField(max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(upload_to='profile_pic/DoctorProfilePic/')),
                ('email', models.CharField(max_length=60, validators=[hospital.models.validarEmail])),
                ('status', models.BooleanField(default=False)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
