# Generated by Django 4.2.6 on 2023-10-27 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tikect', '0007_rename_content_review_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.CharField(choices=[('0', '☆☆☆☆☆'), ('1', '⭐☆☆☆☆'), ('2', '⭐⭐☆☆☆'), ('3', '⭐⭐⭐☆☆'), ('4', '⭐⭐⭐⭐☆'), ('5', '⭐⭐⭐⭐⭐')], default=None, max_length=10),
        ),
    ]
