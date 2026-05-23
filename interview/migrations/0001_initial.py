from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id',             models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applicant_name', models.CharField(max_length=255)),
                ('interview_date', models.DateField()),
                ('interview_type', models.CharField(
                    choices=[
                        ('initial',   'Initial Interview'),
                        ('technical', 'Technical Interview'),
                        ('final',     'Final Interview'),
                        ('hr',        'HR Interview'),
                    ],
                    default='initial', max_length=20
                )),
                ('interviewer', models.CharField(max_length=100)),
                ('location',    models.CharField(blank=True, max_length=255)),
                ('result',      models.CharField(
                    choices=[
                        ('pending', 'Pending'),
                        ('passed',  'Passed'),
                        ('failed',  'Failed'),
                        ('no_show', 'No Show'),
                    ],
                    default='pending', max_length=20
                )),
                ('remarks', models.TextField(blank=True)),
            ],
            options={'ordering': ['-interview_date']},
        ),
    ]