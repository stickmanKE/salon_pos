from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0004_alter_saleitem_item_type_alter_saleitem_quantity'),
        ('staff', '0001_initial'),
    ]

    operations = [
        # Add worker to SaleItem
        migrations.AddField(
            model_name='saleitem',
            name='worker',
            field=models.ForeignKey(
                blank=True, null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='sale_items', to='staff.staffmember',
                help_text='Staff member who performed this service/item',
            ),
        ),

        # Add payment_method to Sale
        migrations.AddField(
            model_name='sale',
            name='payment_method',
            field=models.CharField(
                blank=True,
                choices=[
                    ('cash', 'Cash'), ('mpesa', 'M-Pesa'),
                    ('card', 'Card'), ('mixed', 'Mixed'),
                ],
                default='cash', max_length=10,
            ),
        ),

        # Add discount_amount to Sale
        migrations.AddField(
            model_name='sale',
            name='discount_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),

        # Add notes to Sale
        migrations.AddField(
            model_name='sale',
            name='notes',
            field=models.TextField(blank=True),
        ),

        # Add reference to Payment
        migrations.AddField(
            model_name='payment',
            name='reference',
            field=models.CharField(
                blank=True, max_length=100,
                help_text='M-Pesa code or card ref',
            ),
        ),

        # Add beverage to SaleItem item_type choices
        migrations.AlterField(
            model_name='saleitem',
            name='item_type',
            field=models.CharField(
                choices=[
                    ('service', 'Service'),
                    ('product_sale', 'Product Sale'),
                    ('product_use', 'Product Used'),
                    ('beverage', 'Beverage'),
                ],
                max_length=20,
            ),
        ),
    ]
