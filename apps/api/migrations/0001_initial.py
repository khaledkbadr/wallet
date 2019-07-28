# Generated by Django 2.2.3 on 2019-07-25 15:52

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountBalance',
            fields=[
                ('account', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('balance', models.DecimalField(decimal_places=2, max_digits=20, validators=[django.core.validators.MinValueValidator(Decimal('0.0'))])),
                ('currency', models.CharField(default='USD', max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('direction', models.CharField(choices=[('incoming', 'incoming'), ('outgoing', 'outgoing')], max_length=8)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('timestamp', models.DateTimeField()),
                ('primary_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transfers', to='api.AccountBalance')),
                ('secondary_account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.AccountBalance')),
            ],
        ),
    ]
