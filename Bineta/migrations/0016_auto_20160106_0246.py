# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Bineta', '0015_auto_20160103_1047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='level',
            field=models.ForeignKey( default=1, to='Bineta.ClassLevel' ),
        ),
        migrations.AlterField(
            model_name='document',
            name='matter',
            field=models.ForeignKey( default=1, to='Bineta.ClassTopic' ),
        ),
        migrations.AlterField(
            model_name='document',
            name='school',
            field=models.ForeignKey( default=1, to='Bineta.School' ),
        ),
    ]
