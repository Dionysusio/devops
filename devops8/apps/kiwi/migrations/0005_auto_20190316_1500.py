# Generated by Django 2.1.7 on 2019-03-16 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kiwi', '0004_auto_20190316_1455'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='az',
            options={'ordering': ['id'], 'verbose_name': 'AZ', 'verbose_name_plural': 'AZ'},
        ),
        migrations.AlterModelOptions(
            name='function',
            options={'ordering': ['id'], 'verbose_name': '功能大类', 'verbose_name_plural': '功能大类'},
        ),
        migrations.AlterModelOptions(
            name='idc',
            options={'ordering': ['id'], 'verbose_name': 'IDC', 'verbose_name_plural': 'IDC'},
        ),
        migrations.AlterModelOptions(
            name='subfunction',
            options={'ordering': ['id'], 'verbose_name': '功能小类', 'verbose_name_plural': '功能小类'},
        ),
        migrations.AlterField(
            model_name='function',
            name='az',
            field=models.ForeignKey(help_text='所在AZ', on_delete=django.db.models.deletion.CASCADE, related_name='az_fun', to='kiwi.AZ', verbose_name='所在AZ'),
        ),
    ]