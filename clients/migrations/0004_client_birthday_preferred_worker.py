from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_alter_client_options_alter_client_email_and_more'),
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='birthday',
            field=models.DateField(
                blank=True, null=True,
                help_text='Used for birthday promotions',
            ),
        ),
        migrations.AddField(
            model_name='client',
            name='preferred_worker',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='preferred_clients',
                to='staff.staffmember',
                help_text='Preferred stylist/worker',
            ),
        ),
    ]
