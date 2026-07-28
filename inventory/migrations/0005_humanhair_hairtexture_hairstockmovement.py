from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_alter_product_unit_type'),
        ('salons', '0001_initial'),
    ]

    operations = [

        # 1. Add updated_at to Product
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),

        # 2. Fix Product ordering
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at']},
        ),

        # 3. Create HairTexture
        migrations.CreateModel(
            name='HairTexture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('salon', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='hair_textures',
                    to='salons.salon',
                )),
            ],
            options={'ordering': ['name']},
        ),

        # 4. Create HumanHair
        migrations.CreateModel(
            name='HumanHair',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255,
                    help_text='Auto-filled if left blank e.g. "Brazilian Body Wave 18 inch"')),
                ('origin', models.CharField(
                    choices=[
                        ('brazilian',  'Brazilian'),
                        ('peruvian',   'Peruvian'),
                        ('malaysian',  'Malaysian'),
                        ('indian',     'Indian'),
                        ('cambodian',  'Cambodian'),
                        ('vietnamese', 'Vietnamese'),
                        ('mongolian',  'Mongolian'),
                        ('burmese',    'Burmese'),
                        ('other',      'Other'),
                    ],
                    default='brazilian', max_length=20,
                )),
                ('length_inch', models.PositiveIntegerField(help_text='Length in inches e.g. 10, 12, 14, 16, 18, 20, 22, 24')),
                ('cost_price', models.DecimalField(decimal_places=2, default=0, max_digits=10,
                    help_text='What you paid per bundle')),
                ('selling_price', models.DecimalField(decimal_places=2, max_digits=10,
                    help_text='What you charge the client per bundle')),
                ('bundles_in_stock', models.PositiveIntegerField(default=0)),
                ('low_stock_alert', models.PositiveIntegerField(default=2,
                    help_text='Alert when bundles fall below this number')),
                ('is_active', models.BooleanField(default=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('salon', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='human_hair',
                    to='salons.salon',
                )),
                ('texture', models.ForeignKey(
                    blank=True, null=True,
                    on_delete=django.db.models.deletion.SET_NULL,
                    related_name='hair_items',
                    to='inventory.hairtexture',
                )),
            ],
            options={
                'verbose_name': 'Human Hair',
                'verbose_name_plural': 'Human Hair Stock',
                'ordering': ['origin', 'texture__name', 'length_inch'],
            },
        ),

        # 5. Create HairStockMovement
        migrations.CreateModel(
            name='HairStockMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bundles', models.PositiveIntegerField(help_text='Number of bundles')),
                ('movement_type', models.CharField(
                    choices=[('in', 'Stock In (Restock)'), ('out', 'Stock Out (Sold)')],
                    max_length=10,
                )),
                ('source', models.CharField(
                    choices=[
                        ('sale',       'Sold to Client'),
                        ('purchase',   'Purchased / Restocked'),
                        ('adjustment', 'Stock Adjustment'),
                        ('returned',   'Returned by Client'),
                    ],
                    max_length=20,
                )),
                ('reference', models.CharField(blank=True, max_length=255,
                    help_text='e.g. Sale #12, supplier invoice number')),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hair', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='movements',
                    to='inventory.humanhair',
                )),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
