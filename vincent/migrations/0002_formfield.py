# Generated by Django 4.1.3 on 2022-11-16 04:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('vincent', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_type', models.IntegerField(blank=True, choices=[(1, 'Text'), (2, 'Textarea'), (3, 'Number'), (4, 'Select'), (5, 'Checkbox'), (6, 'Radio')], default=1, verbose_name='Field Type')),
                ('label', models.CharField(help_text='Define a label', max_length=255, verbose_name='Label')),
                ('placeholder', models.CharField(blank=True, help_text='Add a placeholder if needed', max_length=255, null=True, verbose_name='Placeholder')),
                ('required', models.BooleanField(blank=True, default=False, verbose_name='Is Field Required?')),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vincent.form', verbose_name='Form')),
            ],
            options={
                'verbose_name': 'Form Field',
                'verbose_name_plural': 'Form Fields',
            },
        ),
    ]
