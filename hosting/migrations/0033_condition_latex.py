# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-05 18:45
from __future__ import unicode_literals

from django.db import migrations, models


SYMBOLS = (
    ('dont-smoke', {'latex': r'\faBan'}),
    ('one-room', {'latex': r'\faGroup'}),
    ('sleeping-bag', {'latex': r'\faBed'}),
)

def populate_latex_field(apps, schema_editor):
    Condition = apps.get_model('hosting', 'Condition')
    for slug, symbol in SYMBOLS:
        Condition.objects.update_or_create(slug=slug, defaults=symbol)

def reverse_nothing(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('hosting', '0032_refrazigo'),
    ]

    operations = [
        migrations.AddField(
            model_name='condition',
            name='latex',
            field=models.CharField(default='\\fa', help_text='Latex symbol. E.g.: \\faBan', max_length=20, verbose_name='latex'),
            preserve_default=False,
        ),

        migrations.RunPython(populate_latex_field, reverse_nothing),
    ]
