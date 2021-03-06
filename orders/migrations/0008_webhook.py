# Generated by Django 3.0.5 on 2021-09-06 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_remove_returndata_callbackurl'),
    ]

    operations = [
        migrations.CreateModel(
            name='Webhook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paymentConversation', models.CharField(max_length=510, verbose_name='paymentConversation:')),
                ('merchant', models.CharField(max_length=510, verbose_name='merchant:')),
                ('webhooktoken', models.CharField(max_length=510, verbose_name='webhooktoken:')),
                ('status', models.CharField(max_length=510, verbose_name='status:')),
                ('iyziReferenceCode', models.CharField(max_length=510, verbose_name='iyziReferenceCode:')),
                ('iyziEventType', models.CharField(max_length=510, verbose_name='iyziEventType:')),
                ('iyziEventTime', models.CharField(max_length=510, verbose_name='iyziEventTime:')),
            ],
        ),
    ]
