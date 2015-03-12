# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(max_length=500, null=True, upload_to=b'projectimg/', blank=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='shipping_details',
            field=models.CharField(default=b'0', help_text=b'Select the shipping details for this Product', max_length=10, choices=[(b'0', b'Free'), (b'5', b'5 %'), (b'10', b'10 %'), (b'20', b'20 %')]),
        ),
    ]
