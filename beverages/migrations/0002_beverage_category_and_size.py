from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('beverages', '0001_initial'),
        ('salons', '0001_initial'),
    ]

    operations = [
        # 1. Create BeverageCategory
        migrations.CreateModel(
            name='BeverageCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('salon', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE,
                    related_name='beverage_categories', to='salons.salon',
                )),
            ],
            options={
                'verbose_name': 'Beverage Category',
                'verbose_name_plural': 'Beverage Categories',
                'ordering': ['name'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='beveragecategory',
            unique_together={('salon', 'name')},
        ),

        # 2. Add category FK to Beverage (nullable first)
        migrations.AddField(
            model_name='beverage',
            name='category',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='beverages', to='beverages.beveragecategory',
            ),
        ),

        # 3. Add size field
        migrations.AddField(
            model_name='beverage',
            name='size',
            field=models.CharField(
                choices=[
                    ('200ml', '200ml'), ('300ml', '300ml'), ('500ml', '500ml'),
                    ('1000ml', '1 Litre'), ('2000ml', '2 Litres'), ('other', 'Other'),
                ],
                default='500ml', max_length=20,
            ),
        ),

        # 4. Add low_stock_threshold
        migrations.AddField(
            model_name='beverage',
            name='low_stock_threshold',
            field=models.IntegerField(default=5, help_text='Alert when stock falls below this'),
        ),

        # 5. Add updated_at
        migrations.AddField(
            model_name='beverage',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
