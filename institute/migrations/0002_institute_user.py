# Generated by Django 4.2.16 on 2024-12-08 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_role'),
        ('institute', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='institute',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='institute', to='users.user'),
            preserve_default=False,
        ),
    ]