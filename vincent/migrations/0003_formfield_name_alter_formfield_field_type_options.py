# Generated by Django 4.1.3 on 2022-11-17 01:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vincent', '0002_formfield'),
    ]

    operations = [
        migrations.AddField(
            model_name='formfield',
            name='name',
            field=models.CharField(blank=True, max_length=500, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='formfield',
            name='field_type',
            field=models.IntegerField(blank=True, choices=[(1, 'Text'), (2, 'Textarea'), (3, 'Number'), (4, 'Dropdown'), (5, 'Checkbox'), (6, 'Radio'), (7, 'Email'), (8, 'Date'), (9, 'Time')], default=1, verbose_name='Field Type'),
        ),
        migrations.CreateModel(
            name='Options',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Option Name', max_length=255, verbose_name='Name')),
                ('order', models.IntegerField(blank=True, default=1, verbose_name='Order')),
                ('field', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='vincent.formfield', verbose_name='Field')),
            ],
            options={
                'verbose_name': 'Option',
                'verbose_name_plural': 'Options',
                'ordering': ['-order'],
            },
        ),
    ]
