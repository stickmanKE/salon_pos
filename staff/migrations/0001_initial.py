from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('salons', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StaffMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=150)),
                ('role', models.CharField(
                    choices=[
                        ('stylist', 'Stylist'), ('colorist', 'Colorist'),
                        ('nail_tech', 'Nail Technician'), ('aesthetician', 'Aesthetician'),
                        ('manager', 'Manager'), ('receptionist', 'Receptionist'), ('other', 'Other'),
                    ],
                    default='stylist', max_length=50,
                )),
                ('phone', models.CharField(blank=True, max_length=20)),
                ('email', models.EmailField(blank=True)),
                ('status', models.CharField(
                    choices=[('active', 'Active'), ('inactive', 'Inactive'), ('on_leave', 'On Leave')],
                    default='active', max_length=20,
                )),
                ('hire_date', models.DateField(blank=True, null=True)),
                ('commission_rate', models.DecimalField(
                    decimal_places=2, default=0.0,
                    help_text='Commission percentage e.g. 10.00 for 10%', max_digits=5,
                )),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('salon', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='staff', to='salons.salon',
                )),
                ('user', models.OneToOneField(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='staff_profile', to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={
                'verbose_name': 'Staff Member',
                'verbose_name_plural': 'Staff Members',
                'ordering': ['full_name'],
            },
        ),
    ]
