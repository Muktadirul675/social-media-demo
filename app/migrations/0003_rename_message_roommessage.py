# Generated by Django 4.1.1 on 2022-11-04 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_alter_message_room_alter_message_user_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Message',
            new_name='RoomMessage',
        ),
    ]
