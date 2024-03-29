# Generated by Django 4.1.3 on 2023-04-18 22:04

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_remove_profile_following_remove_profile_followers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SemanticTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('wikidata_id', models.CharField(max_length=25, unique=True)),
                ('label', models.CharField(max_length=200, unique=True)),
                ('description', models.CharField(max_length=500, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='post',
            name='semantic_tags',
            field=models.ManyToManyField(default=None, related_name='posts', to='core.semantictag'),
        ),
    ]
