# Generated by Django 3.2.5 on 2021-10-24 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInformations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('username', models.CharField(db_index=True, max_length=20, unique=True)),
                ('email', models.CharField(max_length=40, unique=True)),
                ('profile_picture', models.CharField(max_length=100, null=True)),
                ('bio', models.CharField(default='', max_length=200)),
                ('verified', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'user_information',
            },
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('content', models.TextField(null=True)),
                ('file', models.CharField(max_length=100, null=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='postsowner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'post',
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('timestamp', models.CharField(max_length=20)),
                ('text', models.TextField(null=True)),
                ('date', models.CharField(max_length=20, null=True)),
                ('seeing', models.BooleanField(default=False)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'message',
            },
        ),
        migrations.CreateModel(
            name='Conversations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(null=True)),
                ('date', models.CharField(max_length=20, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('seeing', models.BooleanField(default=False)),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='targetchat', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userowner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'conversation',
            },
        ),
        migrations.CreateModel(
            name='ConfirmToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(db_index=True, max_length=100, unique=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='chat.userinformations')),
            ],
            options={
                'db_table': 'confirm_token',
            },
        ),
        migrations.AddIndex(
            model_name='messages',
            index=models.Index(fields=['sender', 'target', 'timestamp'], name='message_sender__c8cdda_idx'),
        ),
        migrations.AddIndex(
            model_name='conversations',
            index=models.Index(fields=['user', 'target', 'create'], name='conversatio_user_id_0a86c9_idx'),
        ),
        migrations.AlterUniqueTogether(
            name='conversations',
            unique_together={('user', 'target')},
        ),
    ]
