# Generated by Django 4.0.1 on 2022-02-28 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_account_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(blank=True, max_length=120, null=True, verbose_name='ایمیل'),
        ),
    ]
