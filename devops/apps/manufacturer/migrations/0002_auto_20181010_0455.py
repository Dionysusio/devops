# Generated by Django 2.0.9 on 2018-10-10 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('manufacturer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturer',
            name='mail',
            field=models.CharField(help_text='联系邮件', max_length=32, null=True, verbose_name='联系邮件'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='remark',
            field=models.CharField(help_text='备注', max_length=300, null=True, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='tel',
            field=models.CharField(help_text='联系电话', max_length=15, null=True, verbose_name='联系电话'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='vendor_name',
            field=models.CharField(db_index=True, help_text='厂商名称', max_length=32, unique=True, verbose_name='厂商名称'),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='model_name',
            field=models.CharField(help_text='型号名称', max_length=20, verbose_name='型号名称'),
        ),
        migrations.AlterField(
            model_name='productmodel',
            name='vendor',
            field=models.ForeignKey(help_text='所属制造商', on_delete=django.db.models.deletion.CASCADE, to='manufacturer.Manufacturer', verbose_name='所属制造商'),
        ),
    ]
