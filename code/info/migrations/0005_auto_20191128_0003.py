# Generated by Django 2.2.5 on 2019-11-28 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0004_auto_20191127_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='email',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='email',
            name='entity',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='info.Entity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entity',
            name='name',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='entity',
            name='raw_entity',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='info.RawEntity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='phone',
            name='entity',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='info.Entity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='phone',
            name='is_mobile',
            field=models.BooleanField(default=None),
        ),
        migrations.AddField(
            model_name='phone',
            name='phone',
            field=models.CharField(default='', max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='available_from',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='available_to',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='service',
            name='entity',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='info.Entity'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='is_main',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='service',
            name='name',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
