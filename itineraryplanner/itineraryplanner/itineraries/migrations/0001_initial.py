# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-07-05 17:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Itinerary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'pending'), (1, 'completed'), (2, 'running'), (3, 'error')], default=0, editable=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ItineraryStep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('method', models.PositiveSmallIntegerField(choices=[(0, 'walk'), (1, 'bus'), (2, 'car'), (3, 'tube')], default=0)),
                ('duration', models.PositiveIntegerField(default=0)),
                ('index', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PlaceOfInterest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('place_id', models.CharField(max_length=255)),
                ('is_hotel', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=255)),
                ('lat', models.DecimalField(decimal_places=10, max_digits=13, verbose_name='latitude')),
                ('lng', models.DecimalField(decimal_places=10, max_digits=13, verbose_name='longitude')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='itinerarystep',
            name='destination',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destination', to='itineraries.PlaceOfInterest', verbose_name='the destination place'),
        ),
        migrations.AddField(
            model_name='itinerarystep',
            name='itinerary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='itineraries.Itinerary'),
        ),
        migrations.AddField(
            model_name='itinerarystep',
            name='origin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='origin', to='itineraries.PlaceOfInterest', verbose_name='the origin place'),
        ),
    ]
