# Generated by Django 3.2.9 on 2021-12-05 14:13

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('caretaker', '0003_alter_care_taker_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='AWT_Device',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_no', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='AutisticChildren',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('child_name', models.CharField(max_length=100)),
                ('Emergency_contact_name', models.CharField(max_length=100)),
                ('Emergency_contact_phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, region=None, verbose_name='Phone number')),
                ('Emergency_contact_address', models.CharField(max_length=100)),
                ('AWT_device_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='device', to='caretaker.awt_device')),
                ('caretaker_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='caretaker', to='caretaker.care_taker')),
            ],
        ),
        # migrations.AddField(
        #     model_name='care_taker',
        #     name='child_id',
        #     field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='caretaker.autisticchildren'),
        #     preserve_default=False,
        # ),
    ]
