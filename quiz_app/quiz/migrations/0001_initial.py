# Generated migration file for Question model
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('question_type', models.CharField(choices=[('MCQ', 'Multiple Choice'), ('TF', 'True/False')], default='MCQ', max_length=3)),
                ('option_a', models.CharField(blank=True, max_length=255)),
                ('option_b', models.CharField(blank=True, max_length=255)),
                ('option_c', models.CharField(blank=True, max_length=255)),
                ('option_d', models.CharField(blank=True, max_length=255)),
                ('correct_answer', models.CharField(max_length=5)),
                ('order', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['order', 'id'],
            },
        ),
    ]
