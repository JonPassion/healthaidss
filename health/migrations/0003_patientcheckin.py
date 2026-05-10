# Generated manually

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('health', '0002_medicalhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientCheckIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'Active'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='active', max_length=20)),
                ('initial_symptoms', models.TextField(help_text='Symptoms that triggered the check-in')),
                ('last_check_in_time', models.DateTimeField(auto_now=True)),
                ('next_check_in_time', models.DateTimeField()),
                ('check_in_count', models.IntegerField(default=0)),
                ('responses', models.TextField(blank=True, help_text='Patient responses to check-ins')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='check_ins', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
