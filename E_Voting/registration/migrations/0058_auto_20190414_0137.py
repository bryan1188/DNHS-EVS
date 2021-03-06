# Generated by Django 2.1.5 on 2019-04-13 17:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('election', '0026_auto_20190414_0137'),
        ('registration', '0057_auto_20190413_2309'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteArchived',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
                ('hashed_id', models.CharField(default='93db77aacd77403c8fd2613eaf3fef2e', max_length=255, unique=True)),
                ('ballot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='votes_archived', to='election.Ballot', verbose_name='Ballot')),
                ('candidate', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='votes_archived', to='registration.Candidate', verbose_name='Candidate')),
            ],
        ),
        migrations.CreateModel(
            name='WinnerCandidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='vote',
            name='hashed_id',
            field=models.CharField(default='72fee4b5385041f8b05aaa4ce10e6e86', max_length=255, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='votearchived',
            unique_together={('ballot', 'candidate')},
        ),
    ]
