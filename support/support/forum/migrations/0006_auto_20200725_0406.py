# Generated by Django 3.0.8 on 2020-07-24 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20200725_0401'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='category',
            field=models.CharField(choices=[
                ('General Development', 'General Development'),
                ('Web Development', 'Web Development'),
                ('CS', 'Computer Science'),
                ('About DomeCode', 'About DomeCode')
            ],
                                   default='GEN',
                                   max_length=30),
        ),
    ]
